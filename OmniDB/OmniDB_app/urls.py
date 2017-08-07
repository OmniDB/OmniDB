from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #LOGIN
    url(r'^$', views.login.index, name='login'),
    url(r'^login/', views.login.index, name='login'),
    url(r'^logout/', views.login.logout, name='logout'),
    url(r'^check_session_message/$', views.login.check_session_message, name='check_session_message'),
    url(r'^sign_in/$', views.login.sign_in, name='sign_in'),

    #CONNECTIONS
    url(r'^connections/', views.connections.index, name='connections'),
    url(r'^get_connections/$', views.connections.get_connections, name='get_connections'),
    url(r'^save_connections/$', views.connections.save_connections, name='save_connections'),
    url(r'^test_connection/$', views.connections.test_connection, name='test_connection'),
    url(r'^select_connection/$', views.connections.select_connection, name='select_connection'),

    #USERS
    url(r'^get_users/$', views.users.get_users, name='get_users'),
    url(r'^new_user/$', views.users.new_user, name='new_user'),
    url(r'^remove_user/$', views.users.remove_user, name='remove_user'),
    url(r'^save_users/$', views.users.save_users, name='save_users'),

    #MONITORING
    url(r'^monitoring/', views.monitoring.index, name='monitoring'),
    url(r'^get_nodes/$', views.monitoring.get_nodes, name='get_nodes'),
    url(r'^new_node/$', views.monitoring.new_node, name='new_node'),
    url(r'^remove_node/$', views.monitoring.remove_node, name='remove_node'),
    url(r'^refresh_node_key/$', views.monitoring.refresh_node_key, name='refresh_node_key'),
    url(r'^save_nodes/$', views.monitoring.save_nodes, name='save_nodes'),
    url(r'^get_alerts/$', views.monitoring.get_alerts, name='get_alerts'),
    url(r'^new_alert/$', views.monitoring.new_alert, name='new_alert'),
    url(r'^remove_alert/$', views.monitoring.remove_alert, name='remove_alert'),
    url(r'^save_alerts/$', views.monitoring.save_alerts, name='save_alerts'),
    url(r'^get_alert_data_list/$', views.monitoring.get_alert_data_list, name='get_alert_data_list'),
    url(r'^view_alert_chart/$', views.monitoring.view_alert_chart, name='view_alert_chart'),
    url(r'^receive_alert_data/', views.monitoring.receive_alert_data, name='receive_alert_data'),

    #WORKSPACE
    url(r'^workspace/', views.workspace.index, name='workspace'),
    url(r'^save_config_user/', views.workspace.save_config_user, name='save_config_user'),
    url(r'^get_database_list/', views.workspace.get_database_list, name='get_database_list'),
    url(r'^renew_password/', views.workspace.renew_password, name='renew_password'),
    url(r'^draw_graph/', views.workspace.draw_graph, name='draw_graph'),
    url(r'^alter_table_data/', views.workspace.alter_table_data, name='alter_table_data'),
    url(r'^save_alter_table/', views.workspace.save_alter_table, name='save_alter_table'),
    url(r'^start_edit_data/', views.workspace.start_edit_data, name='start_edit_data'),
    url(r'^get_completions/', views.workspace.get_completions, name='get_completions'),
    url(r'^get_completions_table/', views.workspace.get_completions_table, name='get_completions_table'),
    url(r'^get_command_list/', views.workspace.get_command_list, name='get_command_list'),
    url(r'^clear_command_list/', views.workspace.clear_command_list, name='clear_command_list'),
    url(r'^indent_sql/', views.workspace.indent_sql, name='indent_sql'),

    #TREE_SNIPPETS
    url(r'^get_node_children/', views.tree_snippets.get_node_children, name='get_node_children'),
    url(r'^get_snippet_text/', views.tree_snippets.get_snippet_text, name='get_snippet_text'),
    url(r'^new_node_snippet/', views.tree_snippets.new_node_snippet, name='new_node_snippet'),
    url(r'^delete_node_snippet/', views.tree_snippets.delete_node_snippet, name='delete_node_snippet'),
    url(r'^save_snippet_text/', views.tree_snippets.save_snippet_text, name='save_snippet_text'),
    url(r'^rename_node_snippet/', views.tree_snippets.rename_node_snippet, name='rename_node_snippet'),

    #TREE
    url(r'^get_tree_info/', views.tree.get_tree_info, name='get_tree_info'),
    url(r'^get_tables/', views.tree.get_tables, name='get_tables'),
    url(r'^get_columns/', views.tree.get_columns, name='get_columns'),
    url(r'^get_pk/', views.tree.get_pk, name='get_pk'),
    url(r'^get_fks/', views.tree.get_fks, name='get_fks'),
    url(r'^get_uniques/', views.tree.get_uniques, name='get_uniques'),
    url(r'^get_indexes/', views.tree.get_indexes, name='get_indexes'),
    url(r'^get_functions/', views.tree.get_functions, name='get_functions'),
    url(r'^get_function_fields/', views.tree.get_function_fields, name='get_function_fields'),
    url(r'^get_function_definition/', views.tree.get_function_definition, name='get_function_definition'),
    url(r'^get_procedures/', views.tree.get_procedures, name='get_procedures'),
    url(r'^get_procedure_fields/', views.tree.get_procedure_fields, name='get_procedure_fields'),
    url(r'^get_procedure_definition/', views.tree.get_procedure_definition, name='get_procedure_definition'),
    url(r'^get_sequences/', views.tree.get_sequences, name='get_sequences'),

    #TREE_POSTGRESQL
    url(r'^get_tree_info_postgresql/', views.tree_postgresql.get_tree_info, name='get_tree_info'),
    url(r'^get_tables_postgresql/', views.tree_postgresql.get_tables, name='get_tables'),
    url(r'^get_schemas_postgresql/', views.tree_postgresql.get_schemas, name='get_schemas'),
    url(r'^get_columns_postgresql/', views.tree_postgresql.get_columns, name='get_columns'),
    url(r'^get_pk_postgresql/', views.tree_postgresql.get_pk, name='get_pk'),
    url(r'^get_fks_postgresql/', views.tree_postgresql.get_fks, name='get_fks'),
    url(r'^get_uniques_postgresql/', views.tree_postgresql.get_uniques, name='get_uniques'),
    url(r'^get_indexes_postgresql/', views.tree_postgresql.get_indexes, name='get_indexes'),
    url(r'^get_functions_postgresql/', views.tree_postgresql.get_functions, name='get_functions'),
    url(r'^get_function_fields_postgresql/', views.tree_postgresql.get_function_fields, name='get_function_fields'),
    url(r'^get_function_definition_postgresql/', views.tree_postgresql.get_function_definition, name='get_function_definition'),
    url(r'^get_sequences_postgresql/', views.tree_postgresql.get_sequences, name='get_sequences'),
    url(r'^get_views_postgresql/', views.tree_postgresql.get_views, name='get_views'),
    url(r'^get_views_columns_postgresql/', views.tree_postgresql.get_views_columns, name='get_views_columns'),
    url(r'^get_view_definition_postgresql/', views.tree_postgresql.get_view_definition, name='get_view_definition'),
    url(r'^get_databases_postgresql/', views.tree_postgresql.get_databases, name='get_databases_postgresql'),
    url(r'^get_tablespaces_postgresql/', views.tree_postgresql.get_tablespaces, name='get_tablespaces_postgresql'),
    url(r'^get_roles_postgresql/', views.tree_postgresql.get_roles, name='get_roles_postgresql'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
