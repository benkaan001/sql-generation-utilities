
insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_sap_journal_entries_raw','finance_gl_bronze','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_journal_entries_cleaned','finance_gl_silver','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_gl_balance_monthly_agg','finance_gl_gold','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_crm_orders_raw','sales_orders_bronze','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_order_header_cleaned','sales_orders_silver','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_order_details_cleaned','sales_orders_silver','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_sales_revenue_daily_agg','sales_orders_gold','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_email_send_log_raw','marketing_campaign_bronze','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_campaign_touchpoints','marketing_campaign_silver','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_campaign_roi_analysis','marketing_campaign_gold','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_wms_stock_levels_raw','inventory_mgmt_bronze','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');



insert into system_info.t_optimize_nonpartition_table_list(tbl_name,tbl_schema,ignore_partition,zorder_col,run_freq,rec_strt_ts,rec_end_ts,rec_flg,run_parallel_flg,non_partition_tables) values('t_inventory_snapshot_daily','inventory_mgmt_silver','Y','','daily',current_timestamp(), '9999-12-31T00:00:00.000-0600','Y','Y','group1');


