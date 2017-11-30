CREATE TABLE db_type (
    dbt_st_name varchar(40),
    dbt_in_enabled integer,
    constraint pk_db_type primary key (dbt_st_name)
);--omnidb--
INSERT INTO db_type VALUES('sqlite',0);--omnidb--
INSERT INTO db_type VALUES('mysql',0);--omnidb--
INSERT INTO db_type VALUES('postgresql',1);--omnidb--
INSERT INTO db_type VALUES('firebird',0);--omnidb--
INSERT INTO db_type VALUES('oracle',0);--omnidb--
INSERT INTO db_type VALUES('sqlserver',0);--omnidb--
INSERT INTO db_type VALUES('access',0);--omnidb--
INSERT INTO db_type VALUES('sqlce',0);--omnidb--
INSERT INTO db_type VALUES('mariadb',0);--omnidb--
INSERT INTO db_type VALUES('filedb',0);--omnidb--

CREATE TABLE data_categories (
    cat_st_name varchar(40),
    cat_st_description varchar(100),
    cat_st_class varchar(40),
    constraint pk_data_categories primary key (cat_st_name)
);--omnidb--
INSERT INTO data_categories VALUES('bigint','Big Integer','numeric');--omnidb--
INSERT INTO data_categories VALUES('boolean','Boolean','text');--omnidb--
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

CREATE TABLE users (user_id integer not null,
    user_name varchar(30),
    password varchar(100),
    theme_id integer,
    editor_font_size varchar(10),
    chat_enabled integer,
    super_user integer,
    user_key text,
    constraint pk_users primary key (user_id),
    constraint users_fk_0 foreign key (theme_id) references themes (theme_id)  on update NO ACTION  on delete NO ACTION,
    constraint uq_users_0 unique (user_name)
);--omnidb--
INSERT INTO users VALUES(1,'admin','8IqxKdQ=',1,'14',1,1,'0c4a137f-9918-4c0b-af45-480deef6f760');--omnidb--

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

CREATE TABLE connections (conn_id integer,
    user_id integer,
    dbt_st_name varchar(40),
    server varchar(500),
    port varchar(20),
    service varchar(500),
    user varchar(100),
    password varchar(100),
    alias varchar(100),
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
    cl_st_mode text,
    cl_st_status text,
    cl_st_duration text,
    constraint pk_command_list primary key (cl_in_codigo),
    constraint command_list_fk_0 foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE
);--omnidb--

CREATE TABLE tabs (
    conn_id integer not null,
    user_id integer not null,
    tab_id integer not null,
    snippet text,
    constraint fk_tabs_conn foreign key (conn_id) references connections (conn_id)  on update CASCADE  on delete CASCADE,
    constraint fk_tabs_users foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE
);--omnidb--

CREATE TABLE mon_units (
    unit_id integer not null,
    dbt_st_name text,
    script text,
    type text,
    title text,
    append integer,
    is_default integer,
    user_id integer,
    constraint pk_mon_units primary key (unit_id),
    constraint fk_mu_dbt foreign key (dbt_st_name) references db_type (dbt_st_name)  on update NO ACTION  on delete NO ACTION,
    constraint fk_mu_users foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE
);--omnidb--
INSERT INTO mon_units VALUES(1,'postgresql',replace('from datetime import datetime\n\ndatabases = connection.Query(''''''select datname, numbackends, now() as time from pg_stat_database where datname not in (''template0'',''template1'')'''''')\n\nmax_connections = connection.ExecuteScalar(''show max_connections'')\n\ncolors = [\n"rgb(255, 99, 132)",\n"rgb(255, 159, 64)",\n"rgb(255, 205, 86)",\n"rgb(75, 192, 192)",\n"rgb(54, 162, 235)",\n"rgb(153, 102, 255)",\n"rgb(201, 203, 207)"]\n\ndatasets = []\ncolor_index = 0\nfor db in databases.Rows:\n    datasets.append({\n            "label": db[''datname''],\n            "fill": False,\n            "backgroundColor": colors[color_index],\n            "borderColor": colors[color_index],\n            "lineTension": 0,\n            "pointRadius": 2,\n            "borderWidth": 1,\n            "data": [db["numbackends"]]\n        })\n    color_index = color_index + 1\n    if color_index == len(colors):\n        color_index = 0\n\noptions = {\n    "type": "line",\n    "data": {\n        "labels": [datetime.now().strftime(''%H:%M:%S'')],\n        "datasets": datasets\n    },\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Backends (max_connections: " + str(max_connections) + ")"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Value"\n                },\n                "ticks": {\n                    "beginAtZero": True,\n                    "max": int(max_connections)\n                }\n            }]\n        }\n    }\n}\n\nresult = options','\n',char(10)),'chart_append','Backends',1,1,NULL);--omnidb--
INSERT INTO mon_units VALUES(2,'postgresql',replace('from datetime import datetime\n\ndatabases = connection.Query(''''''\nSELECT d.datname AS datname,  \n    round(pg_catalog.pg_database_size(d.datname)/1048576.0,2) as size\nFROM pg_catalog.pg_database d\nWHERE d.datname not in (''template0'',''template1'')\nORDER BY\nCASE WHEN pg_catalog.has_database_privilege(d.datname, ''CONNECT'')\n    THEN pg_catalog.pg_database_size(d.datname)\n    ELSE NULL\nEND DESC\n'''''')\n\ncolors = [\n"rgb(255, 99, 132)",\n"rgb(255, 159, 64)",\n"rgb(255, 205, 86)",\n"rgb(75, 192, 192)",\n"rgb(54, 162, 235)",\n"rgb(153, 102, 255)",\n"rgb(201, 203, 207)"]\n\ndatasets = []\ncolor_index = 0\nfor db in databases.Rows:\n    datasets.append({\n            "label": db[''datname''],\n            "fill": False,\n            "backgroundColor": colors[color_index],\n            "borderColor": colors[color_index],\n            "lineTension": 0,\n            "pointRadius": 2,\n            "borderWidth": 1,\n            "data": [db["size"]]\n        })\n    color_index = color_index + 1\n    if color_index == len(colors):\n        color_index = 0\n\noptions = {\n    "type": "line",\n    "data": {\n        "labels": [datetime.now().strftime(''%H:%M:%S'')],\n        "datasets": datasets\n    },\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Database size"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                }\n            }]\n        }\n    }\n}\n\nresult = options','\n',char(10)),'chart_append','Database size',1,1,NULL);--omnidb--
INSERT INTO mon_units VALUES(3,'postgresql',replace('from datetime import datetime\n\ntables = connection.Query(''''''\nSELECT nspname || ''.'' || relname AS relation,\n    round(pg_relation_size(C.oid)/1048576.0,2) AS size\n  FROM pg_class C\n  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)\n  WHERE nspname NOT IN (''pg_catalog'', ''information_schema'')\n    AND C.relkind <> ''i''\n    AND nspname !~ ''^pg_toast''\n  ORDER BY pg_total_relation_size(C.oid) DESC\n  LIMIT 5\n'''''')\n\ncolors = [\n"rgb(255, 99, 132)",\n"rgb(255, 159, 64)",\n"rgb(255, 205, 86)",\n"rgb(75, 192, 192)",\n"rgb(54, 162, 235)",\n"rgb(153, 102, 255)",\n"rgb(201, 203, 207)"]\n\ndatasets = []\ncolor_index = 0\nfor table in tables.Rows:\n    datasets.append({\n            "label": table[''relation''],\n            "fill": False,\n            "backgroundColor": colors[color_index],\n            "borderColor": colors[color_index],\n            "lineTension": 0,\n            "pointRadius": 2,\n            "borderWidth": 1,\n            "data": [table["size"]]\n        })\n    color_index = color_index + 1\n    if color_index == len(colors):\n        color_index = 0\n\noptions = {\n    "type": "line",\n    "data": {\n        "labels": [datetime.now().strftime(''%H:%M:%S'')],\n        "datasets": datasets\n    },\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Top 5 tables in size"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                }\n            }]\n        }\n    }\n}\n\nresult = options','\n',char(10)),'chart_append','Top 5 tables in size',1,0,NULL);--omnidb--
INSERT INTO mon_units VALUES(4,'postgresql',replace('from datetime import datetime\nfrom random import *\n\ndata = connection.Query(''''''\nselect * from pg_stat_activity\n'''''')\n\nreturn_data = {\n    "columns": data.Columns,\n    "data": data.Rows\n}\n\nresult = return_data','\n',char(10)),'grid','Backends',0,0,NULL);--omnidb--
INSERT INTO mon_units VALUES(5,'postgresql',replace('from datetime import datetime\nfrom random import *\n\ndata = connection.Query(''''''\nSELECT\n  current_database(), schemaname, tablename, /*reltuples::bigint, relpages::bigint, otta,*/\n  ROUND((CASE WHEN otta=0 THEN 0.0 ELSE sml.relpages::FLOAT/otta END)::NUMERIC,1) AS tbloat,\n  CASE WHEN relpages < otta THEN 0 ELSE bs*(sml.relpages-otta)::BIGINT END AS wastedbytes,\n  iname, /*ituples::bigint, ipages::bigint, iotta,*/\n  ROUND((CASE WHEN iotta=0 OR ipages=0 THEN 0.0 ELSE ipages::FLOAT/iotta END)::NUMERIC,1) AS ibloat,\n  CASE WHEN ipages < iotta THEN 0 ELSE bs*(ipages-iotta) END AS wastedibytes\nFROM (\n  SELECT\n    schemaname, tablename, cc.reltuples, cc.relpages, bs,\n    CEIL((cc.reltuples*((datahdr+ma-\n      (CASE WHEN datahdr%ma=0 THEN ma ELSE datahdr%ma END))+nullhdr2+4))/(bs-20::FLOAT)) AS otta,\n    COALESCE(c2.relname,''?'') AS iname, COALESCE(c2.reltuples,0) AS ituples, COALESCE(c2.relpages,0) AS ipages,\n    COALESCE(CEIL((c2.reltuples*(datahdr-12))/(bs-20::FLOAT)),0) AS iotta -- very rough approximation, assumes all cols\n  FROM (\n    SELECT\n      ma,bs,schemaname,tablename,\n      (datawidth+(hdr+ma-(CASE WHEN hdr%ma=0 THEN ma ELSE hdr%ma END)))::NUMERIC AS datahdr,\n      (maxfracsum*(nullhdr+ma-(CASE WHEN nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2\n    FROM (\n      SELECT\n        schemaname, tablename, hdr, ma, bs,\n        SUM((1-null_frac)*avg_width) AS datawidth,\n        MAX(null_frac) AS maxfracsum,\n        hdr+(\n          SELECT 1+COUNT(*)/8\n          FROM pg_stats s2\n          WHERE null_frac<>0 AND s2.schemaname = s.schemaname AND s2.tablename = s.tablename\n        ) AS nullhdr\n      FROM pg_stats s, (\n        SELECT\n          (SELECT current_setting(''block_size'')::NUMERIC) AS bs,\n          CASE WHEN SUBSTRING(v,12,3) IN (''8.0'',''8.1'',''8.2'') THEN 27 ELSE 23 END AS hdr,\n          CASE WHEN v ~ ''mingw32'' THEN 8 ELSE 4 END AS ma\n        FROM (SELECT version() AS v) AS foo\n      ) AS constants\n      GROUP BY 1,2,3,4,5\n    ) AS foo\n  ) AS rs\n  JOIN pg_class cc ON cc.relname = rs.tablename\n  JOIN pg_namespace nn ON cc.relnamespace = nn.oid AND nn.nspname = rs.schemaname AND nn.nspname <> ''information_schema''\n  LEFT JOIN pg_index i ON indrelid = cc.oid\n  LEFT JOIN pg_class c2 ON c2.oid = i.indexrelid\n) AS sml\nORDER BY wastedbytes DESC\n'''''')\n\nreturn_data = {\n    "columns": data.Columns,\n    "data": data.Rows\n}\n\nresult = return_data','\n',char(10)),'grid','Table bloat',0,0,NULL);--omnidb--
INSERT INTO mon_units VALUES(6,'postgresql',replace('from datetime import datetime\n\ndatabases = connection.Query(''''''select datname, numbackends from pg_stat_database where datname not in (''template0'',''template1'')'''''')\n\nmax_connections = connection.ExecuteScalar(''show max_connections'')\n\ncolors = [\n"rgb(255, 99, 132)",\n"rgb(255, 159, 64)",\n"rgb(255, 205, 86)",\n"rgb(75, 192, 192)",\n"rgb(54, 162, 235)",\n"rgb(153, 102, 255)",\n"rgb(201, 203, 207)"]\n\ndata = []\ncolor = []\nlabel = []\n\ncolor_index = 0\n\nfor db in databases.Rows:\n    data.append(db["numbackends"])\n    color.append(colors[color_index])\n    label.append(db["datname"])\n    color_index = color_index + 1\n    if color_index == len(colors):\n        color_index = 0\n\noptions = {\n    "type": "pie",\n    "data": {\n        "labels": label,\n        "datasets": [\n            {\n                "data": data,\n                "backgroundColor": color,\n                "label": "Dataset 1"\n            }\n        ]\n    },\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Backends (max_connections: " + str(max_connections) + ")"\n        }\n    }\n}\n\nresult = options','\n',char(10)),'chart','Backends',0,0,NULL);--omnidb--
INSERT INTO mon_units VALUES(7,'postgresql',replace('from datetime import datetime\012\012cpu_data = connection.ExecuteScalar(''''''\012create temporary table omnidb_monitor_result (result text);\012DO LANGUAGE plpythonu\012$$\012import sys\012import StringIO\012import subprocess\012codeOut = StringIO.StringIO()\012codeErr = StringIO.StringIO()\012sys.stdout = codeOut\012sys.stderr = codeErr\012print subprocess.Popen("mpstat -P ALL 1 1 | grep ''Average:'' | tail -n +2 | tr -s '' '' | cut -f2,3 -d'' ''", shell=True, stdout=subprocess.PIPE).stdout.read()\012sys.stdout = sys.__stdout__\012sys.stderr = sys.__stderr__\012result = codeOut.getvalue()\012plpy.execute("insert into omnidb_monitor_result values (''{0}'')".format(result))\012$$;\012select * from omnidb_monitor_result;\012'''''')\012\012colors = [\012"rgb(255, 99, 132)",\012"rgb(255, 159, 64)",\012"rgb(255, 205, 86)",\012"rgb(75, 192, 192)",\012"rgb(54, 162, 235)",\012"rgb(153, 102, 255)",\012"rgb(201, 203, 207)"]\012\012cpu_list = []\012color_index = 0\012for cpu in cpu_data.split(''\n''):\012    if cpu!='''':\012        cpu_split = cpu.split('' '')\012        cpu_list.append({\012            "label": cpu_split[0],\012            "fill": False,\012            "backgroundColor": colors[color_index],\012            "borderColor": colors[color_index],\012            "lineTension": 0,\012            "pointRadius": 2,\012            "borderWidth": 1,\012            "data": [cpu_split[1]]\012        })\012        color_index = color_index + 1\012        if color_index == len(colors):\012            color_index = 0\012\012options = {\012    "type": "line",\012    "data": {\012        "labels": [datetime.now().strftime(''%H:%M:%S'')],\012        "datasets": cpu_list\012    },\012    "options": {\012        "responsive": True,\012        "title":{\012            "display":True,\012            "text":"CPU usage"\012        },\012        "tooltips": {\012            "mode": "index",\012            "intersect": False\012        },\012        "hover": {\012            "mode": "nearest",\012            "intersect": True\012        },\012        "scales": {\012            "xAxes": [{\012                "display": True,\012                "scaleLabel": {\012                    "display": True,\012                    "labelString": "Time"\012                }\012            }],\012            "yAxes": [{\012                "display": True,\012                "scaleLabel": {\012                    "display": True,\012                    "labelString": "Value",\012                },\012                "ticks": {\012                    "beginAtZero": True,\012                    "max": 100\012                }\012            }]\012        }\012    }\012}\012\012result = options','\012',char(10)),'chart_append','CPU usage',0,0,1);--omnidb--
INSERT INTO mon_units VALUES(8,'postgresql',replace('from datetime import datetime\n\nlocks = connection.Query(''''''\nselect mode, count(*) as count\nfrom pg_locks\ngroup by mode\n'''''')\n\ncolors = [\n"rgb(255, 99, 132)",\n"rgb(255, 159, 64)",\n"rgb(255, 205, 86)",\n"rgb(75, 192, 192)",\n"rgb(54, 162, 235)",\n"rgb(153, 102, 255)",\n"rgb(201, 203, 207)"]\n\ndatasets = []\ncolor_index = 0\nfor lock in locks.Rows:\n    datasets.append({\n            "label": lock[''mode''],\n            "fill": False,\n            "backgroundColor": colors[color_index],\n            "borderColor": colors[color_index],\n            "lineTension": 0,\n            "pointRadius": 2,\n            "borderWidth": 1,\n            "data": [lock["count"]]\n        })\n    color_index = color_index + 1\n    if color_index == len(colors):\n        color_index = 0\n\noptions = {\n    "type": "line",\n    "data": {\n        "labels": [datetime.now().strftime(''%H:%M:%S'')],\n        "datasets": datasets\n    },\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Locks"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                }\n            }]\n        }\n    }\n}\n\nresult = options','\n',char(10)),'chart_append','Locks',1,0,NULL);--omnidb--
INSERT INTO mon_units VALUES(9,'postgresql',replace('data = connection.Query(''''''\nselect pg_is_in_recovery() as "In recovery"\n'''''')\n\nreturn_data = {\n    "columns": data.Columns,\n    "data": data.Rows\n}\n\nresult = return_data','\n',char(10)),'grid','In recovery',0,0,1);--omnidb--

CREATE TABLE version (
    ver_id text not null,
    constraint pk_versions primary key (ver_id)
);--omnidb--
INSERT INTO version VALUES('2.4.0');--omnidb--
