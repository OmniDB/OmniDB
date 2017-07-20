import threading, time, datetime

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

from OmniDB import settings

database = OmniDatabase.Generic.InstantiateDatabase(
    'sqlite',
    '',
    '',
    settings.OMNIDB_DATABASE,
    '',
    '',
    '0',
    ''
)

def start_monitoring_thread():
    t = threading.Thread(target=monitoring_loop)
    t.setDaemon(True)
    t.start()

def monitoring_loop():

    while True:
        v_alerts_due = database.v_connection.Query('''
            select z.*
            from (
            select y.*,
                   printf("%.0f",(julianday('now') - julianday(y.last_not_unknown))*86400.0) as seconds_last_not_unknown,
                   printf("%.0f",(julianday('now') - julianday(y.last_unknown))*86400.0) as seconds_last_unkown
            from (
            select a.*,
                    (
                    select t.alert_date as last_not_unknown
                    from monitor_alert_data t
                    where t.status<>'UNKNOWN'
                      and t.alert_id = a.alert_id
                    order by datetime(t.alert_date) desc
                    limit 1) as last_not_unknown,
                    (
                    select t.alert_date as last_unknown
                    from monitor_alert_data t
                    where t.status=='UNKNOWN'
                      and t.alert_id = a.alert_id
                    order by datetime(t.alert_date) desc
                    limit 1) as last_unknown
            from monitor_alert a
            where alert_enabled = 1
            ) y
            ) z
            where
            -- both null or only unknowns
            (z.last_not_unknown is null and (z.last_unknown is null or z.seconds_last_unkown > z.alert_interval)) or
            -- only not unknowns
            (z.last_unknown     is null and (z.seconds_last_not_unknown > z.alert_timeout)) or
            -- both not null
            (((z.last_not_unknown > z.last_unknown) and (z.seconds_last_not_unknown > z.alert_timeout)) or ((z.last_unknown > z.last_not_unknown) and (z.seconds_last_unkown > z.alert_interval)))
        ''')

        for v_alert in v_alerts_due.Rows:
            #message = '{0} is UNKNOWN. Last data received {1} seconds ago.'.format(v_alert['alert_name'],v_alert['seconds_last_not_unknown'])
            message = '{0} is UNKNOWN. No data received.'.format(v_alert['alert_name'])
            receive_status(v_alert['alert_id'],'UNKNOWN',message,'')

        time.sleep(60)

def receive_status(alert_id,status,message,value):
    v_last_status = 'OK'
    v_ack = 0
    try:
        v_ack = database.v_connection.ExecuteScalar('''
            select t.alert_ack
            from monitor_alert t
            where t.alert_id = {0}
        '''.format(alert_id))
    except Exception as exc:
        v_ack = 0

    try:
        v_last_status = database.v_connection.ExecuteScalar('''
            select t.status
            from monitor_alert_data t
            where t.alert_id = {0}
            order by datetime(t.alert_date)
            desc limit 1
        '''.format(alert_id))
    except Exception as exc:
        v_last_status = 'OK'


    #recovery
    if status=='OK' and v_last_status != 'OK':
        print('recovery')
        database.v_connection.Execute('''
            update monitor_alert
            set alert_ack = 0
            where alert_id = {0}
        '''.format(alert_id))
    #problem
    elif status != 'OK':
        print('problem')

    database.v_connection.Execute('''
        insert into monitor_alert_data(alert_id,status,message,value,alert_date) values (
        {0},'{1}','{2}','{3}','{4}')
    '''.format(alert_id,status,message,value,datetime.datetime.now()))
