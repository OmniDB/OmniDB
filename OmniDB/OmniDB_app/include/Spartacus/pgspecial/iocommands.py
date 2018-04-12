from contextlib import contextmanager
import re
import sys
import logging
import click
import io
import shlex
import sqlparse
import psycopg2
from os.path import expanduser
from .namedqueries import NamedQueries
from . import export
from .main import special_command

_logger = logging.getLogger(__name__)


@export
def editor_command(command):
    """
    Is this an external editor command?
    :param command: string
    """
    # It is possible to have `\e filename` or `SELECT * FROM \e`. So we check
    # for both conditions.
    return command.strip().endswith('\\e') or command.strip().startswith('\\e ')


@export
def get_filename(sql):
    if sql.strip().startswith('\\e'):
        command, _, filename = sql.partition(' ')
        return filename.strip() or None


@export
def get_watch_command(command):
    match = re.match("(.*?)[\s]*\\\\watch (\d+);?$", command)
    if match:
        groups = match.groups()
        return groups[0], int(groups[1])
    return None, None


@export
def get_editor_query(sql):
    """Get the query part of an editor command."""
    sql = sql.strip()

    # The reason we can't simply do .strip('\e') is that it strips characters,
    # not a substring. So it'll strip "e" in the end of the sql also!
    # Ex: "select * from style\e" -> "select * from styl".
    pattern = re.compile('(^\\\e|\\\e$)')
    while pattern.search(sql):
        sql = pattern.sub('', sql)

    return sql


@export
def open_external_editor(filename=None, sql=None):
    """
    Open external editor, wait for the user to type in his query,
    return the query.
    :return: list with one tuple, query as first element.
    """

    message = None
    filename = filename.strip().split(' ', 1)[0] if filename else None

    sql = sql or ''
    MARKER = '# Type your query above this line.\n'

    # Populate the editor buffer with the partial sql (if available) and a
    # placeholder comment.
    query = click.edit(u'{sql}\n\n{marker}'.format(sql=sql, marker=MARKER),
                       filename=filename, extension='.sql')

    if filename:
        try:
            query = read_from_file(filename)
        except IOError:
            message = 'Error reading file: %s.' % filename

    if query is not None:
        query = query.split(MARKER, 1)[0].rstrip('\n')
    else:
        # Don't return None for the caller to deal with.
        # Empty string is ok.
        query = sql

    return (query, message)


def read_from_file(path):
    with io.open(expanduser(path), encoding='utf-8') as f:
        contents = f.read()
    return contents


@contextmanager
def _paused_thread():
    try:
        thread = psycopg2.extensions.get_wait_callback()
        psycopg2.extensions.set_wait_callback(None)
        yield
    finally:
        psycopg2.extensions.set_wait_callback(thread)


def _index_of_file_name(tokenlist):
    for (idx, token) in reversed(list(enumerate(tokenlist[:-2]))):
        if token.is_keyword and token.value.upper() in ('TO', 'FROM'):
            return idx + 2
    return None


@special_command('\\copy', '\\copy [tablename] to/from [filename]',
                 'Copy data between a file and a table.')
def copy(cur, pattern, verbose):
    """Copies table data to/from files"""

    # Replace the specified file destination with STDIN or STDOUT
    parsed = sqlparse.parse(pattern)
    tokenlist = parsed[0].tokens
    idx = _index_of_file_name(tokenlist)
    file_name = tokenlist[idx].value
    before_file_name = ''.join(t.value for t in tokenlist[:idx])
    after_file_name = ''.join(t.value for t in tokenlist[idx+1:])

    direction = tokenlist[idx-2].value.upper()
    replacement_file_name = 'STDIN' if direction == 'FROM' else 'STDOUT'
    query = u'{0} {1} {2}'.format(before_file_name, replacement_file_name,
                                  after_file_name)
    open_mode = 'r' if direction == 'FROM' else 'w'
    if file_name.startswith("'") and file_name.endswith("'"):
        file = io.open(expanduser(file_name.strip("'")), mode=open_mode, encoding='utf-8')
    elif 'stdin' in file_name.lower():
        file = sys.stdin
    elif 'stdout' in file_name.lower():
        file = sys.stdout
    else:
        raise Exception('Enclose filename in single quotes')

    with _paused_thread():
        cur.copy_expert('copy ' + query, file)

    if cur.description:
        headers = [x[0] for x in cur.description]
        return [(None, cur, headers, cur.statusmessage)]
    else:
        return [(None, None, None, cur.statusmessage)]


def subst_favorite_query_args(query, args):
    """replace positional parameters ($1,$2,...$n) in query."""
    for idx, val in enumerate(args):
        subst_var = '$' + str(idx + 1)
        if subst_var not in query:
            return [None, 'query does not have substitution parameter ' + subst_var + ':\n  ' + query]

        query = query.replace(subst_var, val)

    match = re.search('\\$\d+', query)
    if match:
        return[None, 'missing substitution for ' + match.group(0) + ' in query:\n  ' + query]

    return [query, None]


@special_command('\\n', '\\n[+] [name] [param1 param2 ...]', 'List or execute named queries.')
def execute_named_query(cur, pattern, **_):
    """Returns (title, rows, headers, status)"""
    if pattern == '':
        return list_named_queries(True)

    params = shlex.split(pattern)
    pattern = params.pop(0)

    query = NamedQueries.instance.get(pattern)
    title = '> {}'.format(query)
    if query is None:
        message = "No named query: {}".format(pattern)
        return [(None, None, None, message)]

    try:
        if "$1" in query:
            query, params = subst_favorite_query_args(query, params)
            if query is None:
                raise Exception("Bad arguments\n" + params)
        cur.execute(query, params)
    except (IndexError, TypeError):
        raise Exception("Bad arguments")

    if cur.description:
        headers = [x[0] for x in cur.description]
        return [(title, cur, headers, cur.statusmessage)]
    else:
        return [(title, None, None, cur.statusmessage)]


def list_named_queries(verbose):
    """List of all named queries.
    Returns (title, rows, headers, status)"""
    if not verbose:
        rows = [[r] for r in NamedQueries.instance.list()]
        headers = ["Name"]
    else:
        headers = ["Name", "Query"]
        rows = [[r, NamedQueries.instance.get(r)]
                for r in NamedQueries.instance.list()]

    if not rows:
        status = NamedQueries.instance.usage
    else:
        status = ''
    return [('', rows, headers, status)]


@special_command('\\ns', '\\ns name query', 'Save a named query.')
def save_named_query(pattern, **_):
    """Save a new named query.
    Returns (title, rows, headers, status)"""

    usage = 'Syntax: \\ns name query.\n\n' + NamedQueries.instance.usage
    if not pattern:
        return [(None, None, None, usage)]

    name, _, query = pattern.partition(' ')

    # If either name or query is missing then print the usage and complain.
    if (not name) or (not query):
        return [(None, None, None,
            usage + 'Err: Both name and query are required.')]

    NamedQueries.instance.save(name, query)
    return [(None, None, None, "Saved.")]


@special_command('\\nd', '\\nd [name]', 'Delete a named query.')
def delete_named_query(pattern, **_):
    """Delete an existing named query.
    """
    usage = 'Syntax: \\nd name.\n\n' + NamedQueries.instance.usage
    if not pattern:
        return [(None, None, None, usage)]

    status = NamedQueries.instance.delete(pattern)

    return [(None, None, None, status)]
