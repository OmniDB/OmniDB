/**********************************************************************
 * Headers
 **********************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "postgres.h"
#if PG_VERSION_NUM >= 90300
#include "access/htup_details.h"
#endif
#include "utils/syscache.h"
#include "catalog/pg_proc.h"
#include "catalog/pg_type.h"
#include "plpgsql.h"
#include "miscadmin.h"
#include "libpq-fe.h"

PG_MODULE_MAGIC;

/**********************************************************************
 * Function prototypes
 **********************************************************************/

void load_plugin( PLpgSQL_plugin * hooks );
static void profiler_init(PLpgSQL_execstate * estate, PLpgSQL_function * func);
static void profiler_func_beg(PLpgSQL_execstate * estate, PLpgSQL_function * func);
static void profiler_func_end(PLpgSQL_execstate * estate, PLpgSQL_function * func);
static void profiler_stmt_beg(PLpgSQL_execstate * estate, PLpgSQL_stmt * stmt);
static void profiler_stmt_end(PLpgSQL_execstate * estate, PLpgSQL_stmt * stmt);
static char * findProcName(Oid oid);
char *decode_stmt_type(int typ);
static bool var_is_argument(PLpgSQL_execstate *estate, int i, char **p_argname);
static bool var_is_null(PLpgSQL_datum *datum);
static char *get_text_val(PLpgSQL_var *var, char **name, char **type);


/**********************************************************************
 * Other variables
 **********************************************************************/

static PLpgSQL_plugin plugin_funcs = { profiler_init, profiler_func_beg, profiler_func_end, profiler_stmt_beg, profiler_stmt_end };
PGconn *plugin_conn;
bool plugin_active = false;
unsigned int plugin_depth = 0;
unsigned int plugin_step;
int plugin_breakpoint;

/**********************************************************************
 * Function definitions
 **********************************************************************/

/* -------------------------------------------------------------------
 * _PG_init()
 * ------------------------------------------------------------------*/

void _PG_init( void )
{
	PLpgSQL_plugin ** var_ptr = (PLpgSQL_plugin **) find_rendezvous_variable("PLpgSQL_plugin");
	*var_ptr = &plugin_funcs;
}

/* -------------------------------------------------------------------
 * load_plugin()
 * ------------------------------------------------------------------*/

void load_plugin( PLpgSQL_plugin * hooks )
{
	hooks->func_setup = profiler_init;
	hooks->func_beg   = profiler_func_beg;
	hooks->func_end   = profiler_func_end;
	hooks->stmt_beg   = profiler_stmt_beg;
	hooks->stmt_end   = profiler_stmt_end;
}

/* -------------------------------------------------------------------
 * profiler_init()
 * ------------------------------------------------------------------*/

static void profiler_init( PLpgSQL_execstate * estate, PLpgSQL_function * func )
{
    #ifdef DEBUG
        elog(LOG, "omnidb, DECLARE, %s, %i", findProcName(func->fn_oid), MyProcPid);
    #endif
}

/* -------------------------------------------------------------------
 * profiler_func_beg()
 * ------------------------------------------------------------------*/

static void profiler_func_beg( PLpgSQL_execstate * estate, PLpgSQL_function * func )
{
    #ifdef DEBUG
	   elog(LOG, "omnidb, BEGIN, %s, %i", findProcName(func->fn_oid), MyProcPid);
    #endif

    if (!plugin_active)
    {
        PGconn *conn = PQconnectdb("user=postgres dbname=postgres");
        if (PQstatus(conn) != CONNECTION_BAD)
        {
            char query[256];
            sprintf(query, "SELECT datname FROM pg_database WHERE oid = %i", MyDatabaseId);
            PGresult *res = PQexec(conn, query);
            if (PQresultStatus(res) == PGRES_TUPLES_OK)
            {
                char conninfo[256];
                sprintf(conninfo, "user=postgres dbname=%s", PQgetvalue(res, 0, 0));
                plugin_conn = PQconnectdb(conninfo);
                if (PQstatus(plugin_conn) != CONNECTION_BAD)
                {
                    PQclear(res);
                    PQfinish(conn);

                    #ifdef DEBUG
                        elog(LOG, "omnidb: Connected to (%s)", conninfo);
                    #endif

                    char select_context[1024];
                    sprintf(select_context, "SELECT pid FROM omnidb.contexts WHERE pid = %i", MyProcPid);
                    PGresult *res = PQexec(plugin_conn, select_context);
                    if (PQresultStatus(res) == PGRES_TUPLES_OK && PQntuples(res) == 1)
                    {
                        char update_context[1024];
                        sprintf(update_context, "UPDATE omnidb.contexts SET function = '%s', hook = 'func_beg', stmttype = 'BEGIN', lineno = NULL where pid = %i", findProcName(func->fn_oid), MyProcPid);
                        PQexec(plugin_conn, update_context);

                        #ifdef DEBUG
                            elog(LOG, "omnidb: Debugger active for PID %i", MyProcPid);
                        #endif

                        plugin_active = true;
                        plugin_step = 0;
                    }
                    else
                    {
                        plugin_active = false;
                        #ifdef DEBUG
                            elog(LOG, "omnidb: Debugger not active for PID %i", MyProcPid);
                        #endif
                    }
                }
                else
                {
                    plugin_active = false;
                    elog(ERROR, "omnidb: Connection to database failed: %s", PQerrorMessage(plugin_conn));
                }
            }
        }
        else
        {
            plugin_active = false;
            elog(ERROR, "omnidb: Connection to maintenance database failed: %s", PQerrorMessage(conn));
        }
    }
    else
    {
        #ifdef DEBUG
            elog(LOG, "omnidb: Debugger not active for subcall depth %i for PID %i", plugin_depth, MyProcPid);
        #endif

        plugin_depth++;
    }
}

/* -------------------------------------------------------------------
 * profiler_func_end()
 * ------------------------------------------------------------------*/

static void profiler_func_end( PLpgSQL_execstate * estate, PLpgSQL_function * func )
{
    #ifdef DEBUG
       elog(LOG, "omnidb, END, %s, %i", findProcName(func->fn_oid), MyProcPid);
    #endif

    if (plugin_active && !plugin_depth)
    {
        char unlock[256];
        sprintf(unlock, "select pg_advisory_unlock(%i) from omnidb.contexts where pid = %i", MyProcPid, MyProcPid);
        PQexec(plugin_conn, unlock);

        PQfinish(plugin_conn);
    }
    else
    {
        if (plugin_active && plugin_depth > 0)
            plugin_depth--;
    }
}

/* -------------------------------------------------------------------
 * profiler_stmt_beg()
 * ------------------------------------------------------------------*/

static void profiler_stmt_beg( PLpgSQL_execstate * estate, PLpgSQL_stmt * stmt )
{
    #ifdef DEBUG
        elog(LOG, "omnidb, STMT START, line %d, type %s, %s, %i", stmt->lineno, decode_stmt_type(stmt->cmd_type), findProcName(estate->func->fn_oid), MyProcPid);
    #endif

    if (plugin_active && !plugin_depth)
    {
        char select_breakpoint[1024];
        sprintf(select_breakpoint, "SELECT breakpoint FROM omnidb.contexts WHERE pid = %i", MyProcPid);
        PGresult *res = PQexec(plugin_conn, select_breakpoint);
        if (PQresultStatus(res) == PGRES_TUPLES_OK && PQntuples(res) == 1)
            plugin_breakpoint = atoi(PQgetvalue(res, 0, 0));
        else
            plugin_breakpoint = 0;

        if (plugin_breakpoint == 0 || plugin_breakpoint == stmt->lineno)
        {
            char delete_variables[1024];
            sprintf(delete_variables, "DELETE FROM omnidb.variables WHERE pid = %i", MyProcPid);
            PQexec(plugin_conn, delete_variables);

            int i;
            for( i = 0; i < estate->ndatums; i++ )
            {
                switch( estate->datums[i]->dtype )
                {
                    case PLPGSQL_DTYPE_VAR:
        			{
        				PLpgSQL_var * var = (PLpgSQL_var *) estate->datums[i];
        				char        * val;
        				char		* name = var->refname;
                        char        * typeName;

                        typeName = var->datatype ? var->datatype->typname : "InvalidType";

        				if( var_is_null((PLpgSQL_datum *)var ))
        					val = "NULL";
        				else
        					val = get_text_val( var, NULL, NULL );

                        #ifdef DEBUG
                            elog(LOG, "omnidb, VAR, (%s %s %s)", name, typeName, val);
                        #endif

                        char insert_variable[1024];
                        sprintf(insert_variable, "INSERT INTO omnidb.variables (pid, name, attribute, vartype, value) VALUES (%i, '%s', NULL, '%s', '%s')", MyProcPid, name, typeName, val);
                        PQexec(plugin_conn, insert_variable);

        				break;
        			}
                    case PLPGSQL_DTYPE_REC:
        			{
        				PLpgSQL_rec * rec = (PLpgSQL_rec *) estate->datums[i];
        				int		      att;
        				char        * typeName;
                        char        * val;

        				if (rec->tupdesc != NULL)
        				{
        					for( att = 0; att < rec->tupdesc->natts; ++att )
        					{
        						typeName = SPI_gettype( rec->tupdesc, att + 1 );

                                val = SPI_getvalue( rec->tup, rec->tupdesc, att + 1 );
                                if (!val)
                                    val = "NULL";

                                #ifdef DEBUG
                                    elog(LOG, "omnidb, REC, (%s.%s %s %s)",
        								      rec->refname,
                                              NameStr( rec->tupdesc->attrs[att]->attname ),
        								      typeName,
                                              val );
                                #endif

                                char insert_variable[1024];
                                sprintf(insert_variable, "INSERT INTO omnidb.variables (pid, name, attribute, vartype, value) VALUES (%i, '%s', '%s', '%s', '%s')", MyProcPid, rec->refname, NameStr( rec->tupdesc->attrs[att]->attname ), typeName, val);
                                PQexec(plugin_conn, insert_variable);

        						if( typeName )
        							pfree( typeName );
        					}
        				}
        				break;
        			}
                }
            }

            char update_context[1024];
            sprintf(update_context, "UPDATE omnidb.contexts SET function = '%s', hook = 'stmt_beg', stmttype = '%s', lineno = %d where pid = %i", findProcName(estate->func->fn_oid), decode_stmt_type(stmt->cmd_type), stmt->lineno, MyProcPid);
            PQexec(plugin_conn, update_context);

            char unlock[256];
            sprintf(unlock, "select pg_advisory_unlock(%i) from omnidb.contexts where pid = %i", MyProcPid, MyProcPid);
            PQexec(plugin_conn, unlock);

            char lock[256];
            sprintf(lock, "select pg_advisory_lock(%i) from omnidb.contexts where pid = %i", MyProcPid, MyProcPid);
            PQexec(plugin_conn, lock);
        }

        char insert_statistics[1024];
        sprintf(insert_statistics, "INSERT INTO omnidb.statistics (pid, lineno, step, tstart, tend) VALUES (%i, %i, %i, now(), NULL)", MyProcPid, stmt->lineno, plugin_step);
        PQexec(plugin_conn, insert_statistics);
    }
}

/* -------------------------------------------------------------------
 * profiler_stmt_end()
 * ------------------------------------------------------------------*/

static void profiler_stmt_end( PLpgSQL_execstate * estate, PLpgSQL_stmt * stmt )
{
    #ifdef DEBUG
        elog(LOG, "omnidb, STMT END, line %d, type %s, %s, %i", stmt->lineno, decode_stmt_type(stmt->cmd_type), findProcName(estate->func->fn_oid), MyProcPid);
    #endif

    if (plugin_active && !plugin_depth)
    {
        char update_statistics[1024];
        sprintf(update_statistics, "UPDATE omnidb.statistics SET tend = now() WHERE pid = %i AND lineno = %i AND step = %i", MyProcPid, stmt->lineno, plugin_step);
        PQexec(plugin_conn, update_statistics);

        plugin_step++;
    }
}

/* -------------------------------------------------------------------
 * findProcName()
 * ------------------------------------------------------------------*/

static char * findProcName(Oid oid)
{
	HeapTuple	procTuple;
	char       *procName;

	procTuple = SearchSysCache(PROCOID, ObjectIdGetDatum(oid), 0, 0, 0);

	if(!HeapTupleIsValid(procTuple))
		elog(ERROR, "omnidb: cache lookup for proc %u failed", oid);

	procName = NameStr(((Form_pg_proc) GETSTRUCT(procTuple))->proname);
	ReleaseSysCache(procTuple);

	return procName;
}

/* -------------------------------------------------------------------
 * decode_stmt_type()
 * ------------------------------------------------------------------*/

char *decode_stmt_type(int typ)
{
	char *decoded_type = "unknown";

    switch (typ)
    {
        case PLPGSQL_STMT_BLOCK:
            decoded_type = "BLOCK";
            break;

        case PLPGSQL_STMT_ASSIGN:
            decoded_type = "ASSIGN";
            break;

        case PLPGSQL_STMT_PERFORM:
            decoded_type = "PERFORM";
            break;

        case PLPGSQL_STMT_GETDIAG:
            decoded_type = "GETDIAG";
            break;

        case PLPGSQL_STMT_IF:
            decoded_type = "IF";
            break;

        case PLPGSQL_STMT_CASE:
            decoded_type = "CASE";
            break;

        case PLPGSQL_STMT_LOOP:
            decoded_type = "LOOP";
            break;

        case PLPGSQL_STMT_WHILE:
            decoded_type = "WHILE";
            break;

        case PLPGSQL_STMT_FORI:
            decoded_type = "FORI";
            break;

        case PLPGSQL_STMT_FORS:
            decoded_type = "FORS";
            break;

        case PLPGSQL_STMT_FORC:
            decoded_type = "FORC";
            break;

        case PLPGSQL_STMT_EXIT:
            decoded_type = "EXIT";
            break;

        case PLPGSQL_STMT_RETURN:
            decoded_type = "RETURN";
            break;

        case PLPGSQL_STMT_RETURN_NEXT:
            decoded_type = "RETURN NEXT";
            break;

        case PLPGSQL_STMT_RETURN_QUERY:
            decoded_type = "RETURN QUERY";
            break;

        case PLPGSQL_STMT_RAISE:
            decoded_type = "RAISE";
            break;

        case PLPGSQL_STMT_EXECSQL:
            decoded_type = "EXEC SQL";
            break;

        case PLPGSQL_STMT_DYNEXECUTE:
            decoded_type = "DYNEXECUTE";
            break;

        case PLPGSQL_STMT_DYNFORS:
            decoded_type = "DYNFORS";
            break;

        case PLPGSQL_STMT_OPEN:
            decoded_type = "OPEN";
            break;

        case PLPGSQL_STMT_FETCH:
            decoded_type = "FETCH";
            break;

        case PLPGSQL_STMT_CLOSE:
            decoded_type = "CLOSE";
            break;
    }

    return decoded_type;
}

/* -------------------------------------------------------------------
 * var_is_null()
 * ------------------------------------------------------------------*/

static bool var_is_null(PLpgSQL_datum *datum)
{
	switch (datum->dtype)
	{
		case PLPGSQL_DTYPE_VAR:
		{
			PLpgSQL_var *var = (PLpgSQL_var *) datum;

			if (var->isnull)
				return true;
		}
		break;

		/* other data types are not currently handled, we just return true */
		case PLPGSQL_DTYPE_REC:
		case PLPGSQL_DTYPE_ROW:
			return true;

		default:
			return true;
	}

	return false;
}

/* -------------------------------------------------------------------
 * var_is_null()
 * ------------------------------------------------------------------*/

static char *get_text_val(PLpgSQL_var *var, char **name, char **type)
{
	HeapTuple	       typeTup;
    Form_pg_type       typeStruct;
    FmgrInfo	       finfo_output;
	char            *  text_value = NULL;

    /* Find the output function for this data type */
    typeTup = SearchSysCache( TYPEOID, ObjectIdGetDatum( var->datatype->typoid ), 0, 0, 0 );

    if( !HeapTupleIsValid( typeTup ))
		return( NULL );

    typeStruct = (Form_pg_type)GETSTRUCT( typeTup );

	/* Now invoke the output function to convert the variable into a null-terminated string */
    fmgr_info( typeStruct->typoutput, &finfo_output );

    text_value = DatumGetCString( FunctionCall3( &finfo_output, var->value, ObjectIdGetDatum(typeStruct->typelem), Int32GetDatum(-1)));

	ReleaseSysCache( typeTup );

	if( name )
		*name = var->refname;

	if( type )
		*type = var->datatype->typname;

	return( text_value );
}
