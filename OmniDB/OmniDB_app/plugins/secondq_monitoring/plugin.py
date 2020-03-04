from . import metadata as metadata

import json
import psycopg2

from pprint import pprint

MONITORING_DATABASE = "dbname='postgres' user='postgres' host='10.33.2.114'"
SCHEMA = "monitoring"

def secondq_load_dashboard_data(p_database_object, p_data):

    v_mode = p_data['p_mode']


    if v_mode == 'all' or v_mode == 'notifications':
        v_notifications = secondq_get_notifications(p_database_object, p_data)
    else:
        v_notifications = None

    if v_mode == 'all':
        v_counts = secondq_get_state_counts(p_data)
    else:
        v_counts = None

    return {
        'state_counts': v_counts,
        'notifications': v_notifications
    }

def secondq_get_state_counts(p_data):
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        # Retrieving aggregation by unit to fill the 4 summary boxes in the tactical board
        cur.execute("""
        SELECT su_state, unit_front_name, count(*)
        FROM {0}.server_unit su
        INNER JOIN {0}.unit u ON su.unit_id = u.unit_id
        WHERE su_state NOT in ('ok','unknown')
          AND su_acked = false
          AND (su_downtime = false or (su_downtime = true AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime)))
          AND su_enabled = true
        GROUP BY su_state, unit_front_name
        ORDER BY su_state
        """.format(SCHEMA))
        rows_groups = cur.fetchall()

        groups = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }

        for row in rows_groups:
            groups[row[0]].append(
            {
                'unit': row[1],
                'count': int(row[2])
            }
            )

        # Retrieving counts to fill the charts and colored boxes in the tactical board
        cur.execute("""
        WITH resultset AS (
        SELECT su.*,
        u.unit_name
        FROM {0}.server_unit su
        INNER JOIN {0}.server s ON su.server_id = s.server_id
        INNER JOIN {0}.unit u ON su.unit_id = u.unit_id
        WHERE 1 = 1
        )
        SELECT

        (SELECT count(*)
           FROM resultset
           WHERE unit_name='ping'
             AND su_enabled = true
             AND su_state != 'ok'
             AND su_acked = true) as server_critical_ack_count,

        (SELECT count(*)
           FROM resultset
           WHERE unit_name='ping'
             AND su_enabled = true
             AND su_state != 'ok'
             AND (su_downtime = true
                      AND (now() BETWEEN su_downtime_starttime AND su_downtime_endtime))) as server_critical_downtime_count,

        (SELECT count(*)
           FROM resultset
           WHERE unit_name='ping'
             AND su_enabled = true
             AND su_state != 'ok'
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as server_critical_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='critical'
             AND su_enabled = true
             AND su_acked = true) as unit_critical_ack_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='critical'
             AND su_enabled = true
             AND (su_downtime = true
                      AND (now() BETWEEN su_downtime_starttime AND su_downtime_endtime))) as unit_critical_downtime_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='critical'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as unit_critical_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='high'
             AND su_enabled = true
             AND su_acked = true) as unit_high_ack_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='high'
             AND su_enabled = true
             AND (su_downtime = true
                      AND (now() BETWEEN su_downtime_starttime AND su_downtime_endtime))) as unit_high_downtime_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='high'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as unit_high_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='medium'
             AND su_enabled = true
             AND su_acked = true) as unit_medium_ack_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='medium'
             AND (su_downtime = true
                      AND (now() BETWEEN su_downtime_starttime AND su_downtime_endtime))) as unit_medium_downtime_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='medium'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as unit_medium_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='low'
             AND su_enabled = true
             AND su_acked = true) as unit_low_ack_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='low'
             AND su_enabled = true
             AND (su_downtime = true
                      AND (now() BETWEEN su_downtime_starttime AND su_downtime_endtime))) as unit_low_downtime_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='low'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as unit_low_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='unknown'
             AND su_enabled = true
             AND su_acked = true) as unit_unknown_ack_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='unknown'
             AND su_enabled = true
             AND (su_downtime = true
                      AND (now() BETWEEN su_downtime_starttime AND su_downtime_endtime))) as unit_unknown_downtime_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='unknown'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as unit_unknown_count,

        (SELECT count(*)
           FROM resultset
           WHERE unit_name='ping'
             AND su_enabled = true
             AND su_state = 'ok') as chart_server_ok_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='ok'
             AND su_enabled = true) as chart_unit_ok_count
        """.format(SCHEMA))
        rows = cur.fetchall()

        result = {
            "server_critical_ack_count": rows[0][0],
            "server_critical_downtime_count": rows[0][1],
            "server_critical_count": rows[0][2],
            "chart_server_critical_count": rows[0][2],

            "unit_critical_ack_count": rows[0][3],
            "unit_critical_downtime_count": rows[0][4],
            "unit_critical_count": rows[0][5],
            "chart_unit_critical_count": rows[0][5],

            "unit_high_ack_count": rows[0][6],
            "unit_high_downtime_count": rows[0][7],
            "unit_high_count": rows[0][8],
            "chart_unit_high_count": rows[0][8],

            "unit_medium_ack_count": rows[0][9],
            "unit_medium_downtime_count": rows[0][10],
            "unit_medium_count": rows[0][11],
            "chart_unit_medium_count": rows[0][11],

            "unit_low_ack_count": rows[0][12],
            "unit_low_downtime_count": rows[0][13],
            "unit_low_count": rows[0][14],
            "chart_unit_low_count": rows[0][14],

            "unit_unknown_ack_count": rows[0][15],
            "unit_unknown_downtime_count": rows[0][16],
            "unit_unknown_count": rows[0][17],
            "chart_unit_unknown_count": rows[0][17],

            "chart_server_ok_count": rows[0][18],
            "chart_unit_ok_count": rows[0][19],
            "chart_server_problem_ok_count": rows[0][0] + rows[0][1],
            "chart_unit_problem_ok_count": rows[0][3] + rows[0][4] + rows[0][6] + rows[0][7] + rows[0][9] + rows[0][10] + rows[0][12] + rows[0][13] + rows[0][15] + rows[0][16],
            'groups': groups

        }

    except Exception as exc:
        print(str(exc))

    return result

def secondq_get_notifications(p_database_object, p_data):
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        # events
        if p_data['p_notification_type'] == 'events':

            v_filter = 'WHERE 1=1 '
            if p_data['p_check_events_severity'] == False:
                v_filter = v_filter + """ AND t.event_category != 'unit'
                """

            if p_data['p_check_events_user'] == False:
                v_filter = v_filter + """ AND t.event_category != 'administrative'
                """

            if 'input_filter' in p_data and p_data['input_filter']!=None and p_data['input_filter']!='':
                v_filter = v_filter + """ AND (lower(t.customer_name) like lower('%{0}%')
                                        OR lower(t.server_name) like lower('%{0}%')
                                        OR lower(t.event_name) like lower('%{0}%')
                                        OR lower(t.elapsed) like lower('%{0}%')
                                        OR lower(t.unit_name) like lower('%{0}%')
                                        OR lower(t.new_state) like lower('%{0}%'))
                                    """.format(p_data['input_filter'])

            cur.execute("""
            SELECT * FROM (
            SELECT monitoring.get_elapsed_time(event_time) as elapsed,
                   e.data->>'type' as type,
                   ev.event_name as event_name,
                   e.data->>'data' as data,
                   c.customer_name,
                   c.customer_id,
                   s.server_name,
                   s.server_id,
                   CASE WHEN su.su_key IS NULL THEN
                        u.unit_front_name
                   ELSE
                        u.unit_front_name || ' - ' || su.su_key
                   END as unit_name,
                   su.su_id,
                   e.event_time,
                   e.data->'data'->>'new_state' as new_state,
                   ev.event_category
            FROM monitoring.event_list e
            LEFT JOIN {0}.event ev ON (e.data->>'type')::text = ev.event_type
            LEFT JOIN {0}.customer c ON (e.data->'data'->>'customer_id')::bigint = c.customer_id
            LEFT JOIN {0}.server s ON (e.data->'data'->>'server_id')::bigint = s.server_id
            LEFT JOIN {0}.server_unit su ON (e.data->'data'->>'su_id')::bigint = su.su_id
            LEFT JOIN {0}.unit u ON su.unit_id = u.unit_id
            ) t
            {1}
            ORDER BY t.event_time desc
            LIMIT 500
            """.format(SCHEMA,v_filter))

            rows = cur.fetchall()

            notifications_data = []
            for row in rows:
                notifications_data.append(
                {
                'time': row[0],
                'type': row[1],
                'type_name': row[2],
                'data': json.loads(row[3]),
                'customer_name': row[4],
                'customer_id': row[5],
                'server_name': row[6],
                'server_id': row[7],
                'unit_name': row[8],
                'su_id': row[9],
                }
                )
        #problems
        else:

            v_filter = ' '
            if p_data['p_check_problems_criticalhigh'] == True:
                v_filter = v_filter + """ AND t.su_state in ('critical','high')
                """

            if 'input_filter' in p_data and p_data['input_filter']!=None and p_data['input_filter']!='':
                v_filter = v_filter + """ AND (lower(t.customer_name) like lower('%{0}%')
                                        OR lower(t.server_name) like lower('%{0}%')
                                        OR lower(t.elapsed) like lower('%{0}%')
                                        OR lower(t.unit_name) like lower('%{0}%')
                                        OR lower(t.su_state) like lower('%{0}%'))
                                    """.format(p_data['input_filter'])

            cur.execute("""
            SELECT * FROM (
                select {0}.get_elapsed_time(su.su_last_change) as elapsed,
                       c.customer_name,
                       c.customer_id,
                       s.server_name,
                       s.server_id,
                       CASE WHEN su.su_key IS NULL THEN
                            u.unit_front_name
                       ELSE
                            u.unit_front_name || ' - ' || su.su_key
                       END as unit_name,
                       su.su_id,
                       su.su_state,
                       CASE su.su_state WHEN 'critical' THEN 0
                       WHEN 'high' THEN 1
                       WHEN 'medium' THEN 2
                       WHEN 'low' THEN 3
                       WHEN 'unknown' THEN 4
                       END as priority
                from {0}.server_unit su
                inner join {0}.server s on su.server_id = s.server_id
                inner join {0}.unit u on su.unit_id = u.unit_id
                inner join {0}.customer c on s.customer_id = c.customer_id
                where su_state != 'ok'
                  and su.su_enabled = true
                  and su.su_acked = false
                  and (su.su_downtime = false or (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime)))
              ) t WHERE 1 = 1
              {1}
            order by priority, elapsed DESC
            """.format(SCHEMA,v_filter))

            rows = cur.fetchall()

            notifications_data = []
            for row in rows:
                notifications_data.append(
                {
                'time': row[0],
                'state': row[7],
                'customer_name': row[1],
                'customer_id': row[2],
                'server_name': row[3],
                'server_id': row[4],
                'unit_name': row[5],
                'su_id': row[6],
                }
                )

    except Exception as exc:
        print(str(exc))

    return notifications_data

def secondq_load_host_dashboard_data(p_database_object, p_data):

    v_mode = p_data['p_mode']

    if v_mode == 'all' or v_mode == 'details':
        v_details = secondq_load_host_details(p_data)
    else:
        v_details = None

    if v_mode == 'all' or v_mode == 'grid':
        v_grid = secondq_load_unit_list_data(p_database_object, p_data)
    else:
        v_grid = None

    return {
        'details': v_details,
        'units': v_grid
    }

def secondq_load_host_details(p_data):
    host_data = None
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        v_filter = "WHERE s.server_id = {0}".format(p_data['p_host_id'])

        cur.execute("""
        WITH resultset AS (
        SELECT su.*,
        u.unit_name
        FROM {0}.server_unit su
        INNER JOIN {0}.server s ON su.server_id = s.server_id
        INNER JOIN {0}.customer c ON s.customer_id = c.customer_id
        INNER JOIN {0}.unit u ON su.unit_id = u.unit_id
        {1}
        )
        SELECT

        (SELECT count(*)
           FROM resultset
           WHERE su_state='critical'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_critical_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='high'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_high_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='medium'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_medium_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='low'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_low_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='unknown'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_unknown_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state!='ok'
             AND su_enabled = true
             AND ((su_acked = true)
                  OR (su_downtime = true
                           AND (now() BETWEEN su_downtime_starttime AND su_downtime_endtime)))) as chart_unit_problem_ok_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='ok'
             AND su_enabled = true) as chart_unit_ok_count
        """.format(SCHEMA,v_filter))
        rows_chart = cur.fetchall()

        cur.execute("""
        SELECT CASE WHEN su.su_state = 'ok' THEN 'up'
               ELSE 'down' END AS status,
               {0}.get_elapsed_time(su.su_last_change) as elapsed,
               CASE WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'critical' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'critical'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'high' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'high'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'unknown' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'unknown'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'medium' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'medium'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'low' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'low'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'ok' AND su.su_enabled = true) > 0 THEN 'ok'
               ELSE '' END AS max_severity,
               (s.server_data->'gathered_data')::text,
               su.su_acked,
               CASE WHEN su.su_downtime = true AND (now() BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime) THEN true
               ELSE false END AS downtime_now,
               to_char(su.su_acked_endtime, 'YYYY-mm-dd HH24:MI:SS'),
               su.su_acked_message,
               su.su_acked_user,
               to_char(su.su_downtime_starttime, 'YYYY-mm-dd HH24:MI:SS'),
               to_char(su.su_downtime_endtime, 'YYYY-mm-dd HH24:MI:SS'),
               su.su_downtime_user,
               su.su_downtime,
               {0}.get_elapsed_time((server_data->'gathered_data'->>'time')::timestamp) as gathered_elapsed,
               su.su_enabled,
               c.customer_name,
               s.server_front_name,
               s.server_token
        FROM {0}.server s
        INNER JOIN {0}.customer c ON s.customer_id = c.customer_id
        LEFT JOIN {0}.server_unit su ON s.server_id = su.server_id AND su.unit_id = (SELECT unit_id FROM {0}.unit WHERE unit_name ='ping')
        {1}
        """.format(SCHEMA,v_filter))

        rows = cur.fetchall()

        #Status
        if rows[0][0] == 'up':
            status_cell = "<i class='fas fa-arrow-alt-circle-up secondq_status_text_up'></i> ({0})".format(rows[0][1])
        else:
            status_cell = "<i class='fas fa-arrow-alt-circle-down secondq_status_text_down'></i> ({0})".format(rows[0][1])

        try:
            data_json = json.loads(rows[0][3])
        except Exception:
            data_json = None

        if (rows[0][4]==True or rows[0][5]==True):
            ok = True
        else:
            ok = False

        host_data = {
            'customer': rows[0][15],
            'server': rows[0][16],
            'token': rows[0][17],
            'status': status_cell,
            'max_severity': rows[0][2],
            'ok': ok,
            'ack': rows[0][4],
            'ack_endtime': rows[0][6],
            'ack_message': rows[0][7],
            'ack_user': rows[0][8],
            'downtime': rows[0][12],
            'downtime_starttime': rows[0][9],
            'downtime_endtime': rows[0][10],
            'downtime_user': rows[0][11],
            'enabled': rows[0][14],
            'data_json': data_json,
            'data_elapsed': rows[0][13],
            'chart': {
                "chart_unit_critical_count": rows_chart[0][0],
                "chart_unit_high_count": rows_chart[0][1],
                "chart_unit_medium_count": rows_chart[0][2],
                "chart_unit_low_count": rows_chart[0][3],
                "chart_unit_unknown_count": rows_chart[0][4],
                "chart_unit_problem_ok_count": rows_chart[0][5],
                "chart_unit_ok_count": rows_chart[0][6]
            }
        }

    except Exception as exc:
        print(str(exc))

    return host_data

def secondq_load_customer_dashboard_data(p_database_object, p_data):

    v_mode = p_data['p_mode']

    if v_mode == 'all' or v_mode == 'details':
        v_details = secondq_load_customer_details(p_data)
    else:
        v_details = None

    if v_mode == 'all' or v_mode == 'grid':
        v_grid = secondq_load_host_list_data(p_database_object, p_data)
    else:
        v_grid = None

    return {
        'details': v_details,
        'hosts': v_grid
    }

def secondq_load_customer_details(p_data):
    host_data = None
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        v_filter = "WHERE c.customer_id = {0}".format(p_data['p_customer_id'])

        cur.execute("""
        WITH resultset AS (
        SELECT su.*,
        u.unit_name
        FROM {0}.server_unit su
        INNER JOIN {0}.server s ON su.server_id = s.server_id
        INNER JOIN {0}.customer c ON s.customer_id = c.customer_id
        INNER JOIN {0}.unit u ON su.unit_id = u.unit_id
        {1}
        )
        SELECT

        (SELECT count(*)
           FROM resultset
           WHERE su_state='critical'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_critical_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='high'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_high_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='medium'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_medium_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='low'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_low_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='unknown'
             AND su_enabled = true
             AND (su_acked = false
                  AND (su_downtime = false
                       OR (su_downtime = true
                           AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))))) as chart_unit_unknown_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state!='ok'
             AND su_enabled = true
             AND ((su_acked = true)
                  OR (su_downtime = true
                           AND (now() BETWEEN su_downtime_starttime AND su_downtime_endtime)))) as chart_unit_problem_ok_count,

        (SELECT count(*)
           FROM resultset
           WHERE su_state='ok'
             AND su_enabled = true) as chart_unit_ok_count,

        (SELECT CASE WHEN (SELECT count(1) FROM resultset WHERE su_state = 'critical' AND su_enabled = true AND (su_downtime = false OR (su_downtime = true AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))) AND su_acked = false ) > 0 THEN 'critical'
                    WHEN (SELECT count(1) FROM resultset WHERE su_state = 'high' AND su_enabled = true AND (su_downtime = false OR (su_downtime = true AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))) AND su_acked = false ) > 0 THEN 'high'
                    WHEN (SELECT count(1) FROM resultset WHERE su_state = 'unknown' AND su_enabled = true AND (su_downtime = false OR (su_downtime = true AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))) AND su_acked = false ) > 0 THEN 'unknown'
                    WHEN (SELECT count(1) FROM resultset WHERE su_state = 'medium' AND su_enabled = true AND (su_downtime = false OR (su_downtime = true AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))) AND su_acked = false ) > 0 THEN 'medium'
                    WHEN (SELECT count(1) FROM resultset WHERE su_state = 'low' AND su_enabled = true AND (su_downtime = false OR (su_downtime = true AND (now() NOT BETWEEN su_downtime_starttime AND su_downtime_endtime))) AND su_acked = false ) > 0 THEN 'low'
                    WHEN (SELECT count(1) FROM resultset WHERE su_state = 'ok' AND su_enabled = true) > 0 THEN 'ok'
                       ELSE '' END AS max_severity)
        """.format(SCHEMA,v_filter))
        rows = cur.fetchall()

        cur.execute("""
        SELECT customer_name,
               server_front_name,
               CASE WHEN su1.su_state = 'ok' THEN 'up'
                       ELSE 'down' END AS status,
               server_data->'gathered_data'->'data'->'system'->>'hostname' as hostname,
               server_data->'gathered_data'->'data'->'system'->>'ip_list' as ip_list,
               su2.su_last_data->>'message' as rep_data,
               s.server_data->'gathered_data'->'data'->'postgresql'->>'role',
               c.customer_token
        FROM {0}.server s
        INNER JOIN {0}.customer c on s.customer_id = c.customer_id
        LEFT JOIN {0}.server_unit su1 ON s.server_id = su1.server_id AND su1.unit_id = (SELECT unit_id FROM {0}.unit WHERE unit_name = 'ping')
        LEFT JOIN {0}.server_unit su2 ON s.server_id = su2.server_id AND su2.unit_id = (SELECT unit_id FROM {0}.unit WHERE unit_name = 'replication_source') AND su2.su_state != 'unknown'
        {1}
        """.format(SCHEMA,v_filter))
        rows_graph = cur.fetchall()

        graph_data = {
            'nodes': [],
            'edges': []
        }
        server_temp_data_list = []

        for row in rows_graph:

            role = row[6]
            status = row[2]
            if role == 'Primary':
                shape = 'star'
            else:
                shape = 'ellipse'
            if status == 'up':
                color = 'rgba(68, 169, 3, 0.75)'
            else:
                color = 'rgba(255, 0, 0, 0.75)'

            add_unique_node(graph_data['nodes'],
                {
                    'data': {
                        'id': row[1],
                        'label': row[1],
                        'shape': shape,
                        'color': color
                    }
                }
            )

            hostname = row[3]
            try:
                ip_list = json.loads(row[4])
            except:
                ip_list = []
            try:
                rep_data = json.loads(row[5])
                if type(rep_data) != list:
                    rep_data = []
            except:
                rep_data = []

            server_temp_data_list.append(
                {
                    'server': row[1],
                    'ip_list': ip_list,
                    'hostname': hostname,
                    'rep_data': rep_data
                }
            )

        # Building replication edges

        # First check replication targets that are monitored so they are added
        # first to the graph
        for monitored in [True,False]:
            for server_temp_data in server_temp_data_list:
                # Iterate through all replication rows
                for target_rep_data in server_temp_data['rep_data']:
                    if target_rep_data['monitored'] == monitored:
                        if not target_rep_data['monitored']:
                            edge_color = 'gray'
                        else:
                            if not target_rep_data['connected']:
                                edge_color = 'rgba(255, 0, 0, 0.75)'
                            else:
                                edge_color = 'rgba(68, 169, 3, 0.75)'

                        # replacing None values with empty string
                        if target_rep_data['address'] == None:
                            target_address = ''
                        else:
                            target_address = target_rep_data['address']
                        if target_rep_data['hostname'] == None:
                            target_hostname = ''
                        else:
                            target_hostname = target_rep_data['hostname']
                        if target_rep_data['application_name'] == None:
                            target_application_name = ''
                        else:
                            target_application_name = target_rep_data['application_name']
                        if target_rep_data['pid'] == None:
                            target_pid = ''
                        else:
                            target_pid = target_rep_data['pid']

                        if target_rep_data['lag_mb'] == None:
                            text_lag = ''
                        else:
                            text_lag = str(target_rep_data['lag_mb']) + 'MiB\n'
                        v_new_nodes = []
                        # Pointing to local server
                        if target_rep_data['address'] == '127.0.0.1' or target_rep_data['address'] == '::1' or target_rep_data['address'] == '':
                            add_unique_edge(graph_data['edges'],
                                {
                                    'data': {
                                        'id': server_temp_data['server'] + '_' + server_temp_data['server'] + '_' + target_address + '_' + target_hostname + '_' + target_application_name + '_' + target_pid,
                                        'source': server_temp_data['server'],
                                        'target': server_temp_data['server'],
                                        'label': text_lag,
                                        'color': edge_color,
                                        'line_style': 'solid'
                                    }
                                }
                            )
                            # next iteration
                            continue
                        else:
                            # Iterate through all server to find the one correspoding to the replication row
                            for target_server_temp_data in server_temp_data_list:
                                if target_server_temp_data['hostname'] == target_hostname:
                                    add_unique_edge(v_new_nodes,
                                        {
                                            'data': {
                                                'id': server_temp_data['server'] + '_' + target_server_temp_data['server'] + '_' + target_address + '_' + target_hostname + '_' + target_application_name + '_' + target_pid,
                                                'source': server_temp_data['server'],
                                                'target': target_server_temp_data['server'],
                                                'label': text_lag,
                                                'color': edge_color
                                            }
                                        }
                                    )
                                else:
                                    # Iterate through ips of server
                                    for target_server_ip in target_server_temp_data['ip_list']:
                                        if target_server_ip == target_address:
                                            add_unique_edge(v_new_nodes,
                                                {
                                                    'data': {
                                                        'id': server_temp_data['server'] + '_' + target_server_temp_data['server'] + '_' + target_address + '_' + target_hostname + '_' + target_application_name + '_' + target_pid,
                                                        'source': server_temp_data['server'],
                                                        'target': target_server_temp_data['server'],
                                                        'label': text_lag,
                                                        'color': edge_color
                                                    }
                                                }
                                            )
                                            break
                            if len(v_new_nodes) > 1:
                                for v_new_node in v_new_nodes:
                                    v_new_node['data']['line_style'] = 'dashed'
                                    add_unique_edge(graph_data['edges'],v_new_node)
                            elif len(v_new_nodes) == 1:
                                for v_new_node in v_new_nodes:
                                    v_new_node['data']['line_style'] = 'solid'
                                    add_unique_edge(graph_data['edges'],v_new_node)
                            # not found, add node and edge to it
                            else:
                                new_id = target_address + '_' + target_hostname + '_' + target_application_name + '_' + target_pid
                                new_name = target_address
                                add_unique_node(graph_data['nodes'],
                                    {
                                        'data': {
                                            'id': new_id,
                                            'label': new_name,
                                            'shape': 'ellipse',
                                            'color': 'gray'
                                        }
                                    }
                                )
                                add_unique_edge(graph_data['edges'],
                                    {
                                        'data': {
                                            'id': server_temp_data['server'] + '_' + new_id,
                                            'source': server_temp_data['server'],
                                            'target': new_id,
                                            'label': text_lag,
                                            'line_style': 'solid',
                                            'color': edge_color
                                        }
                                    }
                                )


        host_data = {
            'customer': rows_graph[0][0],
            'token': rows_graph[0][7],
            'max_severity': rows[0][7],
            'chart': {
                "chart_unit_critical_count": rows[0][0],
                "chart_unit_high_count": rows[0][1],
                "chart_unit_medium_count": rows[0][2],
                "chart_unit_low_count": rows[0][3],
                "chart_unit_unknown_count": rows[0][4],
                "chart_unit_problem_ok_count": rows[0][5],
                "chart_unit_ok_count": rows[0][6]
            },
            'graph': graph_data
        }

    except Exception as exc:
        print(str(exc))

    return host_data

def add_unique_edge(p_edge_list, p_edge):
    for edge in p_edge_list:
        if edge['data']['id'] == p_edge['data']['id']:
            return
    p_edge_list.append(p_edge)

def add_unique_node(p_node_list, p_node):
    for node in p_node_list:
        if node['data']['id'] == p_node['data']['id']:
            return
    p_node_list.append(p_node)


def secondq_load_unit_dashboard_data(p_database_object, p_data):

    v_mode = p_data['p_mode']

    if v_mode == 'all' or v_mode == 'details':
        v_details = secondq_load_unit_details(p_data)
    else:
        v_details = None

    if v_mode == 'all' or v_mode == 'chart':
        v_chart = secondq_load_unit_chart_data(p_database_object, p_data)
    else:
        v_chart = None

    return {
        'details': v_details,
        'chart': v_chart
    }

def secondq_load_unit_details(p_data):
    unit_data = None
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        v_filter = "WHERE su.su_id = {0}".format(p_data['p_su_id'])
        cur.execute("""
        SELECT su.su_state,
               {0}.get_elapsed_time(su.su_last_change) as elapsed,
               coalesce(su.su_threshold_critical::text,'-'),
               coalesce(su.su_threshold_high::text,'-'),
               coalesce(su.su_threshold_medium::text,'-'),
               coalesce(su.su_threshold_low::text,'-'),
               (su.su_last_data)::text,
               su.su_acked,
               CASE WHEN su.su_downtime = true AND (now() BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime) THEN true
               ELSE false END AS downtime_now,
               to_char(su.su_acked_endtime, 'YYYY-mm-dd HH24:MI:SS'),
               su.su_acked_message,
               su.su_acked_user,
               to_char(su.su_downtime_starttime, 'YYYY-mm-dd HH24:MI:SS'),
               to_char(su.su_downtime_endtime, 'YYYY-mm-dd HH24:MI:SS'),
               su.su_downtime_user,
               su.su_downtime,
               su.su_threshold_critical,
               su.su_threshold_high,
               su.su_threshold_medium,
               su.su_threshold_low,
               su.su_enabled,
               su.su_key,
               c.customer_name,
               s.server_front_name,
               CASE WHEN su.su_key IS NULL THEN
                    u.unit_front_name
               ELSE
                    u.unit_front_name || ' - ' || su.su_key
               END as unit_front_name,
               CASE WHEN su.su_threshold_low IS NOT NULL THEN su.su_threshold_low
                    WHEN su.su_threshold_medium IS NOT NULL THEN su.su_threshold_medium
                    WHEN su.su_threshold_high IS NOT NULL THEN su.su_threshold_high
                    WHEN su.su_threshold_critical IS NOT NULL THEN su.su_threshold_critical
               ELSE null END as min_threshold,
               u.unit_name
        FROM {0}.server_unit su
        INNER JOIN {0}.server s ON su.server_id = s.server_id
        INNER JOIN {0}.customer c ON s.customer_id = c.customer_id
        INNER JOIN {0}.unit u ON su.unit_id = u.unit_id
        {1}
        """.format(SCHEMA,v_filter))

        rows = cur.fetchall()

        if (rows[0][7]==True or rows[0][8]==True or rows[0][20]==False):
            status_text = "<span class='secondq_notification_severity_text secondq_status_box_ack'>{0}</span> ({1})".format(rows[0][0],rows[0][1])
        else:
            status_text = "<span class='secondq_notification_severity_text secondq_status_box_{0}'>{0}</span> ({1})".format(rows[0][0],rows[0][1])

        try:
            data_json = json.loads(rows[0][6])
        except Exception:
            data_json = None

        formatted_data = get_formatted_metrics(rows[0][26], rows[0][23], rows[0][0], rows[0][25], rows[0][6])

        if (rows[0][7]==True or rows[0][8]==True):
            ok = True
        else:
            ok = False

        unit_data = {
            'customer': rows[0][22],
            'server': rows[0][23],
            'unit': rows[0][24],
            'status': status_text,
            'ok': ok,
            'threshold_critical': rows[0][16],
            'threshold_high': rows[0][17],
            'threshold_medium': rows[0][18],
            'threshold_low': rows[0][19],
            'threshold_critical_text': rows[0][2],
            'threshold_high_text': rows[0][3],
            'threshold_medium_text': rows[0][4],
            'threshold_low_text': rows[0][5],
            'ack': rows[0][7],
            'ack_endtime': rows[0][9],
            'ack_message': rows[0][10],
            'ack_user': rows[0][11],
            'downtime': rows[0][15],
            'downtime_starttime': rows[0][12],
            'downtime_endtime': rows[0][13],
            'downtime_user': rows[0][14],
            'enabled': rows[0][20],
            'data_json': data_json,
            'key': rows[0][21],
            'value': formatted_data['value_text'],
            'metrics': formatted_data['metrics_text'],
            'unit_text': formatted_data['unit_text'],
        }

    except Exception as exc:
        print(str(exc))

    return unit_data

def secondq_load_unit_chart_data(p_database_object, p_data):
    chart_data = None
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        datasets = [[],[],[],[]]
        labels = []
        annotations = []

        # Retrieving thresholds
        cur.execute("""
        SELECT su_threshold_critical,
               su_threshold_high,
               su_threshold_medium,
               su_threshold_low,
               unit_type
        FROM {0}.server_unit su
        INNER JOIN {0}.unit u ON su.unit_id = u.unit_id
        INNER JOIN {0}.server s ON su.server_id = s.server_id
        WHERE su.su_id = {1}
        """.format(SCHEMA,p_data['p_su_id']))
        rows = cur.fetchall()

        if len(rows) > 0:
            unit_type = rows[0][4]

            if rows[0][0] != None:
                annotations.append(
                {
                    "drawTime": "afterDatasetsDraw",
                    "type": "line",
                    "mode": "horizontal",
                    "scaleID": "y-axis-0",
                    "value": rows[0][0],
                    "borderColor": "rgb(255, 0, 0)",
                    "borderWidth": 1,
                    "borderDash": [2, 2]
                }
                )
            if rows[0][1] != None:
                annotations.append(
                {
                    "drawTime": "afterDatasetsDraw",
                    "type": "line",
                    "mode": "horizontal",
                    "scaleID": "y-axis-0",
                    "value": rows[0][1],
                    "borderColor": "rgb(255, 153, 0)",
                    "borderWidth": 1,
                    "borderDash": [2, 2]
                }
                )
            if rows[0][2] != None:
                annotations.append(
                {
                    "drawTime": "afterDatasetsDraw",
                    "type": "line",
                    "mode": "horizontal",
                    "scaleID": "y-axis-0",
                    "value": rows[0][2],
                    "borderColor": "rgb(255, 224, 0)",
                    "borderWidth": 1,
                    "borderDash": [2, 2]
                }
                )
            if rows[0][3] != None:
                annotations.append(
                {
                    "drawTime": "afterDatasetsDraw",
                    "type": "line",
                    "mode": "horizontal",
                    "scaleID": "y-axis-0",
                    "value": rows[0][3],
                    "borderColor": "rgb(74, 134, 232)",
                    "borderWidth": 1,
                    "borderDash": [2, 2]
                }
                )

            v_filter = "su_id = {0} ".format(p_data['p_su_id'])

            if 'p_start_time' in p_data and p_data['p_start_time'] != '':
                v_filter = v_filter + " AND sud_time >= '{0}' ".format(p_data['p_start_time'])

            if 'p_end_time' in p_data and p_data['p_end_time'] != '':
                v_filter = v_filter + " AND sud_time <= '{0}' ".format(p_data['p_end_time'])

            cur.execute("""
            SELECT to_char(sud_time, 'YYYY-MM-dd HH24:00:00'),
            sud_min,
            sud_average,
            sud_max
            FROM {0}.aggregation_data
            WHERE {1}
            ORDER BY sud_time
            """.format(SCHEMA,v_filter))

            #if unit_type == 'value':
            #    cur.execute("""
            #    SELECT to_char(sud_time, 'YYYY-MM-dd HH24:00:00') AS time,
            #    min((sud_data->'value')::float),
            #    round(avg((sud_data->'value')::float)::numeric,2),
            #    max((sud_data->'value')::float),
            #    sud.server_id,
            #    sud.unit_id,
            #    sud.customer_id
            #    FROM {0}.server_unit_data sud
            #    INNER JOIN {0}.customer c ON sud.customer_id = c.customer_id
            #    INNER JOIN {0}.server s ON sud.server_id = s.server_id
            #    INNER JOIN {0}.unit u ON sud.unit_id = u.unit_id
            #    WHERE {1}
            #      AND sud_data->>'value' is not null
            #    GROUP BY sud.customer_id,
            #             sud.server_id,
            #             sud.unit_id,
            #             to_char(sud_time, 'YYYY-MM-dd HH24:00:00')
            #    ORDER BY time
            #    """.format(SCHEMA,v_filter))
            #else:
            #    cur.execute("""
            #    SELECT time,
            #           min(value::float),
            #           round(avg(value::float)::numeric,2),
            #           max(value::float),
            #           customer_id,
            #           server_id,
            #           unit_id
            #    FROM (
            #    SELECT to_char(sud_time, 'YYYY-MM-dd HH24:00:00') AS time,
            #    CASE (sud_data->>'value')::boolean WHEN true THEN 0
            #    WHEN false THEN 1 END AS value,
            #    sud.server_id,
            #    sud.unit_id,
            #    sud.customer_id
            #    FROM {0}.server_unit_data sud
            #    INNER JOIN {0}.customer c ON sud.customer_id = c.customer_id
            #    INNER JOIN {0}.server s ON sud.server_id = s.server_id
            #    INNER JOIN {0}.unit u ON sud.unit_id = u.unit_id
            #    WHERE {1}
            #      AND sud_data->>'value' is not null) t
            #    GROUP BY customer_id,
            #             server_id,
            #             unit_id,
            #             time
            #    ORDER BY time
            #    """.format(SCHEMA,v_filter))

            rows = cur.fetchall()

            for row in rows:
                labels.append(row[0])
                datasets[0].append(row[1])
                datasets[1].append(row[2])
                datasets[2].append(row[3])
                datasets[3].append(None)

            chart_data = {
                'labels': labels,
                'datasets': datasets,
                'annotations': annotations
            }

    except Exception as exc:
        print(str(exc))

    return chart_data

def secondq_load_customer_list_data(p_database_object, p_data):
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()
        v_filter = ' WHERE 1 = 1 '

        v_page = p_data['page']
        v_num_per_page = 50
        v_num_pages = 0

        if 'input_filter' in p_data and p_data['input_filter']!=None and p_data['input_filter']!='':
            v_filter = v_filter + " AND customer_name like '%{0}%' ".format(p_data['input_filter'])

        #count
        cur.execute("""
        SELECT ceil(count(*)/{0}::numeric)
        FROM (
        SELECT c.customer_name
        FROM {1}.customer c) t
        {2}
        """.format(v_num_per_page,SCHEMA,v_filter))

        rows = cur.fetchall()
        v_num_pages = rows[0][0]

        cur.execute("""
        SELECT *
        FROM (
        SELECT c.customer_id,
               c.customer_name,
               (SELECT count(1) FROM {0}.server s WHERE s.customer_id = c.customer_id ) AS server_count,
               CASE WHEN (SELECT count(*) FROM {0}.server_unit su INNER JOIN {0}.server s ON s.server_id = su.server_id WHERE s.customer_id = c.customer_id AND su.su_state = 'critical' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'critical'
                    WHEN (SELECT count(*) FROM {0}.server_unit su INNER JOIN {0}.server s ON s.server_id = su.server_id WHERE s.customer_id = c.customer_id AND su.su_state = 'high' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'high'
                    WHEN (SELECT count(*) FROM {0}.server_unit su INNER JOIN {0}.server s ON s.server_id = su.server_id WHERE s.customer_id = c.customer_id AND su.su_state = 'unknown' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'unknown'
                    WHEN (SELECT count(*) FROM {0}.server_unit su INNER JOIN {0}.server s ON s.server_id = su.server_id WHERE s.customer_id = c.customer_id AND su.su_state = 'medium' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'medium'
                    WHEN (SELECT count(*) FROM {0}.server_unit su INNER JOIN {0}.server s ON s.server_id = su.server_id WHERE s.customer_id = c.customer_id AND su.su_state = 'low' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'low'
                    WHEN (SELECT count(*) FROM {0}.server_unit su INNER JOIN {0}.server s ON s.server_id = su.server_id WHERE s.customer_id = c.customer_id AND su.su_state = 'ok' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'ok'
               ELSE '' END AS max_severity,
               c.customer_notes
        FROM {0}.customer c) t
        {1}
        ORDER BY customer_name
        LIMIT {2}
        OFFSET {2}*{3}
        """.format(SCHEMA,v_filter,v_num_per_page,v_page))

        rows = cur.fetchall()

        customers_data = []
        customers_status_data = []

        for row in rows:

            customer_cell = '<span class="secondq_link" onclick="secondqCreateCustomerDashboard(' + str(row[0]) + ');">' + row[1] + '</span>'

            customers_data.append(
            [customer_cell,row[2],row[3],row[4]]
            )

            customers_status_data.append(
            {
                'customer_id': row[0],
                'notes': row[4]
            }
            )

    except Exception as exc:
        print(str(exc))

    return {
        'customers_data': customers_data,
        'customers_status_data': customers_status_data,
        'num_pages': int(v_num_pages)
    }

def secondq_load_host_list_data(p_database_object, p_data):
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()
        v_filter = ' WHERE 1 = 1 '

        v_page = 0
        v_num_per_page = 50
        v_num_pages = 0
        v_pagination_text = ''

        if 'p_customer_id' in p_data:
            v_filter = v_filter + " AND customer_id = {0}".format(p_data['p_customer_id'])
        else:
            v_page = p_data['page']
            v_pagination_text = ' LIMIT {0} OFFSET {0}*{1} '.format(v_num_per_page,v_page)

        if 'sel_filter' in p_data and p_data['sel_filter']!=None:
            if p_data['sel_filter']=='1':
                v_filter = v_filter + " AND status = 'up' "
            elif p_data['sel_filter']=='2':
                v_filter = v_filter + " AND (status = 'down' AND ok = false) "
            elif p_data['sel_filter']=='3':
                v_filter = v_filter + " AND (status = 'down' AND ok = true) "
            elif p_data['sel_filter']=='4':
                v_filter = v_filter + " AND su_enabled = true "
            elif p_data['sel_filter']=='5':
                v_filter = v_filter + " AND su_enabled = false "
        if 'input_filter' in p_data and p_data['input_filter']!=None and p_data['input_filter']!='':
            v_filter = v_filter + " AND (customer_name like '%{0}%' OR server_front_name like '%{0}%') ".format(p_data['input_filter'])

        #count
        cur.execute("""
        SELECT ceil(count(*)/{0}::numeric)
        FROM (
        SELECT c.customer_name,
               s.server_front_name,
               CASE WHEN su.su_state = 'ok' THEN 'up'
               ELSE 'down' END AS status,
               CASE WHEN (su.su_downtime = true AND (now() BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime)) OR su.su_acked = true OR su.su_enabled = false THEN true
               ELSE false END AS ok,
               s.customer_id,
               su.su_enabled
        FROM {1}.server s
        LEFT JOIN {1}.server_unit su ON s.server_id = su.server_id AND su.unit_id = (SELECT unit_id FROM {1}.unit WHERE unit_name = 'ping')
        INNER JOIN {1}.customer c ON s.customer_id = c.customer_id) t
        {2}
        """.format(v_num_per_page,SCHEMA,v_filter))

        rows = cur.fetchall()
        v_num_pages = rows[0][0]

        cur.execute("""
        SELECT *
        FROM (
        SELECT c.customer_name,
               s.server_front_name,
               CASE WHEN su.su_state = 'ok' THEN 'up'
               ELSE 'down' END AS status,
               CASE WHEN (su.su_downtime = true AND (now() BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime)) OR su.su_acked = true OR su.su_enabled = false THEN true
               ELSE false END AS ok,
               su.su_downtime AS downtime,
               CASE WHEN su.su_acked = true THEN true
               ELSE false END AS ack,
               {0}.get_elapsed_time(su.su_last_change) as elapsed,
               CASE WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'critical' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'critical'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'high' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'high'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'unknown' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'unknown'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'medium' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'medium'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'low' AND su.su_enabled = true AND (su.su_downtime = false OR (su.su_downtime = true AND (now() NOT BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime))) AND su.su_acked = false ) > 0 THEN 'low'
                    WHEN (SELECT count(*) FROM {0}.server_unit su WHERE su.server_id = s.server_id AND su.su_state = 'ok' AND su.su_enabled = true ) > 0 THEN 'ok'
               ELSE '' END AS max_severity,
               (select string_agg(trim('"'FROM(c1)),', ')
                from (select jsonb_array_elements(server_data->'gathered_data'->'data'->'system'->'ip_list')::text as c1
                from {0}.server where server_id = s.server_id) t where c1 !='"127.0.0.1"') as ip_list,
               s.server_data->'gathered_data'->'data'->'postgresql'->>'role' as role,
               (select string_agg(trim('"'FROM(c1)),', ')
                from (select jsonb_array_elements(server_data->'gathered_data'->'data'->'services')::text as c1
                from {0}.server where server_id = s.server_id) t) as services,
               to_char(su.su_acked_endtime, 'YYYY-mm-dd HH24:MI:SS') as ack_endtime,
               su.su_acked_message,
               to_char(su.su_downtime_starttime, 'YYYY-mm-dd HH24:MI:SS') as downtime_starttime,
               to_char(su.su_downtime_endtime, 'YYYY-mm-dd HH24:MI:SS') as downtime_endtime,
               su.su_acked_user,
               su.su_downtime_user,
               s.server_data->'gathered_data'->'data'->'system'->>'hostname' as hostname,
               s.customer_id,
               s.server_id,
               su.su_enabled
        FROM {0}.server s
        LEFT JOIN {0}.server_unit su ON s.server_id = su.server_id AND su.unit_id = (SELECT unit_id FROM {0}.unit WHERE unit_name = 'ping')
        INNER JOIN {0}.customer c ON s.customer_id = c.customer_id) t
        {1}
        ORDER BY customer_name,
                 server_front_name
        {2}
        """.format(SCHEMA,v_filter,v_pagination_text))

        rows = cur.fetchall()

        current_customer = ''
        current_line = 0
        aggregation_counter = 0
        aggregation_start = 0

        hosts_data = []
        hosts_status_data = []
        aggregation_data = []
        for row in rows:
            status_cell = ''
            actions_cell = ''
            #Ack
            if row[5] == True:
                actions_cell = "<i class='secondq_pointer fas fa-thumbs-up mx-2 secondq_status_icon' onclick='secondqShowAckDetails(\"grid\",{0},this);'></i>".format(current_line)
            #Downtime
            if row[4] == True:
                actions_cell = actions_cell + "<i class='secondq_pointer fas fa-wrench mx-2 secondq_status_icon' onclick='secondqShowDowntimeDetails(\"grid\",{0},this);'></i>".format(current_line)
            #Disabled
            if row[20] == False:
                actions_cell = actions_cell + "<i class='fas fa-power-off mx-2 secondq_status_icon' title='Disabled'></i>".format(current_line)

            #Status
            if row[2] == 'up':
                status_cell = status_cell + "<i class='fas fa-arrow-alt-circle-up secondq_status_text_up'></i>"
            else:
                status_cell = status_cell + "<i class='fas fa-arrow-alt-circle-down secondq_status_text_down'></i>"

            customer_cell = '<span class="secondq_link" onclick="secondqCreateCustomerDashboard(' + str(row[18]) + ');">' + row[0] + '</span>'

            host_cell = '<span class="secondq_link" onclick="secondqCreateHostDashboard(' + str(row[18]) + ',' + str(row[19]) + ');">' + row[1] + '</span>'

            if 'p_customer_id' not in p_data:
                hosts_data.append(
                [customer_cell,host_cell,status_cell,row[6],actions_cell,row[7],row[17],row[8],row[9],row[10]]
                )
            else:
                hosts_data.append(
                [host_cell,status_cell,row[6],actions_cell,row[7],row[17],row[8],row[9],row[10]]
                )

            hosts_status_data.append(
            {
                'status': row[2],
                'ok': row[3],
                'ack_endtime': row[11],
                'ack_message': row[12],
                'ack_user': row[15],
                'downtime_starttime': row[13],
                'downtime_endtime': row[14],
                'downtime_user': row[16],
                'customer_id': row[18],
                'host_id': row[19]
            }
            )

            if current_customer == '':
                current_customer = row[0]


            #Aggregation
            if current_customer != row[0]:
                if aggregation_counter > 1:
                    aggregation_data.append(
                    {
                        'row': aggregation_start,
                        'col': 0,
                        'rowspan': aggregation_counter,
                        'colspan': 1
                    }
                    )
                    aggregation_start = current_line
                aggregation_counter = 0
            aggregation_counter = aggregation_counter + 1
            current_customer = row[0]

            current_line = current_line + 1

        if aggregation_counter > 1:
            aggregation_data.append(
            {
                'row': aggregation_start,
                'col': 0,
                'rowspan': aggregation_counter,
                'colspan': 1
            }
            )

    except Exception as exc:
        print(str(exc))

    return {
        'hosts_data': hosts_data,
        'hosts_status_data': hosts_status_data,
        'aggregation_data': aggregation_data,
        'num_pages': int(v_num_pages)
    }

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def get_formatted_metrics(unit_name, server_name, state, min_threshold, last_data):

    value_text = ''
    metrics_text = ''
    unit_text = ''

    if unit_name in [
        'autovacuum_freeze',
        'sequence_values',
        'autovacuum_workers',
        'disk_space',
        'total_connections'
        ]:
        unit_text = '%'
    elif unit_name in [
        'backend_query_time',
        'backend_idle_in_transaction_time',
        'backend_transaction_time',
        'replication_target'
        ]:
        unit_text = 'seconds'
    elif unit_name in [
        'bloat_table',
        'bloat_index'
        ]:
        unit_text = 'x'
    elif unit_name in [
        'replication_source'
        ]:
        unit_text = 'MiB'

    try:
        if state == 'unknown':
            metrics_text = 'No data'
        else:
            metrics_json = json.loads(last_data)
            value_text = str(metrics_json['value'])
            metrics_text = str(metrics_json['message'])

            if metrics_json != None:

                # Check failed and message is not a list, just print the error in the metrics
                if metrics_json['success'] == False and type(metrics_json['message'])!=list:
                    value_text = 'Check failed'
                    metrics_text = str(metrics_json['message'])
                else:
                    if unit_name == 'ping':
                        value_text = 'Up'
                        metrics_text = '{0} is Up'.format(server_name)

                    elif unit_name == 'postgres_connection':
                        if metrics_json['value']['default_value'] == True:
                            value_text = 'Up'
                            metrics_text = 'Connected to PostgreSQL {0}'.format(metrics_json['message']['version'])
                        else:
                            value_text = 'Down'
                            metrics_text = str(metrics_json['message'])

                    elif unit_name == 'inactive_slots':
                        if metrics_json['value']['default_value'] == True:
                            value_text = ''
                            metrics_text = 'No inactive slots'
                        else:
                            value_text = ''
                            metrics_text = '{} inactive slot(s)'.format(len(metrics_json['message']))

                    elif unit_name == 'role_change':
                        if metrics_json['value']['default_value'] == True:
                            value_text = 'Same role'
                            metrics_text = 'Same role: {0}'.format(metrics_json['message']['role'])
                        else:
                            if metrics_json['message']['role']=='primary':
                                value_text = 'Promotion'
                                metrics_text = '{0} promoted to primary'.format(server_name)
                            if metrics_json['message']['role']=='standby':
                                value_text = 'Demotion'
                                metrics_text = '{0} demoted to standby'.format(server_name)

                    elif unit_name == 'replay_paused':
                        if metrics_json['value']['default_value'] == True:
                            value_text = ''
                            metrics_text = 'Replay NOT paused'
                        else:
                            value_text = ''
                            metrics_text = 'Replay paused'

                    elif unit_name == 'autovacuum_workers':
                        value_text = '{0}%'.format(metrics_json['message']['percentage'])
                        metrics_text = '{0} of {1} workers busy; {2}%'.format(metrics_json['message']['workers_busy'],metrics_json['message']['autovacuum_max_workers'],metrics_json['message']['percentage'])

                    elif unit_name == 'total_connections':
                        value_text = '{0}%'.format(metrics_json['message']['percentage'])
                        metrics_text = '{0} of {1} backends used; {2}%'.format(metrics_json['message']['total'],metrics_json['message']['max'],metrics_json['message']['percentage'])

                    elif unit_name == 'sequence_values':
                        value_text = '{0}%'.format(metrics_json['value']['default_value'])
                        num_problems = 0
                        for seq in metrics_json['message']:
                            if min_threshold != None and seq['percentage'] >= min_threshold:
                                num_problems = num_problems + 1
                        metrics_text = '{0} sequences above {1}%; Highest at {2}%'.format(num_problems, min_threshold,metrics_json['value']['default_value'])

                    elif unit_name == 'disk_space':
                        value_text = '{0}%'.format(metrics_json['value']['default_value'])

                        if len(metrics_json['message'])==0:
                            metrics_text = 'No mounts to check'
                        elif len(metrics_json['message'])==1:
                            metrics_text = '{0} of {1} used; {2} free; {3}% used; Mount: {4}'.format(
                                sizeof_fmt(int(metrics_json['message'][0]['used'])*1024),
                                sizeof_fmt(int(metrics_json['message'][0]['total'])*1024),
                                sizeof_fmt(int(metrics_json['message'][0]['available'])*1024),
                                metrics_json['message'][0]['percentage'],
                                metrics_json['message'][0]['mount'])
                        else:
                            num_problems = 0
                            for mount in metrics_json['message']:
                                if min_threshold != None and mount['percentage'] >= min_threshold:
                                    num_problems = num_problems + 1
                            metrics_text = '{0} mounts above {1}%; Highest at {2}%'.format(
                                num_problems,
                                min_threshold,
                                metrics_json['value']['default_value'])

                    elif unit_name == 'autovacuum_freeze':
                        value_text = '{0}%'.format(metrics_json['value']['default_value'])
                        num_problems = 0
                        for table in metrics_json['message']['tables']:
                            if min_threshold != None and table['percentage'] >= min_threshold:
                                num_problems = num_problems + 1
                        metrics_text = '{0} tables above {1}%; Highest age at {2}%; autovacuum_freeze_max_age: {3}'.format(
                            num_problems,
                            min_threshold,
                            metrics_json['value']['default_value'],
                            metrics_json['message']['autovacuum_freeze_max_age'])

                    elif unit_name == 'bloat_table':
                        value_text = '{0}x'.format(metrics_json['value']['default_value'])
                        num_problems = 0
                        total_bloat = 0
                        max_wasted = 0
                        max_bloat = 0
                        for bloat in metrics_json['message']:
                            current_bloat = int(bloat['wasted_space'])
                            total_bloat = total_bloat + current_bloat
                            if min_threshold != None and bloat['bloat'] >= min_threshold:
                                num_problems = num_problems + 1
                            if bloat['bloat'] > max_bloat:
                                max_bloat = bloat['bloat']
                                max_wasted = current_bloat
                        metrics_text = '{0} tables above {1}x; Highest at {2}x / {3}; Total estimated wasted space: {4}'.format(
                            num_problems,
                            min_threshold,
                            metrics_json['value']['default_value'],
                            sizeof_fmt(max_wasted),
                            sizeof_fmt(total_bloat))

                    elif unit_name == 'bloat_index':
                        value_text = '{0}x'.format(metrics_json['value']['default_value'])
                        num_problems = 0
                        total_bloat = 0
                        max_wasted = 0
                        max_bloat = 0
                        for bloat in metrics_json['message']:
                            current_bloat = int(bloat['wasted_space'])
                            total_bloat = total_bloat + current_bloat
                            if min_threshold != None and bloat['bloat'] >= min_threshold:
                                num_problems = num_problems + 1
                            if bloat['bloat'] > max_bloat:
                                max_bloat = bloat['bloat']
                                max_wasted = current_bloat
                        metrics_text = '{0} indexes above {1}x; Highest at {2}x / {3}; Total estimated wasted space: {4}'.format(
                            num_problems,
                            min_threshold,
                            metrics_json['value']['default_value'],
                            sizeof_fmt(max_wasted),
                            sizeof_fmt(total_bloat))

                    elif unit_name == 'locks_exclusive':
                        value_text = '{0}'.format(metrics_json['value']['default_value'])
                        metrics_text = '{0} exclusive lock(s)'.format(metrics_json['value']['default_value'])

                    elif unit_name == 'locks_share':
                        value_text = '{0}'.format(metrics_json['value']['default_value'])
                        metrics_text = '{0} share lock(s)'.format(metrics_json['value']['default_value'])

                    elif unit_name == 'locks_blocked':
                        value_text = '{0}'.format(metrics_json['value']['default_value'])
                        metrics_text = '{0} blocked lock(s)'.format(metrics_json['value']['default_value'])

                    elif unit_name == 'backend_query_time':
                        value_text = '{0} seconds'.format(metrics_json['value']['default_value'])
                        num_problems = 0
                        for query in metrics_json['message']:
                            if min_threshold != None and query['duration'] >= min_threshold:
                                num_problems = num_problems + 1
                        metrics_text = '{0} queries running for more than {1} seconds; Longest: {2} seconds'.format(
                            num_problems,
                            min_threshold,
                            metrics_json['value']['default_value'])

                    elif unit_name == 'backend_transaction_time':
                        value_text = '{0} seconds'.format(metrics_json['value']['default_value'])
                        num_problems = 0
                        for transaction in metrics_json['message']:
                            if min_threshold != None and transaction['duration'] >= min_threshold:
                                num_problems = num_problems + 1
                        metrics_text = '{0} transactions kept open for more than {1} seconds; Longest: {2} seconds'.format(
                            num_problems,
                            min_threshold,
                            metrics_json['value']['default_value'])

                    elif unit_name == 'backend_idle_in_transaction_time':
                        value_text = '{0} seconds'.format(metrics_json['value']['default_value'])
                        num_problems = 0
                        for transaction in metrics_json['message']:
                            if min_threshold != None and transaction['idle_duration'] >= min_threshold:
                                num_problems = num_problems + 1
                        metrics_text = '{0} transactions idle for more than {1} seconds; Longest: {2} seconds'.format(
                            num_problems,
                            min_threshold,
                            metrics_json['value']['default_value'])

                    elif unit_name == 'barman_check':
                        if metrics_json['value']['default_value'] == True:
                            value_text = ''
                            metrics_text = 'All checks are OK'
                        else:
                            value_text = ''
                            metrics_text = 'Barman check FAILED'

                    elif unit_name == 'replication_source':
                        value_text = '{0} seconds'.format(metrics_json['value']['default_value'])
                        metrics_text = ''

                        if metrics_json['success'] == False:
                            value_text = 'Detatched'
                        else:
                            value_text = 'Streaming / Lag={0} MiB'.format(metrics_json['value']['default_value'])

                        for node in metrics_json['message']:
                            if node['monitored']:
                                node_name = '{0}'.format(node['alias'])

                                if not node['connected']:
                                    metrics_text = '{0} {1} detached; '.format(metrics_text, node_name)
                                elif min_threshold != None and node['lag_mb'] >= min_threshold:
                                    metrics_text = '{0} {1} lagging (lag={2} MiB); '.format(metrics_text, node_name,node['lag_mb'])
                                else:
                                    metrics_text = '{0} {1} in sync (lag={2} MiB); '.format(metrics_text, node_name,node['lag_mb'])

                    elif unit_name == 'replication_target':
                        value_text = '{0} seconds'.format(metrics_json['value']['default_value'])
                        metrics_text = 'Last replayed transcation on {0} is {1} seconds old'.format(server_name,metrics_json['value']['default_value'])

    except Exception as exc:
        value_text = ''
        metrics_text = str(exc)

    return {
        'value_text': value_text,
        'metrics_text': metrics_text,
        'unit_text': unit_text
    }

def secondq_load_unit_list_data(p_database_object, p_data):
    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        v_filter = ' WHERE 1 = 1 '

        v_page = 0
        v_num_per_page = 50
        v_num_pages = 0
        v_pagination_text = ''

        if 'p_host_id' in p_data:
            v_filter = v_filter + " AND server_id = {0} ".format(p_data['p_host_id'])
        else:
            v_page = p_data['page']
            v_pagination_text = ' LIMIT {0} OFFSET {0}*{1} '.format(v_num_per_page,v_page)

        if 'sel_filter' in p_data and p_data['sel_filter']!=None:
            if p_data['sel_filter']=='1':
                v_filter = v_filter + " AND su_state = 'ok' "
            elif p_data['sel_filter']=='2':
                v_filter = v_filter + " AND (su_state = 'critical' AND ok = false) "
            elif p_data['sel_filter']=='3':
                v_filter = v_filter + " AND (su_state = 'critical' AND ok = true) "
            elif p_data['sel_filter']=='4':
                v_filter = v_filter + " AND (su_state = 'high' AND ok = false) "
            elif p_data['sel_filter']=='5':
                v_filter = v_filter + " AND (su_state = 'high' AND ok = true) "
            elif p_data['sel_filter']=='6':
                v_filter = v_filter + " AND (su_state = 'medium' AND ok = false) "
            elif p_data['sel_filter']=='7':
                v_filter = v_filter + " AND (su_state = 'medium' AND ok = true) "
            elif p_data['sel_filter']=='8':
                v_filter = v_filter + " AND (su_state = 'low' AND ok = false) "
            elif p_data['sel_filter']=='9':
                v_filter = v_filter + " AND (su_state = 'low' AND ok = true) "
            elif p_data['sel_filter']=='10':
                v_filter = v_filter + " AND (su_state = 'unknown' AND ok = false) "
            elif p_data['sel_filter']=='11':
                v_filter = v_filter + " AND (su_state = 'unknown' AND ok = true) "
            elif p_data['sel_filter']=='12':
                v_filter = v_filter + " AND su_enabled = true "
            elif p_data['sel_filter']=='13':
                v_filter = v_filter + " AND su_enabled = false "
        if 'input_filter' in p_data and p_data['input_filter']!=None and p_data['input_filter']!='':
            v_filter = v_filter + " AND (lower(customer_name) like lower('%{0}%') OR lower(server_front_name) like lower('%{0}%') OR lower(unit_front_name) like lower('%{0}%')) ".format(p_data['input_filter'])

        #count
        cur.execute("""
        SELECT ceil(count(*)/{0}::numeric)
        FROM (
        SELECT CASE WHEN (su.su_downtime = true AND (now() BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime)) OR su.su_acked = true OR su.su_enabled = false THEN true
        ELSE false END AS ok,
        su_state,
        server_front_name,
        customer_name,
        CASE WHEN su.su_key IS NULL THEN
             u.unit_front_name
        ELSE
             u.unit_front_name || ' - ' || su.su_key
        END as unit_front_name,
        s.customer_id,
        s.server_id,
        su.su_enabled
        FROM {1}.server_unit su
        INNER JOIN {1}.unit u on su.unit_id = u.unit_id
        INNER JOIN {1}.server s on su.server_id = s.server_id
        INNER JOIN {1}.customer c on s.customer_id = c.customer_id
        ) t
        {2}
        """.format(v_num_per_page,SCHEMA,v_filter))

        rows = cur.fetchall()
        v_num_pages = rows[0][0]

        cur.execute("""
        SELECT *
        FROM (
        SELECT c.customer_name,
               s.server_front_name,
               u.unit_name,
               su.su_state,
               {0}.get_elapsed_time(su.su_last_change) as time_elapsed,
               su.su_acked,
               to_char(su.su_acked_endtime, 'YYYY-mm-dd HH24:MI:SS'),
               su.su_acked_message,
               su.su_downtime,
               to_char(su.su_downtime_starttime, 'YYYY-mm-dd HH24:MI:SS'),
               to_char(su.su_downtime_endtime, 'YYYY-mm-dd HH24:MI:SS'),
               CASE WHEN (su.su_downtime = true AND (now() BETWEEN su.su_downtime_starttime AND su.su_downtime_endtime)) OR su.su_acked = true OR su.su_enabled = false THEN true
               ELSE false END AS ok,
               coalesce(su.su_threshold_critical::text,'-'),
               coalesce(su.su_threshold_high::text,'-'),
               coalesce(su.su_threshold_medium::text,'-'),
               coalesce(su.su_threshold_low::text,'-'),
               su_last_data::text,
               su.su_acked_user,
               su.su_downtime_user,
               su.su_threshold_critical,
               su.su_threshold_high,
               su.su_threshold_medium,
               su.su_threshold_low,
               u.unit_type,
               CASE WHEN su.su_key IS NULL THEN
                    u.unit_front_name
               ELSE
                    u.unit_front_name || ' - ' || su.su_key
               END as unit_front_name,
               c.customer_id,
               s.server_id,
               su.su_id,
               CASE WHEN su.su_threshold_low IS NOT NULL THEN su.su_threshold_low
                    WHEN su.su_threshold_medium IS NOT NULL THEN su.su_threshold_medium
                    WHEN su.su_threshold_high IS NOT NULL THEN su.su_threshold_high
                    WHEN su.su_threshold_critical IS NOT NULL THEN su.su_threshold_critical
               ELSE null END as min_threshold,
               su.su_enabled,
               su.su_key
        FROM {0}.server_unit su
        INNER JOIN {0}.unit u on su.unit_id = u.unit_id
        INNER JOIN {0}.server s on su.server_id = s.server_id
        INNER JOIN {0}.customer c on s.customer_id = c.customer_id) t
        {1}
        ORDER BY customer_name,
                 server_front_name,
                 unit_name
        {2}
        """.format(SCHEMA,v_filter,v_pagination_text))

        rows = cur.fetchall()

        current_customer = ''
        current_host = ''
        current_line = 0
        aggregation_customer_counter = 0
        aggregation_customer_start = 0
        aggregation_host_counter = 0
        aggregation_host_start = 0

        units_data = []
        units_status_data = []
        aggregation_data = []
        for row in rows:

            customer_name = row[0]
            server_name = row[1]
            unit_name = row[2]
            state = row[3]
            time_elapsed = row[4]
            acked = row[5]
            acked_endtime = row[6]
            acked_message = row[7]
            downtime = row[8]
            downtime_start_time = row[9]
            downtime_end_time = row[10]
            unit_handled = row[11]
            threshold_critical_text = row[12]
            threshold_high_text = row[13]
            threshold_medium_text = row[14]
            threshold_low_text = row[15]
            last_data = row[16]
            acked_user = row[17]
            downtime_user = row[18]
            threshold_critical = row[19]
            threshold_high = row[20]
            threshold_medium = row[21]
            threshold_low = row[22]
            unit_type = row[23]
            unit_front_name = row[24]
            customer_id = row[25]
            server_id = row[26]
            su_id = row[27]
            min_threshold = row[28]
            enabled = row[29]
            key = row[30]

            # Create custom visualization for each type of unit
            value_text = ''
            metrics_text = ''

            formatted_data = get_formatted_metrics(unit_name, server_name, state, min_threshold, last_data)


            actions_cell = ''
            #Ack
            if row[5] == True:
                actions_cell = "<i class='fas fa-thumbs-up mx-2 secondq_status_icon' onclick='secondqShowAckDetails(\"grid\",{0},this);'></i>".format(current_line)
            #Downtime
            if row[8] == True:
                actions_cell = actions_cell + "<i class='fas fa-wrench mx-2 secondq_status_icon' onclick='secondqShowDowntimeDetails(\"grid\",{0},this);'></i>".format(current_line)
            #Disabled
            if enabled == False:
                actions_cell = actions_cell + "<i class='fas fa-power-off mx-2 secondq_status_icon' title='Disabled'></i>".format(current_line)

            threshold_text = '{0} / {1} / {2} / {3} {4}'.format(threshold_critical_text,threshold_high_text,threshold_medium_text,threshold_low_text,formatted_data['unit_text'])

            unit_cell = '<span class="secondq_link" onclick="secondqCreateUnitDashboard({1},{2},{3});">{0}</span>'.format(unit_front_name,str(customer_id),str(server_id),str(su_id))

            if 'p_host_id' not in p_data:
                customer_cell = '<span class="secondq_link" onclick="secondqCreateCustomerDashboard({1});">{0}</span>'.format(customer_name,str(customer_id))
                host_cell = '<span class="secondq_link" onclick="secondqCreateHostDashboard({1},{2});">{0}</span>'.format(server_name,str(customer_id),str(server_id))
                units_data.append([customer_cell,host_cell,unit_cell,state,time_elapsed,actions_cell,threshold_text,formatted_data['value_text'],formatted_data['metrics_text']])
            else:
                units_data.append([unit_cell,state,time_elapsed,actions_cell,threshold_text,formatted_data['value_text'],formatted_data['metrics_text']])

            units_status_data.append(
            {
                'status': state,
                'ok': unit_handled,
                'ack_endtime': acked_endtime,
                'ack_message': acked_message,
                'ack_user': acked_user,
                'downtime_starttime': downtime_start_time,
                'downtime_endtime': downtime_end_time,
                'downtime_user': downtime_user,
                'threshold_critical': threshold_critical,
                'threshold_high': threshold_high,
                'threshold_medium': threshold_medium,
                'threshold_low': threshold_low,
                'customer_id': customer_id,
                'host_id': server_id,
                'su_id': su_id,
                'key': key
            }
            )

            if current_customer == '':
                current_customer = row[0]
            if current_host == '':
                current_host = row[1]

            #Aggregation Customer
            if current_customer != row[0]:
                if aggregation_customer_counter > 1:
                    aggregation_data.append(
                    {
                        'row': aggregation_customer_start,
                        'col': 0,
                        'rowspan': aggregation_customer_counter,
                        'colspan': 1
                    }
                    )
                    aggregation_customer_start = current_line
                aggregation_customer_counter = 0
            aggregation_customer_counter = aggregation_customer_counter + 1
            current_customer = row[0]

            #Aggregation Host
            if current_host != row[1]:
                if aggregation_host_counter > 1:
                    aggregation_data.append(
                    {
                        'row': aggregation_host_start,
                        'col': 1,
                        'rowspan': aggregation_host_counter,
                        'colspan': 1
                    }
                    )
                    aggregation_host_start = current_line
                aggregation_host_counter = 0
            aggregation_host_counter = aggregation_host_counter + 1
            current_host = row[1]

            current_line = current_line + 1

        if aggregation_customer_counter > 1:
            aggregation_data.append(
            {
                'row': aggregation_customer_start,
                'col': 0,
                'rowspan': aggregation_customer_counter,
                'colspan': 1
            }
            )

        if aggregation_host_counter > 1:
            aggregation_data.append(
            {
                'row': aggregation_host_start,
                'col': 1,
                'rowspan': aggregation_host_counter,
                'colspan': 1
            }
            )

    except Exception as exc:
        print(str(exc))

    return {
        'units_data': units_data,
        'units_status_data': units_status_data,
        'aggregation_data': aggregation_data,
        'num_pages': int(v_num_pages)
    }

def acknowledge_units(p_database_object, p_data):

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        if 'su_id' not in p_data['rows'][0]:
            for row in p_data['rows']:

                #Generate event
                event_data = {
                    "type": "ack",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": None,
                        "message": p_data['message'],
                        "end_time": p_data['time'],
                        "user": p_data['omnidb_user']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_acked = true,
                su_acked_endtime = '{1}',
                su_acked_message = '{2}',
                su_acked_user = '{3}'
                WHERE server_id = {4}
                """.format(SCHEMA,p_data['time'],p_data['message'],p_data['omnidb_user'],row['server_id']))
        #units
        else:
            for row in p_data['rows']:

                #Generate event
                event_data = {
                    "type": "ack",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": row['su_id'],
                        "message": p_data['message'],
                        "end_time": p_data['time'],
                        "user": p_data['omnidb_user']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_acked = true,
                su_acked_endtime = '{1}',
                su_acked_message = '{2}',
                su_acked_user = '{3}'
                WHERE su_id = {4}
                """.format(SCHEMA,p_data['time'],p_data['message'],p_data['omnidb_user'],row['su_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def change_customer_token(p_database_object, p_data):

    if not p_data['omnidb_user_superuser']:
        result = {
            'error': True,
            'message': "You need superuser privileges to change a unit's key."
        }
        return result

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        #Generate event
        event_data = {
            "type": "customer_token_change",
            "data": {
                "customer_id": p_data['customer_id']
            }
        }
        cur.execute("""
        INSERT INTO {0}.event_list(event_time, data)
        VALUES (
        now(),
        '{1}'
        );
        """.format(SCHEMA,json.dumps(event_data)))

        cur.execute("""
        UPDATE {0}.customer SET
        customer_token = (SELECT {0}.random_string(32))
        WHERE customer_id = {1}
        """.format(SCHEMA,p_data['customer_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def change_host_token(p_database_object, p_data):

    if not p_data['omnidb_user_superuser']:
        result = {
            'error': True,
            'message': "You need superuser privileges to change a unit's key."
        }
        return result

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        #Generate event
        event_data = {
            "type": "host_token_change",
            "data": {
                "customer_id": p_data['customer_id'],
                "server_id": p_data['host_id']
            }
        }
        cur.execute("""
        INSERT INTO {0}.event_list(event_time, data)
        VALUES (
        now(),
        '{1}'
        );
        """.format(SCHEMA,json.dumps(event_data)))

        cur.execute("""
        UPDATE {0}.server SET
        server_token = (SELECT {0}.random_string(32))
        WHERE server_id = {1}
        """.format(SCHEMA,p_data['host_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def change_notes_customer(p_database_object, p_data):

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        cur.execute("""
        UPDATE {0}.customer SET
        customer_notes = '{1}'
        WHERE customer_id = {2}
        """.format(SCHEMA,p_data['notes'],p_data['rows'][0]['customer_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def change_key_unit(p_database_object, p_data):

    if not p_data['omnidb_user_superuser']:
        result = {
            'error': True,
            'message': "You need superuser privileges to change a unit's key."
        }
        return result

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        if p_data['new_key'] == None:
            v_new_key_text = ""
            v_new_key_data = "null"
        else:
            v_new_key_text = p_data['new_key']
            v_new_key_data = "'{0}'".format(p_data['new_key'])

        if p_data['old_key'] == None:
            v_old_key_text = ""
        else:
            v_old_key_text = p_data['old_key']

        #Generate event
        event_data = {
            "type": "unit_key_change",
            "data": {
                "customer_id": p_data['rows'][0]['customer_id'],
                "server_id": p_data['rows'][0]['server_id'],
                "su_id": p_data['rows'][0]['su_id'],
                "new_key": v_new_key_text,
                "old_key": v_old_key_text
            }
        }
        cur.execute("""
        INSERT INTO {0}.event_list(event_time, data)
        VALUES (
        now(),
        '{1}'
        );
        """.format(SCHEMA,json.dumps(event_data)))

        cur.execute("""
        UPDATE {0}.server_unit SET
        su_key = {1}
        WHERE su_id = {2}
        """.format(SCHEMA,v_new_key_data,p_data['rows'][0]['su_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def enable_units(p_database_object, p_data):

    if not p_data['omnidb_user_superuser']:
        result = {
            'error': True,
            'message': 'You need superuser privileges to enable or disable units.'
        }
        return result

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        if 'su_id' not in p_data['rows'][0]:
            for row in p_data['rows']:

                #Generate event
                event_data = {
                    "type": "enable_unit",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": None
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_enabled = true
                WHERE server_id = {1}
                """.format(SCHEMA,row['server_id']))
        #units
        else:
            for row in p_data['rows']:

                #Generate event
                event_data = {
                    "type": "enable_unit",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": row['su_id']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_enabled = true
                WHERE su_id = {1}
                """.format(SCHEMA,row['su_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def disable_units(p_database_object, p_data):

    if not p_data['omnidb_user_superuser']:
        result = {
            'error': True,
            'message': 'You need superuser privileges to enable or disable units.'
        }
        return result

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        if 'su_id' not in p_data['rows'][0]:
            for row in p_data['rows']:

                #Generate event
                event_data = {
                    "type": "disable_unit",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": None
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_enabled = false
                WHERE server_id = {1}
                """.format(SCHEMA,row['server_id']))
        #units
        else:
            for row in p_data['rows']:

                #Generate event
                event_data = {
                    "type": "disable_unit",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": row['su_id']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_enabled = false
                WHERE su_id = {1}
                """.format(SCHEMA,row['su_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def remove_acknowledge_units(p_database_object, p_data):

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        if 'su_id' not in p_data['rows'][0]:
            for row in p_data['rows']:

                #Generate event
                event_data = {
                    "type": "remove_ack",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": None,
                        "user": p_data['omnidb_user']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_acked = false,
                su_acked_endtime = null,
                su_acked_message = null,
                su_acked_user = null
                WHERE server_id = {1}
                """.format(SCHEMA,row['server_id']))
        #units
        else:
            for row in p_data['rows']:

                #Generate event
                event_data = {
                    "type": "remove_ack",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": row['su_id'],
                        "user": p_data['omnidb_user']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_acked = false,
                su_acked_endtime = null,
                su_acked_message = null,
                su_acked_user = null
                WHERE su_id = {1}
                """.format(SCHEMA,row['su_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def downtime_units(p_database_object, p_data):

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        if 'su_id' not in p_data['rows'][0]:
            for row in p_data['rows']:
                #Generate event
                event_data = {
                    "type": "downtime",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": None,
                        "start_time": p_data['start_time'],
                        "end_time": p_data['end_time'],
                        "user": p_data['omnidb_user']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_downtime = true,
                su_downtime_starttime = '{1}',
                su_downtime_endtime = '{2}',
                su_downtime_user = '{3}'
                WHERE server_id = {4}
                """.format(SCHEMA,p_data['start_time'],p_data['end_time'],p_data['omnidb_user'],row['server_id']))
        #units
        else:
            for row in p_data['rows']:
                #Generate event
                event_data = {
                    "type": "downtime",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": row['su_id'],
                        "start_time": p_data['start_time'],
                        "end_time": p_data['end_time'],
                        "user": p_data['omnidb_user']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_downtime = true,
                su_downtime_starttime = '{1}',
                su_downtime_endtime = '{2}',
                su_downtime_user = '{3}'
                WHERE su_id = {4}
                """.format(SCHEMA,p_data['start_time'],p_data['end_time'],p_data['omnidb_user'],row['su_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def remove_downtime_units(p_database_object, p_data):

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        if 'su_id' not in p_data['rows'][0]:
            for row in p_data['rows']:
                #Generate event
                event_data = {
                    "type": "remove_downtime",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": None,
                        "user": p_data['omnidb_user']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_downtime = false,
                su_downtime_starttime = null,
                su_downtime_endtime = null,
                su_downtime_user = null
                WHERE server_id = {1}
                """.format(SCHEMA,row['server_id']))
        #units
        else:
            for row in p_data['rows']:
                #Generate event
                event_data = {
                    "type": "remove_downtime",
                    "data": {
                        "customer_id": row['customer_id'],
                        "server_id": row['server_id'],
                        "su_id": row['su_id'],
                        "user": p_data['omnidb_user']
                    }
                }
                cur.execute("""
                INSERT INTO {0}.event_list(event_time, data)
                VALUES (
                now(),
                '{1}'
                );
                """.format(SCHEMA,json.dumps(event_data)))

                cur.execute("""
                UPDATE {0}.server_unit SET
                su_downtime = false,
                su_downtime_starttime = null,
                su_downtime_endtime = null,
                su_downtime_user = null
                WHERE su_id = {1}
                """.format(SCHEMA,row['su_id']))

        conn.commit()

        result = {
        }

    except Exception as exc:
        print(str(exc))

    return result

def threshold_generate_event(p_data, p_mode, p_cur, p_row):
    if p_row['thresholds'][p_mode] != None:
        #Generate event
        old_value = ''
        if p_row['thresholds'][p_mode]['old']!=None:
            old_value = p_row['thresholds'][p_mode]['old']
        new_value = ''
        if p_row['thresholds'][p_mode]['new']!=None:
            new_value = p_row['thresholds'][p_mode]['new']

        event_data = {
            "type": "threshold_change",
            "data": {
                "customer_id": p_row['customer_id'],
                "server_id": p_row['server_id'],
                "su_id": p_row['su_id'],
                "severity": p_mode.lower(),
                "old": old_value,
                "new": new_value,
                "user": p_data['omnidb_user']
            }
        }
        p_cur.execute("""
        INSERT INTO {0}.event_list(event_time, data)
        VALUES (
        now(),
        '{1}'
        );
        """.format(SCHEMA,json.dumps(event_data)))

        critical_value = threshold_get_severity_query_value(p_row['thresholds'],'critical')
        high_value = threshold_get_severity_query_value(p_row['thresholds'],'high')
        medium_value = threshold_get_severity_query_value(p_row['thresholds'],'medium')
        low_value = threshold_get_severity_query_value(p_row['thresholds'],'low')

        p_cur.execute("""
        UPDATE {0}.server_unit SET
        su_threshold_critical = {1},
        su_threshold_high = {2},
        su_threshold_medium = {3},
        su_threshold_low = {4}
        WHERE su_id = {5}
        """.format(SCHEMA,critical_value,high_value,medium_value,low_value,p_row['su_id']))

def threshold_get_severity_query_value(p_thresholds,p_mode):
    if p_thresholds[p_mode] != None:
        if p_thresholds[p_mode]['new'].strip() == '':
            return "null"
        else:
            return p_thresholds[p_mode]['new']
    else:
        return "su_threshold_{0}".format(p_mode)

def threshold_units(p_database_object, p_data):

    try:
        conn = psycopg2.connect(MONITORING_DATABASE)
        cur = conn.cursor()

        for row in p_data['rows']:

            threshold_generate_event(p_data,'critical', cur, row)
            threshold_generate_event(p_data,'high', cur, row)
            threshold_generate_event(p_data,'medium', cur, row)
            threshold_generate_event(p_data,'low', cur, row)

            conn.commit()

        result = {
            'error': False
        }

    except Exception as exc:
        print(str(exc))

    return result
