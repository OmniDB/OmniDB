/**********************************************************************
 MIT License

 Portions Copyright (c) 2015-2019, The OmniDB Team
 Portions Copyright (c) 2017-2019, 2ndQuadrant Limited

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 **********************************************************************/

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
#if PG_VERSION_NUM >= 110000
#include "utils/expandedrecord.h"
#endif
#include "catalog/pg_proc.h"
#include "catalog/pg_type.h"
#include "plpgsql.h"
#include "miscadmin.h"
#include "libpq-fe.h"
#include "fmgr.h"
#include "utils/builtins.h"
#include "omnidb_plugin.h"

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
static void update_variables( PLpgSQL_execstate * estate );


/**********************************************************************
 * Other variables
 **********************************************************************/

static PLpgSQL_plugin plugin_funcs = { profiler_init, profiler_func_beg, profiler_func_end, profiler_stmt_beg, profiler_stmt_end };
PGconn *omnidb_plugin_conn;
bool omnidb_plugin_active = false;
unsigned int omnidb_plugin_depth = -1;
unsigned int omnidb_plugin_step;
int omnidb_plugin_breakpoint;
char omnidb_plugin_conninfo[1024];

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
 * omnidb_enable_debugger()
 * ------------------------------------------------------------------*/

PG_FUNCTION_INFO_V1(omnidb_enable_debugger);
Datum omnidb_enable_debugger(PG_FUNCTION_ARGS)
{
    omnidb_plugin_active = true;
    sprintf(omnidb_plugin_conninfo, "%s", text_to_cstring(PG_GETARG_TEXT_P(0)));
		PG_RETURN_VOID();
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

    if (omnidb_plugin_active)
    {
				omnidb_plugin_depth++;

				//First call
				if (omnidb_plugin_depth == 0)
		    {
		        omnidb_plugin_conn = PQconnectdb(omnidb_plugin_conninfo);
		        if (PQstatus(omnidb_plugin_conn) != CONNECTION_BAD)
		        {
		            #ifdef DEBUG
		                elog(LOG, "omnidb: Connected to (%s)", omnidb_plugin_conninfo);
		            #endif

		            char select_context[256];
		            sprintf(select_context, "SELECT pid FROM omnidb.contexts WHERE pid = %i", MyProcPid);
		            PGresult *res = PQexec(omnidb_plugin_conn, select_context);
		            if (PQresultStatus(res) == PGRES_TUPLES_OK && PQntuples(res) == 1)
		            {
		                char update_context[1024];
		                sprintf(update_context, "UPDATE omnidb.contexts SET function = '%s', hook = 'func_beg', stmttype = 'BEGIN', lineno = NULL where pid = %i", findProcName(func->fn_oid), MyProcPid);
		                PQexec(omnidb_plugin_conn, update_context);

		                #ifdef DEBUG
		                    elog(LOG, "omnidb: Debugger active for PID %i", MyProcPid);
		                #endif

		                omnidb_plugin_active = true;
		                omnidb_plugin_step = 0;
		            }
		            else
		            {
		                omnidb_plugin_active = false;
		                #ifdef DEBUG
		                    elog(LOG, "omnidb: Debugger not active for PID %i", MyProcPid);
		                #endif
		            }
		        }
		        else
		        {
		            omnidb_plugin_active = false;
		            elog(ERROR, "omnidb: Connection to database failed: %s", PQerrorMessage(omnidb_plugin_conn));
		        }
				}
				else
				{
					#ifdef DEBUG
							elog(LOG, "omnidb: Debugger not active for subcall in PID %i", MyProcPid);
					#endif
				}
    }
    else
    {
        #ifdef DEBUG
            elog(LOG, "omnidb: Debugger not active for PID %i", MyProcPid);
        #endif
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

    if (omnidb_plugin_active && !omnidb_plugin_depth)
    {
        update_variables(estate);

		char update_context[256];
		sprintf(update_context, "UPDATE omnidb.contexts SET finished = true WHERE pid = %i", MyProcPid);
		PQexec(omnidb_plugin_conn, update_context);

        char unlock[256];
        sprintf(unlock, "SELECT pg_advisory_unlock(%i) FROM omnidb.contexts WHERE pid = %i", MyProcPid, MyProcPid);
        PQexec(omnidb_plugin_conn, unlock);

        PQfinish(omnidb_plugin_conn);
    }
    else
    {
        if (omnidb_plugin_active && omnidb_plugin_depth > 0)
            omnidb_plugin_depth--;
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

    if (omnidb_plugin_active && !omnidb_plugin_depth)
    {
        char select_breakpoint[256];
        sprintf(select_breakpoint, "SELECT breakpoint FROM omnidb.contexts WHERE pid = %i", MyProcPid);
        PGresult *res = PQexec(omnidb_plugin_conn, select_breakpoint);
        if (PQresultStatus(res) == PGRES_TUPLES_OK && PQntuples(res) == 1)
            omnidb_plugin_breakpoint = atoi(PQgetvalue(res, 0, 0));
        else
            omnidb_plugin_breakpoint = 0;

				if ((omnidb_plugin_breakpoint == 0 || omnidb_plugin_breakpoint == stmt->lineno) && ((stmt->cmd_type == 11 && stmt->lineno != 0) || (stmt->cmd_type != 11)))
        {
            update_variables(estate);

            char update_context[1024];
            sprintf(update_context, "UPDATE omnidb.contexts SET function = '%s', hook = 'stmt_beg', stmttype = '%s', lineno = %d where pid = %i", findProcName(estate->func->fn_oid), decode_stmt_type(stmt->cmd_type), stmt->lineno, MyProcPid);
            PQexec(omnidb_plugin_conn, update_context);

            char unlock[256];
            sprintf(unlock, "SELECT pg_advisory_unlock(%i) FROM omnidb.contexts WHERE pid = %i", MyProcPid, MyProcPid);
            PQexec(omnidb_plugin_conn, unlock);

            char lock[256];
            sprintf(lock, "SELECT pg_advisory_lock(%i) FROM omnidb.contexts WHERE pid = %i", MyProcPid, MyProcPid);
            PQexec(omnidb_plugin_conn, lock);
        }

        char insert_statistics[256];
        sprintf(insert_statistics, "INSERT INTO omnidb.statistics (pid, lineno, step, tstart, tend) VALUES (%i, %i, %i, now(), NULL)", MyProcPid, stmt->lineno, omnidb_plugin_step);
        PQexec(omnidb_plugin_conn, insert_statistics);
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

    if (omnidb_plugin_active && !omnidb_plugin_depth)
    {
        char update_statistics[256];
        sprintf(update_statistics, "UPDATE omnidb.statistics SET tend = now() WHERE pid = %i AND lineno = %i AND step = %i", MyProcPid, stmt->lineno, omnidb_plugin_step);
        PQexec(omnidb_plugin_conn, update_statistics);

        omnidb_plugin_step++;
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

    typeTup = SearchSysCache( TYPEOID, ObjectIdGetDatum( var->datatype->typoid ), 0, 0, 0 );

    if( !HeapTupleIsValid( typeTup ))
		return( NULL );

    typeStruct = (Form_pg_type)GETSTRUCT( typeTup );

	fmgr_info( typeStruct->typoutput, &finfo_output );

    text_value = DatumGetCString( FunctionCall3( &finfo_output, var->value, ObjectIdGetDatum(typeStruct->typelem), Int32GetDatum(-1)));

	ReleaseSysCache( typeTup );

	if( name )
		*name = var->refname;

	if( type )
		*type = var->datatype->typname;

	return( text_value );
}

/* -------------------------------------------------------------------
 * update_variables()
 * ------------------------------------------------------------------*/

static void update_variables( PLpgSQL_execstate * estate )
{
    char delete_variables[256];
    sprintf(delete_variables, "DELETE FROM omnidb.variables WHERE pid = %i", MyProcPid);
    PQexec(omnidb_plugin_conn, delete_variables);

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
                PQexec(omnidb_plugin_conn, insert_variable);

                break;
            }

            case PLPGSQL_DTYPE_REC:
            {
                PLpgSQL_rec * rec = (PLpgSQL_rec *) estate->datums[i];
								char        * typeName;
								int		      att;
                char        * val;

								#if PG_VERSION_NUM >= 110000

										HeapTuple   tup;
										TupleDesc   tupdesc;

										if (rec->erh != NULL)
										{
												ExpandedRecordHeader * erh = (ExpandedRecordHeader *) rec->erh;
												tup = expanded_record_get_tuple(erh);
												tupdesc = expanded_record_get_tupdesc(erh);

												if (tupdesc != NULL)
												{
														for( att = 0; att < tupdesc->natts; ++att )
														{
																typeName = SPI_gettype( tupdesc, att + 1 );

																val = SPI_getvalue( tup, tupdesc, att + 1 );
																if (!val)
																		val = "NULL";

																#ifdef DEBUG
																		elog(LOG, "omnidb, REC, (%s.%s %s %s)",
																							rec->refname,
																							NameStr( tupdesc->attrs[att].attname ),
																							typeName,
																							val );
																#endif

																char insert_variable[1024];
																sprintf(insert_variable, "INSERT INTO omnidb.variables (pid, name, attribute, vartype, value) VALUES (%i, '%s', '%s', '%s', '%s')", MyProcPid, rec->refname, NameStr( tupdesc->attrs[att].attname ), typeName, val);
																PQexec(omnidb_plugin_conn, insert_variable);

																if( typeName )
																		pfree( typeName );
														}
												}
										}

								#else

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
														PQexec(omnidb_plugin_conn, insert_variable);

														if( typeName )
																pfree( typeName );
												}
										}

								#endif

								break;
            }

						default:
							break;
        }
    }
}
