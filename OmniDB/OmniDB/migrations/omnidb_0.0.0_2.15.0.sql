CREATE TABLE db_type (
    dbt_st_name varchar(40),
    dbt_in_enabled integer,
    constraint pk_db_type primary key (dbt_st_name)
);--omnidb--
INSERT INTO db_type VALUES('sqlite',0);--omnidb--
INSERT INTO db_type VALUES('mysql',1);--omnidb--
INSERT INTO db_type VALUES('postgresql',1);--omnidb--
INSERT INTO db_type VALUES('firebird',0);--omnidb--
INSERT INTO db_type VALUES('oracle',1);--omnidb--
INSERT INTO db_type VALUES('sqlserver',0);--omnidb--
INSERT INTO db_type VALUES('access',0);--omnidb--
INSERT INTO db_type VALUES('sqlce',0);--omnidb--
INSERT INTO db_type VALUES('mariadb',1);--omnidb--
INSERT INTO db_type VALUES('filedb',0);--omnidb--

CREATE TABLE data_categories (
    cat_st_name varchar(40),
    cat_st_description varchar(100),
    cat_st_class varchar(40),
    constraint pk_data_categories primary key (cat_st_name)
);--omnidb--
INSERT INTO data_categories VALUES('bigint','Big Integer','numeric');--omnidb--
INSERT INTO data_categories VALUES('boolean','Boolean','other');--omnidb--
INSERT INTO data_categories VALUES('char','String','text');--omnidb--
INSERT INTO data_categories VALUES('date','Date Only','other');--omnidb--
INSERT INTO data_categories VALUES('datetime','Date Time','other');--omnidb--
INSERT INTO data_categories VALUES('decimal','Decimal','numeric');--omnidb--
INSERT INTO data_categories VALUES('fp','Floating Point','numeric');--omnidb--
INSERT INTO data_categories VALUES('integer','Integer','numeric');--omnidb--
INSERT INTO data_categories VALUES('smallint','Small Integer','numeric');--omnidb--
INSERT INTO data_categories VALUES('text','Long String','text');--omnidb--
INSERT INTO data_categories VALUES('time','Time Only','other');--omnidb--
INSERT INTO data_categories VALUES('varchar','Var String','text');--omnidb--

CREATE TABLE data_types (
    cat_st_name varchar(40),
    dbt_st_name varchar(40),
    dt_type varchar(100),
    dt_in_sufix integer,
    dt_st_writeformat varchar(1000),
    dt_st_readformat varchar(1000),
    dt_st_compareformat varchar(1000),
    constraint pk_data_types primary key (dbt_st_name, dt_type),
    constraint data_types_fk_0 foreign key (cat_st_name) references data_categories (cat_st_name),
    constraint data_types_fk_1 foreign key (dbt_st_name) references db_type (dbt_st_name)
);--omnidb--
INSERT INTO data_types VALUES('text','access','binary',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('boolean','access','boolean',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('text','access','byte',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('bigint','access','complex_type',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','access','double',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','access','float',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','access','guid',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','access','int',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('bigint','access','long',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','access','memo',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','access','money',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','access','numeric',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','access','ole',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('datetime','access','short_date_time',0,'''#''','format(Nz(CStr(#),''''),''yyyy-MM-dd H:nn:ss'') as #','format(Nz(CStr(#),''''),''yyyy-MM-dd H:nn:ss'')');--omnidb--
INSERT INTO data_types VALUES('text','access','text',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('bigint','firebird','bigint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('char','firebird','char',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('date','firebird','date',0,'cast(''#'' as date)',replace('lpad(cast(extract(year from cast(# as timestamp)) as varchar(4)), 4, ''0'') || ''-'' ||\nlpad(cast(extract(month from cast(# as timestamp)) as varchar(2)), 2, ''0'') || ''-'' ||\nlpad(cast(extract(day from cast(# as timestamp)) as varchar(2)), 2, ''0'') as #','\n',char(10)),replace('lpad(cast(extract(year from cast(# as timestamp)) as varchar(4)), 4, ''0'') || ''-'' ||\nlpad(cast(extract(month from cast(# as timestamp)) as varchar(2)), 2, ''0'') || ''-'' ||\nlpad(cast(extract(day from cast(# as timestamp)) as varchar(2)), 2, ''0'')','\n',char(10)));--omnidb--
INSERT INTO data_types VALUES('decimal','firebird','decimal',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','firebird','double',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','firebird','double precision',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','firebird','float',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','firebird','int',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','firebird','integer',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('char','firebird','nchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('text','firebird','ntext',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','firebird','numeric',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','firebird','nvarchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','firebird','real',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','firebird','smallint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','firebird','BLOB SUB_TYPE TEXT',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('time','firebird','time',0,'cast(''#'' as time)',replace('lpad(cast(extract(hour from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(extract(minute from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(round(extract(second from cast(# as timestamp))) as varchar(2)), 2, ''0'') as #','\n',char(10)),replace('lpad(cast(extract(hour from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(extract(minute from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(round(extract(second from cast(# as timestamp))) as varchar(2)), 2, ''0'')','\n',char(10)));--omnidb--
INSERT INTO data_types VALUES('datetime','firebird','timestamp',0,'cast(''#'' as timestamp)',replace('lpad(cast(extract(year from cast(# as timestamp)) as varchar(4)), 4, ''0'') || ''-'' ||\nlpad(cast(extract(month from cast(# as timestamp)) as varchar(2)), 2, ''0'') || ''-'' ||\nlpad(cast(extract(day from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '' '' ||\nlpad(cast(extract(hour from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(extract(minute from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(round(extract(second from cast(# as timestamp))) as varchar(2)), 2, ''0'') as #','\n',char(10)),replace('lpad(cast(extract(year from cast(# as timestamp)) as varchar(4)), 4, ''0'') || ''-'' ||\nlpad(cast(extract(month from cast(# as timestamp)) as varchar(2)), 2, ''0'') || ''-'' ||\nlpad(cast(extract(day from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '' '' ||\nlpad(cast(extract(hour from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(extract(minute from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(round(extract(second from cast(# as timestamp))) as varchar(2)), 2, ''0'')','\n',char(10)));--omnidb--
INSERT INTO data_types VALUES('smallint','firebird','tinyint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','firebird','varchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('bigint','mysql','bigint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','mysql','bit',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('boolean','mysql','boolean',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('char','mysql','char',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('date','mysql','date',0,'STR_TO_DATE(''#'', ''%Y-%m-%d'')','DATE_FORMAT(#, ''%Y-%m-%d'') as #','DATE_FORMAT(#, ''%Y-%m-%d'')');--omnidb--
INSERT INTO data_types VALUES('datetime','mysql','datetime',0,'STR_TO_DATE(''#'', ''%Y-%m-%d %H:%i:%s'')','DATE_FORMAT(#, ''%Y-%m-%d %H:%i:%s'') as #','DATE_FORMAT(#, ''%Y-%m-%d %H:%i:%s'')');--omnidb--
INSERT INTO data_types VALUES('decimal','mysql','decimal',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','mysql','double',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','mysql','double precision',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','mysql','float',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','mysql','int',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','mysql','integer',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','mysql','mediumint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','mysql','numeric',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','mysql','smallint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','mysql','text',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','mysql','tinyint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','mysql','varchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','oracle','binary_double',0,'#','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('fp','oracle','binary_float',0,'#','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('char','oracle','char',1,'''#''','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','date',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('fp','oracle','double',0,'#','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('fp','oracle','float',0,'#','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('bigint','oracle','integer',0,'#','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('char','oracle','nchar',1,'''#''','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('decimal','oracle','number',2,'#','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('decimal','oracle','numeric',2,'#','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('varchar','oracle','nvarchar2',1,'''#''','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(0)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(1)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(2)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(3)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(4)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(5)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(6)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(7)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(8)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('datetime','oracle','timestamp(9)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');--omnidb--
INSERT INTO data_types VALUES('varchar','oracle','varchar',1,'''#''','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('varchar','oracle','varchar2',1,'''#''','to_char(#) as #','#');--omnidb--
INSERT INTO data_types VALUES('bigint','postgresql','bigint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('bigint','postgresql','bigserial',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('boolean','postgresql','boolean',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('char','postgresql','char',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('char','postgresql','character',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','postgresql','character varying',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('date','postgresql','date',0,'''#''','to_char(#::date, ''YYYY-mm-dd'') as #','to_char(#::date, ''YYYY-mm-dd'')');--omnidb--
INSERT INTO data_types VALUES('decimal','postgresql','decimal',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','postgresql','double precision',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','postgresql','float',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','postgresql','integer',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','postgresql','money',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','postgresql','numeric',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','postgresql','real',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','postgresql','serial',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','postgresql','smallint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','postgresql','smallserial',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','postgresql','text',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('time','postgresql','time with time zone',0,'''#''','to_char(#::time, ''hh24:mi:ss'') as #','to_char(#::time, ''hh24:mi:ss'')');--omnidb--
INSERT INTO data_types VALUES('time','postgresql','time without time zone',0,'''#''','to_char(#::time, ''hh24:mi:ss'') as #','to_char(#::time, ''hh24:mi:ss'')');--omnidb--
INSERT INTO data_types VALUES('datetime','postgresql','timestamp with time zone',0,'''#''','to_char(#::timestamp, ''YYYY-mm-dd hh24:mi:ss'') as #','to_char(#::timestamp, ''YYYY-mm-dd hh24:mi:ss'')');--omnidb--
INSERT INTO data_types VALUES('datetime','postgresql','timestamp without time zone',0,'''#''','to_char(#::timestamp, ''YYYY-mm-dd hh24:mi:ss'') as #','to_char(#::timestamp, ''YYYY-mm-dd hh24:mi:ss'')');--omnidb--
INSERT INTO data_types VALUES('varchar','postgresql','varchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('char','sqlite','char',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','sqlite','integer',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','sqlite','numeric',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','sqlite','nvarchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','sqlite','real',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','sqlite','varchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('bigint','sqlserver','bigint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlserver','binary',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlserver','bit',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('char','sqlserver','char',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('date','sqlserver','date',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');--omnidb--
INSERT INTO data_types VALUES('datetime','sqlserver','datetime',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');--omnidb--
INSERT INTO data_types VALUES('datetime','sqlserver','datetime2',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');--omnidb--
INSERT INTO data_types VALUES('datetime','sqlserver','datetimeoffset',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');--omnidb--
INSERT INTO data_types VALUES('decimal','sqlserver','decimal',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','sqlserver','float',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlserver','image',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','sqlserver','int',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','sqlserver','money',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('char','sqlserver','nchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlserver','ntext',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','sqlserver','numeric',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','sqlserver','nvarchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','sqlserver','real',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('datetime','sqlserver','smalldatetime',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');--omnidb--
INSERT INTO data_types VALUES('smallint','sqlserver','smallint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','sqlserver','smallmoney',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlserver','text',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('time','sqlserver','time',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');--omnidb--
INSERT INTO data_types VALUES('datetime','sqlserver','timestamp',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');--omnidb--
INSERT INTO data_types VALUES('smallint','sqlserver','tinyint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlserver','varbinary',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','sqlserver','varchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','sqlserver','integer',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','oracle','clob',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlite','text',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('datetime','access','datetime',0,'''#''','format(Nz(CStr(#),''''),''yyyy-MM-dd H:nn:ss'') as #','format(Nz(CStr(#),''''),''yyyy-MM-dd H:nn:ss'')');--omnidb--
INSERT INTO data_types VALUES('time','mysql','time',0,'STR_TO_DATE(''#'', ''%H:%i:%s'')','DATE_FORMAT(#, ''%H:%i:%s'') as #','DATE_FORMAT(#, ''%H:%i:%s'')');--omnidb--
INSERT INTO data_types VALUES('bigint','sqlce','bigint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlce','binary',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlce','bit',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('datetime','sqlce','datetime',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');--omnidb--
INSERT INTO data_types VALUES('fp','sqlce','float',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlce','image',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','sqlce','integer',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','sqlce','money',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlce','ntext',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','sqlce','numeric',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','sqlce','real',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','sqlce','smallint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','sqlce','tinyint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','sqlce','varbinary',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('bigint','mariadb','bigint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','mariadb','bit',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('boolean','mariadb','boolean',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('char','mariadb','char',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('date','mariadb','date',0,'STR_TO_DATE(''#'', ''%Y-%m-%d'')','DATE_FORMAT(#, ''%Y-%m-%d'') as #','DATE_FORMAT(#, ''%Y-%m-%d'')');--omnidb--
INSERT INTO data_types VALUES('datetime','mariadb','datetime',0,'STR_TO_DATE(''#'', ''%Y-%m-%d %H:%i:%s'')','DATE_FORMAT(#, ''%Y-%m-%d %H:%i:%s'') as #','DATE_FORMAT(#, ''%Y-%m-%d %H:%i:%s'')');--omnidb--
INSERT INTO data_types VALUES('decimal','mariadb','decimal',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','mariadb','double',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','mariadb','double precision',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('fp','mariadb','float',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','mariadb','int',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','mariadb','integer',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('integer','mariadb','mediumint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('decimal','mariadb','numeric',2,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('smallint','mariadb','smallint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('text','mariadb','text',0,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('time','mariadb','time',0,'STR_TO_DATE(''#'', ''%H:%i:%s'')','DATE_FORMAT(#, ''%H:%i:%s'') as #','DATE_FORMAT(#, ''%H:%i:%s'')');--omnidb--
INSERT INTO data_types VALUES('smallint','mariadb','tinyint',0,'#','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','mariadb','varchar',1,'''#''','#','#');--omnidb--
INSERT INTO data_types VALUES('varchar','filedb','varchar',0,'''#''','#','#');--omnidb--

CREATE TABLE representatives (
    cat_st_name varchar(40),
    dbt_st_name varchar(40),
    rep_st_default varchar(100),
    dt_type varchar(100),
    constraint pk_rep primary key (cat_st_name, dbt_st_name),
    constraint fk_rep_dc foreign key (cat_st_name) references data_categories (cat_st_name),
    constraint fk_rep_dbt foreign key (dbt_st_name) references db_type (dbt_st_name),
    constraint fk_rep_dt foreign key (dbt_st_name, dt_type) references data_types (dbt_st_name, dt_type)
);--omnidb--
INSERT INTO representatives VALUES('smallint','oracle','number(5,0)','number');--omnidb--
INSERT INTO representatives VALUES('integer','oracle','number(10,0)','number');--omnidb--
INSERT INTO representatives VALUES('bigint','oracle','number(19,0)','number');--omnidb--
INSERT INTO representatives VALUES('decimal','oracle','number(38,0)','number');--omnidb--
INSERT INTO representatives VALUES('fp','oracle','number(38,4)','number');--omnidb--
INSERT INTO representatives VALUES('boolean','oracle','char(1)','char');--omnidb--
INSERT INTO representatives VALUES('varchar','oracle','varchar2(1000)','varchar2');--omnidb--
INSERT INTO representatives VALUES('boolean','postgresql','boolean','boolean');--omnidb--
INSERT INTO representatives VALUES('smallint','postgresql','smallint','smallint');--omnidb--
INSERT INTO representatives VALUES('integer','postgresql','bigint','bigint');--omnidb--
INSERT INTO representatives VALUES('bigint','postgresql','bigint','bigint');--omnidb--
INSERT INTO representatives VALUES('decimal','postgresql','numeric','numeric');--omnidb--
INSERT INTO representatives VALUES('fp','postgresql','double precision','double precision');--omnidb--
INSERT INTO representatives VALUES('fp','mysql','double precision','double precision');--omnidb--
INSERT INTO representatives VALUES('smallint','mysql','smallint','smallint');--omnidb--
INSERT INTO representatives VALUES('integer','mysql','integer','integer');--omnidb--
INSERT INTO representatives VALUES('bigint','mysql','bigint','bigint');--omnidb--
INSERT INTO representatives VALUES('varchar','mysql','varchar(1000)','varchar');--omnidb--
INSERT INTO representatives VALUES('boolean','mysql','boolean','boolean');--omnidb--
INSERT INTO representatives VALUES('varchar','postgresql','character varying','character varying');--omnidb--
INSERT INTO representatives VALUES('decimal','mysql','decimal(38,0)','decimal');--omnidb--
INSERT INTO representatives VALUES('decimal','firebird','decimal(38,0)','decimal');--omnidb--
INSERT INTO representatives VALUES('smallint','firebird','smallint','smallint');--omnidb--
INSERT INTO representatives VALUES('integer','firebird','integer','integer');--omnidb--
INSERT INTO representatives VALUES('bigint','firebird','bigint','bigint');--omnidb--
INSERT INTO representatives VALUES('varchar','firebird','varchar(1000)','varchar');--omnidb--
INSERT INTO representatives VALUES('boolean','firebird','char(1)','char');--omnidb--
INSERT INTO representatives VALUES('fp','firebird','double precision','double precision');--omnidb--
INSERT INTO representatives VALUES('datetime','postgresql','timestamp without time zone','timestamp without time zone');--omnidb--
INSERT INTO representatives VALUES('decimal','sqlite','numeric(38,0)','numeric');--omnidb--
INSERT INTO representatives VALUES('smallint','sqlite','integer','integer');--omnidb--
INSERT INTO representatives VALUES('integer','sqlite','integer','integer');--omnidb--
INSERT INTO representatives VALUES('bigint','sqlite','integer','integer');--omnidb--
INSERT INTO representatives VALUES('varchar','sqlite','varchar(1000)','varchar');--omnidb--
INSERT INTO representatives VALUES('boolean','sqlite','char(1)','char');--omnidb--
INSERT INTO representatives VALUES('fp','sqlite','real','real');--omnidb--
INSERT INTO representatives VALUES('varchar','sqlserver','varchar(1000)','varchar');--omnidb--
INSERT INTO representatives VALUES('char','firebird','char(1000)','char');--omnidb--
INSERT INTO representatives VALUES('char','mysql','char(255)','char');--omnidb--
INSERT INTO representatives VALUES('char','oracle','char(1000)','char');--omnidb--
INSERT INTO representatives VALUES('char','postgresql','char(1000)','char');--omnidb--
INSERT INTO representatives VALUES('char','sqlite','char(1000)','char');--omnidb--
INSERT INTO representatives VALUES('char','sqlserver','char(1000)','char');--omnidb--
INSERT INTO representatives VALUES('text','firebird','BLOB SUB_TYPE TEXT','BLOB SUB_TYPE TEXT');--omnidb--
INSERT INTO representatives VALUES('text','mysql','text','text');--omnidb--
INSERT INTO representatives VALUES('text','oracle','clob','clob');--omnidb--
INSERT INTO representatives VALUES('text','postgresql','text','text');--omnidb--
INSERT INTO representatives VALUES('text','sqlite','text','text');--omnidb--
INSERT INTO representatives VALUES('text','sqlserver','text','text');--omnidb--
INSERT INTO representatives VALUES('decimal','sqlserver','decimal(38,0)','decimal');--omnidb--
INSERT INTO representatives VALUES('smallint','sqlserver','smallint','smallint');--omnidb--
INSERT INTO representatives VALUES('integer','sqlserver','integer','integer');--omnidb--
INSERT INTO representatives VALUES('bigint','sqlserver','bigint','bigint');--omnidb--
INSERT INTO representatives VALUES('boolean','sqlserver','char(1)','char');--omnidb--
INSERT INTO representatives VALUES('fp','sqlserver','real','real');--omnidb--
INSERT INTO representatives VALUES('datetime','firebird','timestamp','timestamp');--omnidb--
INSERT INTO representatives VALUES('datetime','mysql','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('datetime','oracle','date','date');--omnidb--
INSERT INTO representatives VALUES('datetime','sqlite','text','text');--omnidb--
INSERT INTO representatives VALUES('datetime','sqlserver','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('datetime','access','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('text','access','text','text');--omnidb--
INSERT INTO representatives VALUES('smallint','access','int','int');--omnidb--
INSERT INTO representatives VALUES('integer','access','int','int');--omnidb--
INSERT INTO representatives VALUES('bigint','access','int','int');--omnidb--
INSERT INTO representatives VALUES('fp','access','double','double');--omnidb--
INSERT INTO representatives VALUES('boolean','access','boolean','boolean');--omnidb--
INSERT INTO representatives VALUES('decimal','access','numeric','numeric');--omnidb--
INSERT INTO representatives VALUES('char','access','text','text');--omnidb--
INSERT INTO representatives VALUES('varchar','access','text','text');--omnidb--
INSERT INTO representatives VALUES('date','postgresql','date','date');--omnidb--
INSERT INTO representatives VALUES('time','postgresql','time without time zone','time without time zone');--omnidb--
INSERT INTO representatives VALUES('time','sqlite','text','text');--omnidb--
INSERT INTO representatives VALUES('date','sqlite','text','text');--omnidb--
INSERT INTO representatives VALUES('date','mysql','date','date');--omnidb--
INSERT INTO representatives VALUES('time','mysql','time','time');--omnidb--
INSERT INTO representatives VALUES('time','firebird','time','time');--omnidb--
INSERT INTO representatives VALUES('date','firebird','date','date');--omnidb--
INSERT INTO representatives VALUES('date','oracle','date','date');--omnidb--
INSERT INTO representatives VALUES('time','oracle','date','date');--omnidb--
INSERT INTO representatives VALUES('date','access','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('time','access','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('date','sqlserver','date','date');--omnidb--
INSERT INTO representatives VALUES('time','sqlserver','time','time');--omnidb--
INSERT INTO representatives VALUES('varchar','sqlce','ntext','ntext');--omnidb--
INSERT INTO representatives VALUES('char','sqlce','ntext','ntext');--omnidb--
INSERT INTO representatives VALUES('text','sqlce','ntext','ntext');--omnidb--
INSERT INTO representatives VALUES('decimal','sqlce','numeric(38,0)','numeric');--omnidb--
INSERT INTO representatives VALUES('smallint','sqlce','smallint','smallint');--omnidb--
INSERT INTO representatives VALUES('integer','sqlce','integer','integer');--omnidb--
INSERT INTO representatives VALUES('bigint','sqlce','bigint','bigint');--omnidb--
INSERT INTO representatives VALUES('boolean','sqlce','ntext','ntext');--omnidb--
INSERT INTO representatives VALUES('fp','sqlce','real','real');--omnidb--
INSERT INTO representatives VALUES('datetime','sqlce','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('date','sqlce','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('time','sqlce','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('fp','mariadb','double precision','double precision');--omnidb--
INSERT INTO representatives VALUES('smallint','mariadb','smallint','smallint');--omnidb--
INSERT INTO representatives VALUES('integer','mariadb','integer','integer');--omnidb--
INSERT INTO representatives VALUES('bigint','mariadb','bigint','bigint');--omnidb--
INSERT INTO representatives VALUES('varchar','mariadb','varchar(1000)','varchar');--omnidb--
INSERT INTO representatives VALUES('boolean','mariadb','boolean','boolean');--omnidb--
INSERT INTO representatives VALUES('decimal','mariadb','decimal(38,0)','decimal');--omnidb--
INSERT INTO representatives VALUES('char','mariadb','char(255)','char');--omnidb--
INSERT INTO representatives VALUES('text','mariadb','text','text');--omnidb--
INSERT INTO representatives VALUES('datetime','mariadb','datetime','datetime');--omnidb--
INSERT INTO representatives VALUES('date','mariadb','date','date');--omnidb--
INSERT INTO representatives VALUES('time','mariadb','time','time');--omnidb--
INSERT INTO representatives VALUES('varchar','filedb','varchar(1000)','varchar');--omnidb--

CREATE TABLE themes (
    theme_id integer not null,
    theme_name varchar(50),
    theme_type varchar(50),
    constraint pk_themes primary key (theme_id)
);--omnidb--
INSERT INTO themes VALUES(1,'omnidb','light');--omnidb--
INSERT INTO themes VALUES(2,'chrome','light');--omnidb--
INSERT INTO themes VALUES(3,'clouds','light');--omnidb--
INSERT INTO themes VALUES(4,'crimson_editor','light');--omnidb--
INSERT INTO themes VALUES(5,'dawn','light');--omnidb--
INSERT INTO themes VALUES(6,'dreamweaver','light');--omnidb--
INSERT INTO themes VALUES(7,'eclipse','light');--omnidb--
INSERT INTO themes VALUES(8,'github','light');--omnidb--
INSERT INTO themes VALUES(9,'iplastic','light');--omnidb--
INSERT INTO themes VALUES(10,'katzenmilch','light');--omnidb--
INSERT INTO themes VALUES(11,'kuroir','light');--omnidb--
INSERT INTO themes VALUES(12,'solarized_light','light');--omnidb--
INSERT INTO themes VALUES(13,'sqlserver','light');--omnidb--
INSERT INTO themes VALUES(14,'textmate','light');--omnidb--
INSERT INTO themes VALUES(15,'tomorrow','light');--omnidb--
INSERT INTO themes VALUES(16,'xcode','light');--omnidb--
INSERT INTO themes VALUES(17,'omnidb_dark','dark');--omnidb--
INSERT INTO themes VALUES(18,'ambiance','dark');--omnidb--
INSERT INTO themes VALUES(19,'chaos','dark');--omnidb--
INSERT INTO themes VALUES(20,'clouds_midnight','dark');--omnidb--
INSERT INTO themes VALUES(21,'cobalt','dark');--omnidb--
INSERT INTO themes VALUES(22,'idle_fingers','dark');--omnidb--
INSERT INTO themes VALUES(23,'kr_theme','dark');--omnidb--
INSERT INTO themes VALUES(24,'merbivore','dark');--omnidb--
INSERT INTO themes VALUES(25,'merbivore_soft','dark');--omnidb--
INSERT INTO themes VALUES(26,'mono_industrial','dark');--omnidb--
INSERT INTO themes VALUES(27,'monokai','dark');--omnidb--
INSERT INTO themes VALUES(28,'pastel_on_dark','dark');--omnidb--
INSERT INTO themes VALUES(29,'solarized_dark','dark');--omnidb--
INSERT INTO themes VALUES(30,'terminal','dark');--omnidb--
INSERT INTO themes VALUES(31,'tomorrow_night','dark');--omnidb--
INSERT INTO themes VALUES(32,'tomorrow_night_blue','dark');--omnidb--
INSERT INTO themes VALUES(33,'tomorrow_night_bright','dark');--omnidb--
INSERT INTO themes VALUES(34,'tomorrow_night_eighties','dark');--omnidb--
INSERT INTO themes VALUES(35,'twilight','dark');--omnidb--
INSERT INTO themes VALUES(36,'vibrant_ink','dark');--omnidb--

CREATE TABLE users (
    user_id integer not null,
    user_name varchar(30),
    password varchar(100),
    theme_id integer,
    editor_font_size varchar(10),
    chat_enabled integer,
    super_user integer,
    csv_encoding varchar(20),
    csv_delimiter varchar(10),
    interface_font_size text,
    constraint pk_users primary key (user_id),
    constraint users_fk_0 foreign key (theme_id) references themes (theme_id)  on update NO ACTION  on delete NO ACTION,
    constraint uq_users_0 unique (user_name)
);--omnidb--
INSERT INTO users VALUES(1,'admin','48b19163bdb02cadab1a09c9dd4eafae',1,'14',1,1,'utf-8',';','11');--omnidb--

CREATE TABLE messages (
    mes_in_code integer not null,
    mes_st_text text,
    mes_dt_timestamp text not null,
    user_id integer not null,
    mes_bo_image integer not null,
    constraint pk_messages primary key (mes_in_code),
    constraint messages_fk_0 foreign key (user_id) references users (user_id)  on update NO ACTION  on delete CASCADE
);--omnidb--

CREATE TABLE messages_users (
    mes_in_code integer not null,
    user_id integer not null,
    constraint pk_messages_users primary key (mes_in_code, user_id),
    constraint messages_users_fk_0 foreign key (mes_in_code) references messages (mes_in_code)  on update NO ACTION  on delete CASCADE,
    constraint messages_users_fk_1 foreign key (user_id) references users (user_id)  on update NO ACTION  on delete CASCADE
);--omnidb--

CREATE TABLE snippets_nodes (
    sn_id integer not null,
    sn_name text,user_id integer not null,
    sn_date_create text,
    sn_date_modify text,
    sn_id_parent integer,
    constraint pk_snippets_nodes primary key (sn_id),
    constraint fk_sn_users foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE,
    constraint fk_sn_sn foreign key (sn_id_parent) references snippets_nodes (sn_id)  on update CASCADE  on delete CASCADE
);--omnidb--

CREATE TABLE snippets_texts (
    st_id integer not null,
    st_name text,
    st_text text,
    st_date_create text,
    st_date_modify text,
    sn_id_parent integer,
    user_id integer not null,
    constraint pk_snippets_texts primary key (st_id),
    constraint fk_st_sn foreign key (sn_id_parent) references snippets_nodes (sn_id)  on update CASCADE  on delete CASCADE,
    constraint fk_st_users foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE
);--omnidb--

CREATE TABLE connections (
    conn_id integer,
    user_id integer,
    dbt_st_name varchar(40),
    server varchar(500),
    port varchar(20),
    service varchar(500),
    user varchar(100),
    alias varchar(100),
    ssh_server varchar(500),
    ssh_port varchar(20),
    ssh_user varchar(100),
    ssh_password varchar(100),
    ssh_key text,
    use_tunnel integer,
    conn_string TEXT,
    constraint pk_connections primary key (conn_id),
    constraint connections_fk_0 foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE,
    constraint connections_fk_1 foreign key (dbt_st_name) references db_type (dbt_st_name)  on update CASCADE  on delete CASCADE
);--omnidb--

CREATE TABLE conversions (
    conv_id integer,conn_id_src integer,
    conn_id_dst integer,
    conv_st_start varchar(100),
    conv_st_end varchar(100),
    conv_re_perc real,
    conv_ch_status char,
    conv_st_comments varchar(500),
    conv_st_duration varchar(100),
    user_id integer,process_id integer,
    constraint pk_conversions primary key (conv_id),
    constraint conversions_fk_0 foreign key (conn_id_src) references connections (conn_id)  on update CASCADE  on delete CASCADE,
    constraint conversions_fk_1 foreign key (conn_id_dst) references connections (conn_id)  on update CASCADE  on delete CASCADE
);--omnidb--

CREATE TABLE conv_tables_data (
    conv_id integer,
    ctd_st_table text,
    ctd_ch_droprecords char,
    ctd_ch_createtable char,
    ctd_ch_createpk char,
    ctd_ch_createfk char,
    ctd_ch_createuq char,
    ctd_ch_createidx char,
    ctd_ch_transferdata char,
    ctd_in_totalrecords integer,
    ctd_in_transfrecords integer,
    ctd_re_transfperc real,
    ctd_re_transferrate real,
    ctd_st_starttransfer text,
    ctd_st_endtransfer text,
    ctd_st_duration text,
    ctd_st_status_droprecords text,
    ctd_st_status_createtable text,
    ctd_st_status_createpk text,
    ctd_st_status_createfk text,
    ctd_st_status_createuq text,
    ctd_st_status_createidx text,
    ctd_st_status_transferdata text,
    ctd_st_transferfilter text,
    constraint pk_conv_tables_data primary key (conv_id, ctd_st_table),
    constraint conv_tables_data_fk_0 foreign key (conv_id) references conversions (conv_id)  on update CASCADE  on delete CASCADE
);--omnidb--

CREATE TABLE command_list (
    user_id integer not null,
    cl_in_codigo integer not null,
    cl_st_command text,
    cl_st_start text,
    cl_st_end text,
    cl_st_status text,
    cl_st_duration text,
    conn_id integer not null,
    constraint pk_command_list primary key (cl_in_codigo),
    constraint command_list_fk_0 foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE,
    constraint fk_cl_conn foreign key (conn_id) references connections (conn_id) on update CASCADE on delete CASCADE
);--omnidb--

CREATE TABLE tabs (
    conn_id integer not null,
    user_id integer not null,
    tab_id integer not null,
    snippet text,
    title text,
    constraint fk_tabs_conn foreign key (conn_id) references connections (conn_id)  on update CASCADE  on delete CASCADE,
    constraint fk_tabs_users foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE
);--omnidb--

CREATE TABLE mon_units (
    unit_id integer not null,
    dbt_st_name text,
    script_chart text,
    script_data text,
    type text,
    title text,
    is_default integer,
    user_id integer,
    interval integer,
    constraint pk_mon_units primary key (unit_id),
    constraint fk_mu_dbt foreign key (dbt_st_name) references db_type (dbt_st_name)  on update NO ACTION  on delete NO ACTION,
    constraint fk_mu_users foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE
);--omnidb--
INSERT INTO mon_units VALUES(1,'postgresql',replace('max_connections = connection.ExecuteScalar(''SHOW max_connections'')\n\nresult = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Backends (max_connections: " + str(max_connections) + ")"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Value"\n                },\n                "ticks": {\n                    "beginAtZero": True,\n                    "max": int(max_connections)\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\ndatabases = connection.Query(''''''\n    SELECT d.datname,\n           s.numbackends\n    FROM pg_stat_database s\n    INNER JOIN pg_database d\n    ON d.oid = s.datid\n    WHERE NOT d.datistemplate\n'''''')\n\ndatasets = []\nfor db in databases.Rows:\n    color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n    datasets.append({\n            "label": db[''datname''],\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [db["numbackends"]]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Backends',1,NULL,5);--omnidb--
INSERT INTO mon_units VALUES(2,'postgresql',replace('total_size = connection.ExecuteScalar(''''''\n    SELECT round(sum(pg_catalog.pg_database_size(datname)/1048576.0),2)\n    FROM pg_catalog.pg_database\n    WHERE NOT datistemplate\n'''''')\n\nresult = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Database Size (Total: " + str(total_size) + " MB)"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\ndatabases = connection.Query(''''''\n    SELECT datname AS datname,\n           round(pg_catalog.pg_database_size(datname)/1048576.0,2) AS size\n    FROM pg_catalog.pg_database\n    WHERE NOT datistemplate\n    ORDER BY\n        CASE WHEN pg_catalog.has_database_privilege(datname, ''CONNECT'')\n             THEN pg_catalog.pg_database_size(datname)\n             ELSE NULL\n        END DESC\n'''''')\n\ndatasets = []\nfor db in databases.Rows:\n    color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n    datasets.append({\n            "label": db[''datname''],\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [db["size"]]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Database Size',1,NULL,30);--omnidb--
INSERT INTO mon_units VALUES(3,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Size: Top 5 Tables"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\ntables = connection.Query(''''''\n    SELECT nspname || ''.'' || relname AS relation,\n           round(pg_relation_size(c.oid)/1048576.0,2) AS size\n    FROM pg_class c\n    LEFT JOIN pg_namespace n ON (n.oid = c.relnamespace)\n    WHERE nspname NOT IN (''pg_catalog'', ''information_schema'')\n      AND c.relkind <> ''i''\n      AND nspname !~ ''^pg_toast''\n    ORDER BY pg_total_relation_size(c.oid) DESC\n    LIMIT 5\n'''''')\n\ndatasets = []\nfor table in tables.Rows:\n    color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n    datasets.append({\n            "label": table[''relation''],\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [table["size"]]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Size: Top 5 Tables',1,NULL,15);--omnidb--
INSERT INTO mon_units VALUES(4,'postgresql','',replace('from datetime import datetime\n\ndata = connection.Query(''''''\n    SELECT *\n    FROM pg_stat_activity\n'''''')\n\nresult = {\n    "columns": data.Columns,\n    "data": data.Rows\n}\n','\n',char(10)),'grid','Activity',1,NULL,15);--omnidb--
INSERT INTO mon_units VALUES(5,'postgresql','',replace('from datetime import datetime\n\ndata = connection.Query(''''''\n    SELECT z.current_database,z.schemaname,z.tablename, pg_size_pretty(sum_wasted) AS total_bloat\n    FROM (\n    SELECT y.schemaname, y.tablename, y.current_database, sum(wastedbytes+wastedibytes)::bigint AS sum_wasted\n    FROM (\n    SELECT current_database,schemaname, tablename, tbloat, wastedbytes, iname, ibloat, wastedibytes AS wastedibytes\n    FROM (\n    SELECT\n      current_database(), schemaname, tablename, /*reltuples::bigint, relpages::bigint, otta,*/\n      ROUND((CASE WHEN otta=0 THEN 0.0 ELSE sml.relpages::FLOAT/otta END)::NUMERIC,1) AS tbloat,\n      CASE WHEN relpages < otta THEN 0 ELSE bs*(sml.relpages-otta)::BIGINT END AS wastedbytes,\n      iname, /*ituples::bigint, ipages::bigint, iotta,*/\n      ROUND((CASE WHEN iotta=0 OR ipages=0 THEN 0.0 ELSE ipages::FLOAT/iotta END)::NUMERIC,1) AS ibloat,\n      CASE WHEN ipages < iotta THEN 0 ELSE bs*(ipages-iotta) END AS wastedibytes\n    FROM (\n      SELECT\n        schemaname, tablename, cc.reltuples, cc.relpages, bs,\n        CEIL((cc.reltuples*((datahdr+ma-\n          (CASE WHEN datahdr%ma=0 THEN ma ELSE datahdr%ma END))+nullhdr2+4))/(bs-20::FLOAT)) AS otta,\n        COALESCE(c2.relname,''?'') AS iname, COALESCE(c2.reltuples,0) AS ituples, COALESCE(c2.relpages,0) AS ipages,\n        COALESCE(CEIL((c2.reltuples*(datahdr-12))/(bs-20::FLOAT)),0) AS iotta -- very rough approximation, assumes all cols\n      FROM (\n        SELECT\n          ma,bs,schemaname,tablename,\n          (datawidth+(hdr+ma-(CASE WHEN hdr%ma=0 THEN ma ELSE hdr%ma END)))::NUMERIC AS datahdr,\n          (maxfracsum*(nullhdr+ma-(CASE WHEN nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2\n        FROM (\n          SELECT\n            schemaname, tablename, hdr, ma, bs,\n            SUM((1-null_frac)*avg_width) AS datawidth,\n            MAX(null_frac) AS maxfracsum,\n            hdr+(\n              SELECT 1+COUNT(*)/8\n              FROM pg_stats s2\n              WHERE null_frac<>0 AND s2.schemaname = s.schemaname AND s2.tablename = s.tablename\n            ) AS nullhdr\n          FROM pg_stats s, (\n            SELECT\n              (SELECT current_setting(''block_size'')::NUMERIC) AS bs,\n              CASE WHEN SUBSTRING(v,12,3) IN (''8.0'',''8.1'',''8.2'') THEN 27 ELSE 23 END AS hdr,\n              CASE WHEN v ~ ''mingw32'' THEN 8 ELSE 4 END AS ma\n            FROM (SELECT version() AS v) AS foo\n          ) AS constants\n          GROUP BY 1,2,3,4,5\n        ) AS foo\n      ) AS rs\n      JOIN pg_class cc ON cc.relname = rs.tablename\n      JOIN pg_namespace nn ON cc.relnamespace = nn.oid AND nn.nspname = rs.schemaname AND nn.nspname <> ''information_schema''\n      LEFT JOIN pg_index i ON indrelid = cc.oid\n      LEFT JOIN pg_class c2 ON c2.oid = i.indexrelid\n    ) AS sml) x) y\n    GROUP BY y.schemaname, y.tablename, y.current_database) z\n    ORDER BY z.sum_wasted DESC\n    LIMIT 20\n'''''')\n\nresult = {\n    "columns": data.Columns,\n    "data": data.Rows\n}','\n',char(10)),'grid','Bloat: Top 20 Tables',0,NULL,30);--omnidb--
INSERT INTO mon_units VALUES(6,'postgresql',replace('max_connections = connection.ExecuteScalar(''SHOW max_connections'')\n\nresult = {\n    "type": "pie",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Backends (max_connections: " + str(max_connections) + ")"\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\ndatabases = connection.Query(''''''\n    SELECT d.datname,\n           s.numbackends\n    FROM pg_stat_database s\n    INNER JOIN pg_database d\n    ON d.oid = s.datid\n    WHERE NOT d.datistemplate\n'''''')\n\ndata = []\ncolor = []\nlabel = []\n\nfor db in databases.Rows:\n    data.append(db["numbackends"])\n    color.append("rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")")\n    label.append(db["datname"])\n\nresult = {\n    "labels": label,\n    "datasets": [\n        {\n            "data": data,\n            "backgroundColor": color,\n            "label": "Dataset 1"\n        }\n    ]\n}\n','\n',char(10)),'chart','Backends',1,NULL,15);--omnidb--
INSERT INTO mon_units VALUES(7,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"CPU Usage"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Value",\n                },\n                "ticks": {\n                    "beginAtZero": True,\n                    "max": 100\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\ncpu_data = connection.Query(''''''\n    create temporary table tabela (c1 text);\n    copy tabela from program ''mpstat -P ALL 1 1 | grep "Average:" | tail -n +2 | tr -s " " | cut -f2,3 -d" "'';\n    select * from tabela;\n'''''')\n\ndatasets = []\nfor cpu in cpu_data.Rows:\n    if cpu!='''':\n        cpu_split = cpu[0].split('' '')\n        color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n        datasets.append({\n            "label": cpu_split[0],\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [cpu_split[1]]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','CPU Usage',1,NULL,10);--omnidb--
INSERT INTO mon_units VALUES(8,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Locks"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Num locks"\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\nlocks = connection.Query(''''''\n    SELECT mode,\n           count(*) as count\n    FROM pg_locks\n    GROUP BY mode\n'''''')\n\ndatasets = []\nfor lock in locks.Rows:\n    color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n    datasets.append({\n            "label": lock[''mode''],\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [lock["count"]]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Locks',1,NULL,15);--omnidb--
INSERT INTO mon_units VALUES(9,'postgresql','',replace('data = connection.Query(''''''\n    SELECT pg_is_in_recovery() as "In Recovery"\n'''''')\n\nresult = {\n    "columns": data.Columns,\n    "data": data.Rows\n}','\n',char(10)),'grid','In Recovery',0,NULL,120);--omnidb--
INSERT INTO mon_units VALUES(10,'postgresql',replace('total_size = connection.ExecuteScalar(''''''\n    SELECT round(sum(pg_catalog.pg_database_size(datname)/1048576.0),2)\n    FROM pg_catalog.pg_database\n    WHERE NOT datistemplate\n'''''')\n\nresult = {\n    "type": "pie",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Database Size (Total: " + str(total_size) + " MB)"\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\ndatabases = connection.Query(''''''\n    SELECT d.datname AS datname,\n           round(pg_catalog.pg_database_size(d.datname)/1048576.0,2) AS size\n    FROM pg_catalog.pg_database d\n    WHERE d.datname not in (''template0'',''template1'')\n'''''')\n\ndata = []\ncolor = []\nlabel = []\n\nfor db in databases.Rows:\n    data.append(db["size"])\n    color.append("rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")")\n    label.append(db["datname"])\n\nresult = {\n    "labels": label,\n    "datasets": [\n        {\n            "data": data,\n            "backgroundColor": color,\n            "label": "Dataset 1"\n        }\n    ]\n}\n','\n',char(10)),'chart','Database Size',0,NULL,30);--omnidb--
INSERT INTO mon_units VALUES(11,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Bloat: Top 5 Tables"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\ntables = connection.Query(''''''\n    SELECT z.schemaname || ''.'' || z.tablename as relation, sum_wasted/1048576.0 AS size\n    FROM (\n    SELECT y.schemaname, y.tablename, y.current_database, wastedbytes + sum(wastedibytes)::bigint AS sum_wasted\n    FROM (\n    SELECT current_database,schemaname, tablename, tbloat, wastedbytes, iname, ibloat, wastedibytes AS wastedibytes\n    FROM (\n    SELECT\n      current_database(), schemaname, tablename, /*reltuples::bigint, relpages::bigint, otta,*/\n      ROUND((CASE WHEN otta=0 THEN 0.0 ELSE sml.relpages::FLOAT/otta END)::NUMERIC,1) AS tbloat,\n      CASE WHEN relpages < otta THEN 0 ELSE bs*(sml.relpages-otta)::BIGINT END AS wastedbytes,\n      iname, /*ituples::bigint, ipages::bigint, iotta,*/\n      ROUND((CASE WHEN iotta=0 OR ipages=0 THEN 0.0 ELSE ipages::FLOAT/iotta END)::NUMERIC,1) AS ibloat,\n      CASE WHEN ipages < iotta THEN 0 ELSE bs*(ipages-iotta) END AS wastedibytes\n    FROM (\n      SELECT\n        schemaname, tablename, cc.reltuples, cc.relpages, bs,\n        CEIL((cc.reltuples*((datahdr+ma-\n          (CASE WHEN datahdr%ma=0 THEN ma ELSE datahdr%ma END))+nullhdr2+4))/(bs-20::FLOAT)) AS otta,\n        COALESCE(c2.relname,''?'') AS iname, COALESCE(c2.reltuples,0) AS ituples, COALESCE(c2.relpages,0) AS ipages,\n        COALESCE(CEIL((c2.reltuples*(datahdr-12))/(bs-20::FLOAT)),0) AS iotta -- very rough approximation, assumes all cols\n      FROM (\n        SELECT\n          ma,bs,schemaname,tablename,\n          (datawidth+(hdr+ma-(CASE WHEN hdr%ma=0 THEN ma ELSE hdr%ma END)))::NUMERIC AS datahdr,\n          (maxfracsum*(nullhdr+ma-(CASE WHEN nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2\n        FROM (\n          SELECT\n            schemaname, tablename, hdr, ma, bs,\n            SUM((1-null_frac)*avg_width) AS datawidth,\n            MAX(null_frac) AS maxfracsum,\n            hdr+(\n              SELECT 1+COUNT(*)/8\n              FROM pg_stats s2\n              WHERE null_frac<>0 AND s2.schemaname = s.schemaname AND s2.tablename = s.tablename\n            ) AS nullhdr\n          FROM pg_stats s, (\n            SELECT\n              (SELECT current_setting(''block_size'')::NUMERIC) AS bs,\n              CASE WHEN SUBSTRING(v,12,3) IN (''8.0'',''8.1'',''8.2'') THEN 27 ELSE 23 END AS hdr,\n              CASE WHEN v ~ ''mingw32'' THEN 8 ELSE 4 END AS ma\n            FROM (SELECT version() AS v) AS foo\n          ) AS constants\n          GROUP BY 1,2,3,4,5\n        ) AS foo\n      ) AS rs\n      JOIN pg_class cc ON cc.relname = rs.tablename\n      JOIN pg_namespace nn ON cc.relnamespace = nn.oid AND nn.nspname = rs.schemaname AND nn.nspname <> ''information_schema''\n      LEFT JOIN pg_index i ON indrelid = cc.oid\n      LEFT JOIN pg_class c2 ON c2.oid = i.indexrelid\n    ) AS sml) x) y\n    GROUP BY y.schemaname, y.tablename, y.current_database, y.wastedbytes) z\n    ORDER BY z.sum_wasted DESC\n    LIMIT 5\n'''''')\n\ndatasets = []\nfor table in tables.Rows:\n    color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n    datasets.append({\n            "label": table[''relation''],\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [table["size"]]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Bloat: Top 5 Tables',0,NULL,45);--omnidb--
INSERT INTO mon_units VALUES(12,'postgresql','',replace('from datetime import datetime\n\ndata = connection.Query(''''''\n    SELECT relname as table_name,\n           pg_size_pretty(pg_table_size(oid)) as table_size,\n           age(relfrozenxid) as xid_age,\n           current_setting(''autovacuum_freeze_max_age'')::integer as max_age,\n           round(age(relfrozenxid)/(current_setting(''autovacuum_freeze_max_age'')::integer)::numeric*100.0,4) as perc\n    FROM pg_class\n    WHERE relkind in (''r'', ''t'')\n    ORDER BY age(relfrozenxid) DESC\n    LIMIT 20;\n'''''')\n\nresult = {\n    "columns": data.Columns,\n    "data": data.Rows\n}\n','\n',char(10)),'grid','AutovacFreeze: Top 20 Tables',0,NULL,60);--omnidb--
INSERT INTO mon_units VALUES(13,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Master: Replication Lag"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                },\n                "ticks": {\n                    "beginAtZero": True\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\nreplags = connection.Query(''''''\n    CREATE TEMPORARY TABLE omnidb_monitor_result (result1 TEXT, result2 TEXT);\n    DO $$\n    BEGIN\n        IF current_setting(''server_version_num'')::integer < 100000 THEN\n            EXECUTE ''INSERT INTO omnidb_monitor_result SELECT client_addr || ''''-'''' || application_name as standby,''\n                    ''round(pg_xlog_location_diff(pg_current_xlog_location(),replay_location)/1048576.0,2) as lag ''\n                    ''FROM pg_stat_replication'';\n        ELSE\n            EXECUTE ''INSERT INTO omnidb_monitor_result SELECT client_addr || ''''-'''' || application_name as standby,''\n                ''round(pg_wal_lsn_diff(pg_current_wal_lsn(),replay_lsn)/1048576.0,2) as lag ''\n                ''FROM pg_stat_replication'';\n        END IF;\n    END$$;\n    SELECT result1 as standby, result2 as lag FROM omnidb_monitor_result;\n'''''')\n\ndatasets = []\nfor replag in replags.Rows:\n    color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n    datasets.append({\n            "label": replag[''standby''],\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [replag[''lag'']]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Master: Replication Lag',0,NULL,15);--omnidb--
INSERT INTO mon_units VALUES(14,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Standby: Replication Lag (Size)"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                },\n                "ticks": {\n                    "beginAtZero": True\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\nreplags = connection.Query(''''''\n    CREATE TEMPORARY TABLE omnidb_monitor_result (result TEXT);\n    DO $$DECLARE r record;\n    BEGIN\n        IF current_setting(''server_version_num'')::integer < 100000 THEN\n            EXECUTE ''INSERT INTO omnidb_monitor_result ''\n                    ''SELECT round(pg_xlog_location_diff(pg_last_xlog_receive_location(), pg_last_xlog_replay_location())/1048576.0,2) AS lag'';\n        ELSE\n            EXECUTE ''INSERT INTO omnidb_monitor_result ''\n                    ''SELECT round(pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn())/1048576.0,2) AS lag'';\n        END IF;\n    END$$;\n    SELECT result as lag FROM omnidb_monitor_result;\n'''''')\n\ndatasets = []\nfor replag in replags.Rows:\n    color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n    datasets.append({\n            "label": "Lag",\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [replag[''lag'']]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Standby: Replication Lag (Size)',0,NULL,15);--omnidb--
INSERT INTO mon_units VALUES(15,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Standby: Replication Lag (Time)"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Seconds"\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\nreplags = connection.Query(''''''\n    SELECT COALESCE(ROUND(EXTRACT(epoch FROM now() - pg_last_xact_replay_timestamp())),0) AS lag\n'''''')\n\ndatasets = []\nfor replag in replags.Rows:\n    color = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\n    datasets.append({\n            "label": "Lag",\n            "fill": False,\n            "backgroundColor": color,\n            "borderColor": color,\n            "lineTension": 0,\n            "pointRadius": 1,\n            "borderWidth": 1,\n            "data": [replag[''lag'']]\n        })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Standby: Replication Lag (Time)',0,NULL,15);--omnidb--
INSERT INTO mon_units VALUES(16,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"System Memory Usage (Total: " + total_mem + "MB)"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "%",\n                },\n                "ticks": {\n                    "beginAtZero": True,\n                    "max": 100\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\nmem_data = connection.ExecuteScalar(''''''\n    create temporary table tabela (c1 text);\n    copy tabela from program ''free -m | tail -n +2 | head -n 1 | tr -s " " | cut -f2,3,4 -d " "'';\n    select * from tabela;\n'''''')\n\ndatasets = []\nmem_split = mem_data.split('' '')\ntotal_mem = mem_split[0]\nused_mem = mem_split[1]\nfree_mem = mem_split[2]\nperc_mem = round(int(used_mem)*100/int(total_mem),2)\ncolor = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\ndatasets.append({\n        "label": "Memory",\n        "fill": False,\n        "backgroundColor": color,\n        "borderColor": color,\n        "lineTension": 0,\n        "pointRadius": 1,\n        "borderWidth": 1,\n        "data": [perc_mem]\n    })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Memory Usage',1,NULL,10);--omnidb--
INSERT INTO mon_units VALUES(17,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "legend": {\n            "display": False\n        },\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Longest Active Query"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Duration(s)"\n                },\n                "ticks": {\n                    "beginAtZero": True\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\nduration = connection.ExecuteScalar(''''''\n    SELECT duration FROM\n    (SELECT EXTRACT(EPOCH FROM(now() - query_start))::INTEGER AS duration FROM pg_stat_activity WHERE state=''active''\n    UNION ALL\n    SELECT 0) t\n    WHERE duration is NOT NULL\n    ORDER BY duration DESC\n    LIMIT 1\n'''''')\n\ndatasets = []\ncolor = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\ndatasets.append({\n        "label": ''Query'',\n        "fill": False,\n        "backgroundColor": color,\n        "borderColor": color,\n        "lineTension": 0,\n        "pointRadius": 1,\n        "borderWidth": 1,\n        "data": [duration]\n    })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','Longest Active Query',0,NULL,5);--omnidb--
INSERT INTO mon_units VALUES(18,'postgresql',replace('result = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "legend": {\n            "display": False\n        },\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"WAL Folder Size"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size(MB)"\n                },\n                "ticks": {\n                    "beginAtZero": True\n                }\n            }]\n        }\n    }\n}\n','\n',char(10)),replace('from datetime import datetime\nfrom random import randint\n\nsize = connection.ExecuteScalar(''''''\n    CREATE TEMPORARY TABLE omnidb_temp (c1 TEXT, c2 TEXT);\n    COPY omnidb_temp FROM PROGRAM ''du -s pg_xlog || du -s pg_wal'';\n    SELECT ROUND(c1::BIGINT/1048576.0,2) AS pg_xlog_size FROM omnidb_temp;\n'''''')\n\ndatasets = []\ncolor = "rgb(" + str(randint(125, 225)) + "," + str(randint(125, 225)) + "," + str(randint(125, 225)) + ")"\ndatasets.append({\n        "label": ''WAL Folder Size'',\n        "fill": False,\n        "backgroundColor": color,\n        "borderColor": color,\n        "lineTension": 0,\n        "pointRadius": 1,\n        "borderWidth": 1,\n        "data": [size]\n    })\n\nresult = {\n    "labels": [datetime.now().strftime(''%H:%M:%S'')],\n    "datasets": datasets\n}\n','\n',char(10)),'chart_append','WAL Folder Size',0,NULL,30);--omnidb--

CREATE TABLE units_users_connections (
    uuc_id integer not null,
    unit_id integer not null,
    user_id integer not null,
    conn_id integer not null,
    interval integer not null,
    plugin_name text,
    constraint pk_units_users_connections primary key (uuc_id),
    constraint units_users_connections_fk_0 foreign key (conn_id) references connections (conn_id) on update CASCADE on delete CASCADE,
    constraint units_users_connections_fk_1 foreign key (user_id) references users (user_id) on update CASCADE on delete CASCADE
);--omnidb--

CREATE TABLE shortcuts (
    user_id integer,
    shortcut_code text,
    ctrl_pressed integer,
    shift_pressed integer,
    alt_pressed integer,
    meta_pressed integer,
    shortcut_key text,
    constraint pk_shortcuts primary key (user_id, shortcut_code),
    constraint fk_shortcuts_users foreign key (user_id) references users (user_id) on update CASCADE on delete CASCADE
);--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_analyze',0,0,1,0,'S');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_explain',0,0,1,0,'A');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_indent',0,0,1,0,'D');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_left_inner_tab',1,0,0,0,',');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_left_outer_tab',0,0,1,0,',');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_new_inner_tab',1,0,0,0,'INSERT');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_new_outer_tab',0,0,1,0,'INSERT');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_remove_inner_tab',1,0,0,0,'END');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_remove_outer_tab',0,0,1,0,'END');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_right_inner_tab',1,0,0,0,'.');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_run_query',0,0,1,0,'Q');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_right_outer_tab',0,0,1,0,'.');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_cancel_query',0,0,1,0,'C');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_next_console_command',1,0,0,0,'ARROWDOWN');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_previous_console_command',1,0,0,0,'ARROWUP');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_autocomplete',1,0,0,0,'SPACE');--omnidb--

CREATE TABLE console_history (
    user_id integer,
    conn_id integer,
    command_text text,
    command_date text,
    constraint fk_ch_users foreign key (user_id) references users (user_id) on update CASCADE on delete CASCADE,
    constraint fk_ch_conn foreign key (conn_id) references connections (conn_id) on update CASCADE on delete CASCADE
);--omnidb--

CREATE TABLE cgroups (
  cgroup_id integer primary key,
  user_id integer references users (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
  cgroup_name text
);--omnidb--

CREATE TABLE cgroups_connections (
  cgroup_id integer references cgroups (cgroup_id) ON UPDATE CASCADE ON DELETE CASCADE,
  conn_id integer references connections (conn_id) ON UPDATE CASCADE ON DELETE CASCADE,
  primary key (cgroup_id, conn_id)
);--omnidb--

CREATE TABLE version (
    ver_id text not null,
    constraint pk_versions primary key (ver_id)
);--omnidb--
INSERT INTO version VALUES('2.14.0');--omnidb--
