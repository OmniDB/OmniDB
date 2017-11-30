CREATE TABLE db_type (
    dbt_st_name varchar(40),
    dbt_in_enabled integer,
    constraint pk_db_type primary key (dbt_st_name)
);
INSERT INTO db_type VALUES('sqlite',0);
INSERT INTO db_type VALUES('mysql',0);
INSERT INTO db_type VALUES('postgresql',1);
INSERT INTO db_type VALUES('firebird',0);
INSERT INTO db_type VALUES('oracle',0);
INSERT INTO db_type VALUES('sqlserver',0);
INSERT INTO db_type VALUES('access',0);
INSERT INTO db_type VALUES('sqlce',0);
INSERT INTO db_type VALUES('mariadb',0);
INSERT INTO db_type VALUES('filedb',0);

CREATE TABLE data_categories (
    cat_st_name varchar(40),
    cat_st_description varchar(100),
    cat_st_class varchar(40),
    constraint pk_data_categories primary key (cat_st_name)
);
INSERT INTO data_categories VALUES('bigint','Big Integer','numeric');
INSERT INTO data_categories VALUES('boolean','Boolean','text');
INSERT INTO data_categories VALUES('char','String','text');
INSERT INTO data_categories VALUES('date','Date Only','other');
INSERT INTO data_categories VALUES('datetime','Date Time','other');
INSERT INTO data_categories VALUES('decimal','Decimal','numeric');
INSERT INTO data_categories VALUES('fp','Floating Point','numeric');
INSERT INTO data_categories VALUES('integer','Integer','numeric');
INSERT INTO data_categories VALUES('smallint','Small Integer','numeric');
INSERT INTO data_categories VALUES('text','Long String','text');
INSERT INTO data_categories VALUES('time','Time Only','other');
INSERT INTO data_categories VALUES('varchar','Var String','text');

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
);
INSERT INTO data_types VALUES('text','access','binary',0,'''#''','#','#');
INSERT INTO data_types VALUES('boolean','access','boolean',0,'''#''','#','#');
INSERT INTO data_types VALUES('text','access','byte',0,'''#''','#','#');
INSERT INTO data_types VALUES('bigint','access','complex_type',0,'#','#','#');
INSERT INTO data_types VALUES('fp','access','double',0,'#','#','#');
INSERT INTO data_types VALUES('fp','access','float',0,'#','#','#');
INSERT INTO data_types VALUES('text','access','guid',0,'''#''','#','#');
INSERT INTO data_types VALUES('integer','access','int',0,'#','#','#');
INSERT INTO data_types VALUES('bigint','access','long',0,'#','#','#');
INSERT INTO data_types VALUES('text','access','memo',0,'''#''','#','#');
INSERT INTO data_types VALUES('decimal','access','money',0,'#','#','#');
INSERT INTO data_types VALUES('decimal','access','numeric',0,'#','#','#');
INSERT INTO data_types VALUES('text','access','ole',0,'''#''','#','#');
INSERT INTO data_types VALUES('datetime','access','short_date_time',0,'''#''','format(Nz(CStr(#),''''),''yyyy-MM-dd H:nn:ss'') as #','format(Nz(CStr(#),''''),''yyyy-MM-dd H:nn:ss'')');
INSERT INTO data_types VALUES('text','access','text',0,'''#''','#','#');
INSERT INTO data_types VALUES('bigint','firebird','bigint',0,'#','#','#');
INSERT INTO data_types VALUES('char','firebird','char',1,'''#''','#','#');
INSERT INTO data_types VALUES('date','firebird','date',0,'cast(''#'' as date)',replace('lpad(cast(extract(year from cast(# as timestamp)) as varchar(4)), 4, ''0'') || ''-'' ||\nlpad(cast(extract(month from cast(# as timestamp)) as varchar(2)), 2, ''0'') || ''-'' ||\nlpad(cast(extract(day from cast(# as timestamp)) as varchar(2)), 2, ''0'') as #','\n',char(10)),replace('lpad(cast(extract(year from cast(# as timestamp)) as varchar(4)), 4, ''0'') || ''-'' ||\nlpad(cast(extract(month from cast(# as timestamp)) as varchar(2)), 2, ''0'') || ''-'' ||\nlpad(cast(extract(day from cast(# as timestamp)) as varchar(2)), 2, ''0'')','\n',char(10)));
INSERT INTO data_types VALUES('decimal','firebird','decimal',2,'#','#','#');
INSERT INTO data_types VALUES('fp','firebird','double',0,'#','#','#');
INSERT INTO data_types VALUES('fp','firebird','double precision',0,'#','#','#');
INSERT INTO data_types VALUES('fp','firebird','float',0,'#','#','#');
INSERT INTO data_types VALUES('integer','firebird','int',0,'#','#','#');
INSERT INTO data_types VALUES('integer','firebird','integer',0,'#','#','#');
INSERT INTO data_types VALUES('char','firebird','nchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('text','firebird','ntext',0,'''#''','#','#');
INSERT INTO data_types VALUES('decimal','firebird','numeric',2,'#','#','#');
INSERT INTO data_types VALUES('varchar','firebird','nvarchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('fp','firebird','real',0,'#','#','#');
INSERT INTO data_types VALUES('smallint','firebird','smallint',0,'#','#','#');
INSERT INTO data_types VALUES('text','firebird','BLOB SUB_TYPE TEXT',0,'''#''','#','#');
INSERT INTO data_types VALUES('time','firebird','time',0,'cast(''#'' as time)',replace('lpad(cast(extract(hour from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(extract(minute from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(round(extract(second from cast(# as timestamp))) as varchar(2)), 2, ''0'') as #','\n',char(10)),replace('lpad(cast(extract(hour from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(extract(minute from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(round(extract(second from cast(# as timestamp))) as varchar(2)), 2, ''0'')','\n',char(10)));
INSERT INTO data_types VALUES('datetime','firebird','timestamp',0,'cast(''#'' as timestamp)',replace('lpad(cast(extract(year from cast(# as timestamp)) as varchar(4)), 4, ''0'') || ''-'' ||\nlpad(cast(extract(month from cast(# as timestamp)) as varchar(2)), 2, ''0'') || ''-'' ||\nlpad(cast(extract(day from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '' '' ||\nlpad(cast(extract(hour from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(extract(minute from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(round(extract(second from cast(# as timestamp))) as varchar(2)), 2, ''0'') as #','\n',char(10)),replace('lpad(cast(extract(year from cast(# as timestamp)) as varchar(4)), 4, ''0'') || ''-'' ||\nlpad(cast(extract(month from cast(# as timestamp)) as varchar(2)), 2, ''0'') || ''-'' ||\nlpad(cast(extract(day from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '' '' ||\nlpad(cast(extract(hour from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(extract(minute from cast(# as timestamp)) as varchar(2)), 2, ''0'') || '':'' ||\nlpad(cast(round(extract(second from cast(# as timestamp))) as varchar(2)), 2, ''0'')','\n',char(10)));
INSERT INTO data_types VALUES('smallint','firebird','tinyint',0,'#','#','#');
INSERT INTO data_types VALUES('varchar','firebird','varchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('bigint','mysql','bigint',0,'#','#','#');
INSERT INTO data_types VALUES('smallint','mysql','bit',0,'#','#','#');
INSERT INTO data_types VALUES('boolean','mysql','boolean',0,'''#''','#','#');
INSERT INTO data_types VALUES('char','mysql','char',1,'''#''','#','#');
INSERT INTO data_types VALUES('date','mysql','date',0,'STR_TO_DATE(''#'', ''%Y-%m-%d'')','DATE_FORMAT(#, ''%Y-%m-%d'') as #','DATE_FORMAT(#, ''%Y-%m-%d'')');
INSERT INTO data_types VALUES('datetime','mysql','datetime',0,'STR_TO_DATE(''#'', ''%Y-%m-%d %H:%i:%s'')','DATE_FORMAT(#, ''%Y-%m-%d %H:%i:%s'') as #','DATE_FORMAT(#, ''%Y-%m-%d %H:%i:%s'')');
INSERT INTO data_types VALUES('decimal','mysql','decimal',2,'#','#','#');
INSERT INTO data_types VALUES('fp','mysql','double',0,'#','#','#');
INSERT INTO data_types VALUES('fp','mysql','double precision',0,'#','#','#');
INSERT INTO data_types VALUES('fp','mysql','float',0,'#','#','#');
INSERT INTO data_types VALUES('integer','mysql','int',0,'#','#','#');
INSERT INTO data_types VALUES('integer','mysql','integer',0,'#','#','#');
INSERT INTO data_types VALUES('integer','mysql','mediumint',0,'#','#','#');
INSERT INTO data_types VALUES('decimal','mysql','numeric',2,'#','#','#');
INSERT INTO data_types VALUES('smallint','mysql','smallint',0,'#','#','#');
INSERT INTO data_types VALUES('text','mysql','text',0,'''#''','#','#');
INSERT INTO data_types VALUES('smallint','mysql','tinyint',0,'#','#','#');
INSERT INTO data_types VALUES('varchar','mysql','varchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('fp','oracle','binary_double',0,'#','to_char(#) as #','#');
INSERT INTO data_types VALUES('fp','oracle','binary_float',0,'#','to_char(#) as #','#');
INSERT INTO data_types VALUES('char','oracle','char',1,'''#''','to_char(#) as #','#');
INSERT INTO data_types VALUES('datetime','oracle','date',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('fp','oracle','double',0,'#','to_char(#) as #','#');
INSERT INTO data_types VALUES('fp','oracle','float',0,'#','to_char(#) as #','#');
INSERT INTO data_types VALUES('bigint','oracle','integer',0,'#','to_char(#) as #','#');
INSERT INTO data_types VALUES('char','oracle','nchar',1,'''#''','to_char(#) as #','#');
INSERT INTO data_types VALUES('decimal','oracle','number',2,'#','to_char(#) as #','#');
INSERT INTO data_types VALUES('decimal','oracle','numeric',2,'#','to_char(#) as #','#');
INSERT INTO data_types VALUES('varchar','oracle','nvarchar2',1,'''#''','to_char(#) as #','#');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(0)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(1)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(2)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(3)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(4)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(5)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(6)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(7)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(8)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('datetime','oracle','timestamp(9)',0,'to_date(''#'', ''yyyy-mm-dd HH24:MI:SS'')','to_char(#,''YYYY-MM-DD HH24:MI:SS'') as #','to_char(#,''YYYY-MM-DD HH24:MI:SS'')');
INSERT INTO data_types VALUES('varchar','oracle','varchar',1,'''#''','to_char(#) as #','#');
INSERT INTO data_types VALUES('varchar','oracle','varchar2',1,'''#''','to_char(#) as #','#');
INSERT INTO data_types VALUES('bigint','postgresql','bigint',0,'#','#','#');
INSERT INTO data_types VALUES('bigint','postgresql','bigserial',0,'#','#','#');
INSERT INTO data_types VALUES('boolean','postgresql','boolean',0,'''#''','#','#');
INSERT INTO data_types VALUES('char','postgresql','char',1,'''#''','#','#');
INSERT INTO data_types VALUES('char','postgresql','character',1,'''#''','#','#');
INSERT INTO data_types VALUES('varchar','postgresql','character varying',1,'''#''','#','#');
INSERT INTO data_types VALUES('date','postgresql','date',0,'''#''','to_char(#::date, ''YYYY-mm-dd'') as #','to_char(#::date, ''YYYY-mm-dd'')');
INSERT INTO data_types VALUES('decimal','postgresql','decimal',2,'#','#','#');
INSERT INTO data_types VALUES('fp','postgresql','double precision',0,'#','#','#');
INSERT INTO data_types VALUES('fp','postgresql','float',0,'#','#','#');
INSERT INTO data_types VALUES('integer','postgresql','integer',0,'#','#','#');
INSERT INTO data_types VALUES('fp','postgresql','money',0,'#','#','#');
INSERT INTO data_types VALUES('decimal','postgresql','numeric',2,'#','#','#');
INSERT INTO data_types VALUES('fp','postgresql','real',0,'#','#','#');
INSERT INTO data_types VALUES('integer','postgresql','serial',0,'#','#','#');
INSERT INTO data_types VALUES('smallint','postgresql','smallint',0,'#','#','#');
INSERT INTO data_types VALUES('smallint','postgresql','smallserial',0,'#','#','#');
INSERT INTO data_types VALUES('text','postgresql','text',0,'''#''','#','#');
INSERT INTO data_types VALUES('time','postgresql','time with time zone',0,'''#''','to_char(#::time, ''hh24:mi:ss'') as #','to_char(#::time, ''hh24:mi:ss'')');
INSERT INTO data_types VALUES('time','postgresql','time without time zone',0,'''#''','to_char(#::time, ''hh24:mi:ss'') as #','to_char(#::time, ''hh24:mi:ss'')');
INSERT INTO data_types VALUES('datetime','postgresql','timestamp with time zone',0,'''#''','to_char(#::timestamp, ''YYYY-mm-dd hh24:mi:ss'') as #','to_char(#::timestamp, ''YYYY-mm-dd hh24:mi:ss'')');
INSERT INTO data_types VALUES('datetime','postgresql','timestamp without time zone',0,'''#''','to_char(#::timestamp, ''YYYY-mm-dd hh24:mi:ss'') as #','to_char(#::timestamp, ''YYYY-mm-dd hh24:mi:ss'')');
INSERT INTO data_types VALUES('varchar','postgresql','varchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('char','sqlite','char',1,'''#''','#','#');
INSERT INTO data_types VALUES('integer','sqlite','integer',0,'#','#','#');
INSERT INTO data_types VALUES('decimal','sqlite','numeric',2,'#','#','#');
INSERT INTO data_types VALUES('varchar','sqlite','nvarchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('fp','sqlite','real',0,'#','#','#');
INSERT INTO data_types VALUES('varchar','sqlite','varchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('bigint','sqlserver','bigint',0,'#','#','#');
INSERT INTO data_types VALUES('text','sqlserver','binary',1,'''#''','#','#');
INSERT INTO data_types VALUES('text','sqlserver','bit',0,'''#''','#','#');
INSERT INTO data_types VALUES('char','sqlserver','char',1,'''#''','#','#');
INSERT INTO data_types VALUES('date','sqlserver','date',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');
INSERT INTO data_types VALUES('datetime','sqlserver','datetime',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');
INSERT INTO data_types VALUES('datetime','sqlserver','datetime2',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');
INSERT INTO data_types VALUES('datetime','sqlserver','datetimeoffset',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');
INSERT INTO data_types VALUES('decimal','sqlserver','decimal',2,'#','#','#');
INSERT INTO data_types VALUES('fp','sqlserver','float',0,'#','#','#');
INSERT INTO data_types VALUES('text','sqlserver','image',0,'''#''','#','#');
INSERT INTO data_types VALUES('integer','sqlserver','int',0,'#','#','#');
INSERT INTO data_types VALUES('fp','sqlserver','money',0,'#','#','#');
INSERT INTO data_types VALUES('char','sqlserver','nchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('text','sqlserver','ntext',0,'''#''','#','#');
INSERT INTO data_types VALUES('decimal','sqlserver','numeric',2,'#','#','#');
INSERT INTO data_types VALUES('varchar','sqlserver','nvarchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('fp','sqlserver','real',0,'#','#','#');
INSERT INTO data_types VALUES('datetime','sqlserver','smalldatetime',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');
INSERT INTO data_types VALUES('smallint','sqlserver','smallint',0,'#','#','#');
INSERT INTO data_types VALUES('fp','sqlserver','smallmoney',0,'#','#','#');
INSERT INTO data_types VALUES('text','sqlserver','text',0,'''#''','#','#');
INSERT INTO data_types VALUES('time','sqlserver','time',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');
INSERT INTO data_types VALUES('datetime','sqlserver','timestamp',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');
INSERT INTO data_types VALUES('smallint','sqlserver','tinyint',0,'#','#','#');
INSERT INTO data_types VALUES('text','sqlserver','varbinary',1,'''#''','#','#');
INSERT INTO data_types VALUES('varchar','sqlserver','varchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('integer','sqlserver','integer',0,'#','#','#');
INSERT INTO data_types VALUES('text','oracle','clob',0,'''#''','#','#');
INSERT INTO data_types VALUES('text','sqlite','text',0,'''#''','#','#');
INSERT INTO data_types VALUES('datetime','access','datetime',0,'''#''','format(Nz(CStr(#),''''),''yyyy-MM-dd H:nn:ss'') as #','format(Nz(CStr(#),''''),''yyyy-MM-dd H:nn:ss'')');
INSERT INTO data_types VALUES('time','mysql','time',0,'STR_TO_DATE(''#'', ''%H:%i:%s'')','DATE_FORMAT(#, ''%H:%i:%s'') as #','DATE_FORMAT(#, ''%H:%i:%s'')');
INSERT INTO data_types VALUES('bigint','sqlce','bigint',0,'#','#','#');
INSERT INTO data_types VALUES('text','sqlce','binary',1,'''#''','#','#');
INSERT INTO data_types VALUES('text','sqlce','bit',0,'''#''','#','#');
INSERT INTO data_types VALUES('datetime','sqlce','datetime',0,'CONVERT(datetime, ''#'', 101)','CONVERT(varchar,#,120) as #','CONVERT(varchar,#,120)');
INSERT INTO data_types VALUES('fp','sqlce','float',0,'#','#','#');
INSERT INTO data_types VALUES('text','sqlce','image',0,'''#''','#','#');
INSERT INTO data_types VALUES('integer','sqlce','integer',0,'#','#','#');
INSERT INTO data_types VALUES('fp','sqlce','money',0,'#','#','#');
INSERT INTO data_types VALUES('text','sqlce','ntext',0,'''#''','#','#');
INSERT INTO data_types VALUES('decimal','sqlce','numeric',2,'#','#','#');
INSERT INTO data_types VALUES('fp','sqlce','real',0,'#','#','#');
INSERT INTO data_types VALUES('smallint','sqlce','smallint',0,'#','#','#');
INSERT INTO data_types VALUES('smallint','sqlce','tinyint',0,'#','#','#');
INSERT INTO data_types VALUES('text','sqlce','varbinary',1,'''#''','#','#');
INSERT INTO data_types VALUES('bigint','mariadb','bigint',0,'#','#','#');
INSERT INTO data_types VALUES('smallint','mariadb','bit',0,'#','#','#');
INSERT INTO data_types VALUES('boolean','mariadb','boolean',0,'''#''','#','#');
INSERT INTO data_types VALUES('char','mariadb','char',1,'''#''','#','#');
INSERT INTO data_types VALUES('date','mariadb','date',0,'STR_TO_DATE(''#'', ''%Y-%m-%d'')','DATE_FORMAT(#, ''%Y-%m-%d'') as #','DATE_FORMAT(#, ''%Y-%m-%d'')');
INSERT INTO data_types VALUES('datetime','mariadb','datetime',0,'STR_TO_DATE(''#'', ''%Y-%m-%d %H:%i:%s'')','DATE_FORMAT(#, ''%Y-%m-%d %H:%i:%s'') as #','DATE_FORMAT(#, ''%Y-%m-%d %H:%i:%s'')');
INSERT INTO data_types VALUES('decimal','mariadb','decimal',2,'#','#','#');
INSERT INTO data_types VALUES('fp','mariadb','double',0,'#','#','#');
INSERT INTO data_types VALUES('fp','mariadb','double precision',0,'#','#','#');
INSERT INTO data_types VALUES('fp','mariadb','float',0,'#','#','#');
INSERT INTO data_types VALUES('integer','mariadb','int',0,'#','#','#');
INSERT INTO data_types VALUES('integer','mariadb','integer',0,'#','#','#');
INSERT INTO data_types VALUES('integer','mariadb','mediumint',0,'#','#','#');
INSERT INTO data_types VALUES('decimal','mariadb','numeric',2,'#','#','#');
INSERT INTO data_types VALUES('smallint','mariadb','smallint',0,'#','#','#');
INSERT INTO data_types VALUES('text','mariadb','text',0,'''#''','#','#');
INSERT INTO data_types VALUES('time','mariadb','time',0,'STR_TO_DATE(''#'', ''%H:%i:%s'')','DATE_FORMAT(#, ''%H:%i:%s'') as #','DATE_FORMAT(#, ''%H:%i:%s'')');
INSERT INTO data_types VALUES('smallint','mariadb','tinyint',0,'#','#','#');
INSERT INTO data_types VALUES('varchar','mariadb','varchar',1,'''#''','#','#');
INSERT INTO data_types VALUES('varchar','filedb','varchar',0,'''#''','#','#');

CREATE TABLE representatives (
    cat_st_name varchar(40),
    dbt_st_name varchar(40),
    rep_st_default varchar(100),
    dt_type varchar(100),
    constraint pk_rep primary key (cat_st_name, dbt_st_name),
    constraint fk_rep_dc foreign key (cat_st_name) references data_categories (cat_st_name),
    constraint fk_rep_dbt foreign key (dbt_st_name) references db_type (dbt_st_name),
    constraint fk_rep_dt foreign key (dbt_st_name, dt_type) references data_types (dbt_st_name, dt_type)
);
INSERT INTO representatives VALUES('smallint','oracle','number(5,0)','number');
INSERT INTO representatives VALUES('integer','oracle','number(10,0)','number');
INSERT INTO representatives VALUES('bigint','oracle','number(19,0)','number');
INSERT INTO representatives VALUES('decimal','oracle','number(38,0)','number');
INSERT INTO representatives VALUES('fp','oracle','number(38,4)','number');
INSERT INTO representatives VALUES('boolean','oracle','char(1)','char');
INSERT INTO representatives VALUES('varchar','oracle','varchar2(1000)','varchar2');
INSERT INTO representatives VALUES('boolean','postgresql','boolean','boolean');
INSERT INTO representatives VALUES('smallint','postgresql','smallint','smallint');
INSERT INTO representatives VALUES('integer','postgresql','bigint','bigint');
INSERT INTO representatives VALUES('bigint','postgresql','bigint','bigint');
INSERT INTO representatives VALUES('decimal','postgresql','numeric','numeric');
INSERT INTO representatives VALUES('fp','postgresql','double precision','double precision');
INSERT INTO representatives VALUES('fp','mysql','double precision','double precision');
INSERT INTO representatives VALUES('smallint','mysql','smallint','smallint');
INSERT INTO representatives VALUES('integer','mysql','integer','integer');
INSERT INTO representatives VALUES('bigint','mysql','bigint','bigint');
INSERT INTO representatives VALUES('varchar','mysql','varchar(1000)','varchar');
INSERT INTO representatives VALUES('boolean','mysql','boolean','boolean');
INSERT INTO representatives VALUES('varchar','postgresql','character varying','character varying');
INSERT INTO representatives VALUES('decimal','mysql','decimal(38,0)','decimal');
INSERT INTO representatives VALUES('decimal','firebird','decimal(38,0)','decimal');
INSERT INTO representatives VALUES('smallint','firebird','smallint','smallint');
INSERT INTO representatives VALUES('integer','firebird','integer','integer');
INSERT INTO representatives VALUES('bigint','firebird','bigint','bigint');
INSERT INTO representatives VALUES('varchar','firebird','varchar(1000)','varchar');
INSERT INTO representatives VALUES('boolean','firebird','char(1)','char');
INSERT INTO representatives VALUES('fp','firebird','double precision','double precision');
INSERT INTO representatives VALUES('datetime','postgresql','timestamp without time zone','timestamp without time zone');
INSERT INTO representatives VALUES('decimal','sqlite','numeric(38,0)','numeric');
INSERT INTO representatives VALUES('smallint','sqlite','integer','integer');
INSERT INTO representatives VALUES('integer','sqlite','integer','integer');
INSERT INTO representatives VALUES('bigint','sqlite','integer','integer');
INSERT INTO representatives VALUES('varchar','sqlite','varchar(1000)','varchar');
INSERT INTO representatives VALUES('boolean','sqlite','char(1)','char');
INSERT INTO representatives VALUES('fp','sqlite','real','real');
INSERT INTO representatives VALUES('varchar','sqlserver','varchar(1000)','varchar');
INSERT INTO representatives VALUES('char','firebird','char(1000)','char');
INSERT INTO representatives VALUES('char','mysql','char(255)','char');
INSERT INTO representatives VALUES('char','oracle','char(1000)','char');
INSERT INTO representatives VALUES('char','postgresql','char(1000)','char');
INSERT INTO representatives VALUES('char','sqlite','char(1000)','char');
INSERT INTO representatives VALUES('char','sqlserver','char(1000)','char');
INSERT INTO representatives VALUES('text','firebird','BLOB SUB_TYPE TEXT','BLOB SUB_TYPE TEXT');
INSERT INTO representatives VALUES('text','mysql','text','text');
INSERT INTO representatives VALUES('text','oracle','clob','clob');
INSERT INTO representatives VALUES('text','postgresql','text','text');
INSERT INTO representatives VALUES('text','sqlite','text','text');
INSERT INTO representatives VALUES('text','sqlserver','text','text');
INSERT INTO representatives VALUES('decimal','sqlserver','decimal(38,0)','decimal');
INSERT INTO representatives VALUES('smallint','sqlserver','smallint','smallint');
INSERT INTO representatives VALUES('integer','sqlserver','integer','integer');
INSERT INTO representatives VALUES('bigint','sqlserver','bigint','bigint');
INSERT INTO representatives VALUES('boolean','sqlserver','char(1)','char');
INSERT INTO representatives VALUES('fp','sqlserver','real','real');
INSERT INTO representatives VALUES('datetime','firebird','timestamp','timestamp');
INSERT INTO representatives VALUES('datetime','mysql','datetime','datetime');
INSERT INTO representatives VALUES('datetime','oracle','date','date');
INSERT INTO representatives VALUES('datetime','sqlite','text','text');
INSERT INTO representatives VALUES('datetime','sqlserver','datetime','datetime');
INSERT INTO representatives VALUES('datetime','access','datetime','datetime');
INSERT INTO representatives VALUES('text','access','text','text');
INSERT INTO representatives VALUES('smallint','access','int','int');
INSERT INTO representatives VALUES('integer','access','int','int');
INSERT INTO representatives VALUES('bigint','access','int','int');
INSERT INTO representatives VALUES('fp','access','double','double');
INSERT INTO representatives VALUES('boolean','access','boolean','boolean');
INSERT INTO representatives VALUES('decimal','access','numeric','numeric');
INSERT INTO representatives VALUES('char','access','text','text');
INSERT INTO representatives VALUES('varchar','access','text','text');
INSERT INTO representatives VALUES('date','postgresql','date','date');
INSERT INTO representatives VALUES('time','postgresql','time without time zone','time without time zone');
INSERT INTO representatives VALUES('time','sqlite','text','text');
INSERT INTO representatives VALUES('date','sqlite','text','text');
INSERT INTO representatives VALUES('date','mysql','date','date');
INSERT INTO representatives VALUES('time','mysql','time','time');
INSERT INTO representatives VALUES('time','firebird','time','time');
INSERT INTO representatives VALUES('date','firebird','date','date');
INSERT INTO representatives VALUES('date','oracle','date','date');
INSERT INTO representatives VALUES('time','oracle','date','date');
INSERT INTO representatives VALUES('date','access','datetime','datetime');
INSERT INTO representatives VALUES('time','access','datetime','datetime');
INSERT INTO representatives VALUES('date','sqlserver','date','date');
INSERT INTO representatives VALUES('time','sqlserver','time','time');
INSERT INTO representatives VALUES('varchar','sqlce','ntext','ntext');
INSERT INTO representatives VALUES('char','sqlce','ntext','ntext');
INSERT INTO representatives VALUES('text','sqlce','ntext','ntext');
INSERT INTO representatives VALUES('decimal','sqlce','numeric(38,0)','numeric');
INSERT INTO representatives VALUES('smallint','sqlce','smallint','smallint');
INSERT INTO representatives VALUES('integer','sqlce','integer','integer');
INSERT INTO representatives VALUES('bigint','sqlce','bigint','bigint');
INSERT INTO representatives VALUES('boolean','sqlce','ntext','ntext');
INSERT INTO representatives VALUES('fp','sqlce','real','real');
INSERT INTO representatives VALUES('datetime','sqlce','datetime','datetime');
INSERT INTO representatives VALUES('date','sqlce','datetime','datetime');
INSERT INTO representatives VALUES('time','sqlce','datetime','datetime');
INSERT INTO representatives VALUES('fp','mariadb','double precision','double precision');
INSERT INTO representatives VALUES('smallint','mariadb','smallint','smallint');
INSERT INTO representatives VALUES('integer','mariadb','integer','integer');
INSERT INTO representatives VALUES('bigint','mariadb','bigint','bigint');
INSERT INTO representatives VALUES('varchar','mariadb','varchar(1000)','varchar');
INSERT INTO representatives VALUES('boolean','mariadb','boolean','boolean');
INSERT INTO representatives VALUES('decimal','mariadb','decimal(38,0)','decimal');
INSERT INTO representatives VALUES('char','mariadb','char(255)','char');
INSERT INTO representatives VALUES('text','mariadb','text','text');
INSERT INTO representatives VALUES('datetime','mariadb','datetime','datetime');
INSERT INTO representatives VALUES('date','mariadb','date','date');
INSERT INTO representatives VALUES('time','mariadb','time','time');
INSERT INTO representatives VALUES('varchar','filedb','varchar(1000)','varchar');

CREATE TABLE themes (
    theme_id integer not null,
    theme_name varchar(50),
    theme_type varchar(50),
    constraint pk_themes primary key (theme_id)
);
INSERT INTO themes VALUES(1,'omnidb','light');
INSERT INTO themes VALUES(2,'chrome','light');
INSERT INTO themes VALUES(3,'clouds','light');
INSERT INTO themes VALUES(4,'crimson_editor','light');
INSERT INTO themes VALUES(5,'dawn','light');
INSERT INTO themes VALUES(6,'dreamweaver','light');
INSERT INTO themes VALUES(7,'eclipse','light');
INSERT INTO themes VALUES(8,'github','light');
INSERT INTO themes VALUES(9,'iplastic','light');
INSERT INTO themes VALUES(10,'katzenmilch','light');
INSERT INTO themes VALUES(11,'kuroir','light');
INSERT INTO themes VALUES(12,'solarized_light','light');
INSERT INTO themes VALUES(13,'sqlserver','light');
INSERT INTO themes VALUES(14,'textmate','light');
INSERT INTO themes VALUES(15,'tomorrow','light');
INSERT INTO themes VALUES(16,'xcode','light');
INSERT INTO themes VALUES(17,'omnidb_dark','dark');
INSERT INTO themes VALUES(18,'ambiance','dark');
INSERT INTO themes VALUES(19,'chaos','dark');
INSERT INTO themes VALUES(20,'clouds_midnight','dark');
INSERT INTO themes VALUES(21,'cobalt','dark');
INSERT INTO themes VALUES(22,'idle_fingers','dark');
INSERT INTO themes VALUES(23,'kr_theme','dark');
INSERT INTO themes VALUES(24,'merbivore','dark');
INSERT INTO themes VALUES(25,'merbivore_soft','dark');
INSERT INTO themes VALUES(26,'mono_industrial','dark');
INSERT INTO themes VALUES(27,'monokai','dark');
INSERT INTO themes VALUES(28,'pastel_on_dark','dark');
INSERT INTO themes VALUES(29,'solarized_dark','dark');
INSERT INTO themes VALUES(30,'terminal','dark');
INSERT INTO themes VALUES(31,'tomorrow_night','dark');
INSERT INTO themes VALUES(32,'tomorrow_night_blue','dark');
INSERT INTO themes VALUES(33,'tomorrow_night_bright','dark');
INSERT INTO themes VALUES(34,'tomorrow_night_eighties','dark');
INSERT INTO themes VALUES(35,'twilight','dark');
INSERT INTO themes VALUES(36,'vibrant_ink','dark');

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
);
INSERT INTO users VALUES(1,'admin','8IqxKdQ=',1,'14',1,1,'0c4a137f-9918-4c0b-af45-480deef6f760');

CREATE TABLE messages (
    mes_in_code integer not null,
    mes_st_text text,
    mes_dt_timestamp text not null,
    user_id integer not null,
    mes_bo_image integer not null,
    constraint pk_messages primary key (mes_in_code),
    constraint messages_fk_0 foreign key (user_id) references users (user_id)  on update NO ACTION  on delete CASCADE
);

CREATE TABLE messages_users (
    mes_in_code integer not null,
    user_id integer not null,
    constraint pk_messages_users primary key (mes_in_code, user_id),
    constraint messages_users_fk_0 foreign key (mes_in_code) references messages (mes_in_code)  on update NO ACTION  on delete CASCADE,
    constraint messages_users_fk_1 foreign key (user_id) references users (user_id)  on update NO ACTION  on delete CASCADE
);

CREATE TABLE snippets_nodes (
    sn_id integer not null,
    sn_name text,user_id integer not null,
    sn_date_create text,
    sn_date_modify text,
    sn_id_parent integer,
    constraint pk_snippets_nodes primary key (sn_id),
    constraint fk_sn_users foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE,
    constraint fk_sn_sn foreign key (sn_id_parent) references snippets_nodes (sn_id)  on update CASCADE  on delete CASCADE
);

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
);

CREATE TABLE monitor_node (
    node_id integer not null,
    node_name text,node_desc text,
    user_id integer,
    node_key text,
    constraint pk_monitor_node primary key (node_id),
    constraint monitor_node_fk_0 foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE
);

CREATE TABLE monitor_alert (
    alert_id integer not null,
    node_id integer not null,
    alert_name text,
    alert_desc text,
    alert_interval integer,
    alert_timeout integer,
    alert_min_value text,
    alert_max_value text,
    alert_enabled integer,
    alert_ack integer,
    constraint pk_monitor_alert primary key (alert_id),
    constraint monitor_alert_fk_0 foreign key (node_id) references monitor_node (node_id)  on update CASCADE  on delete CASCADE
);

CREATE TABLE monitor_alert_data (
    alert_id integer not null,
    status text,
    message text,
    value text,
    alert_date text,
    constraint monitor_alert_data_fk_0 foreign key (alert_id) references monitor_alert (alert_id)  on update CASCADE  on delete CASCADE
);

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
);

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
);

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
);

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
);

CREATE TABLE tabs (
    conn_id integer not null,
    user_id integer not null,
    tab_id integer not null,
    snippet text,
    constraint fk_tabs_conn foreign key (conn_id) references connections (conn_id)  on update CASCADE  on delete CASCADE,
    constraint fk_tabs_users foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE
);

CREATE TABLE version (
    ver_id text not null,
    constraint pk_versions primary key (ver_id)
);
INSERT INTO version VALUES('2.4.0');
