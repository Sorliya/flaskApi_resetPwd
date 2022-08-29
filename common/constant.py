# -*- coding: utf-8 -*-
SQL_CONNECTION_STR = "postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}"

SQL_QUERY_SELECT_BROKER_SERVER = '''
    select pkdata.broker_servers.*, (select broker_name from pkdata.broker where id = broker_id) as broker_name
    from pkdata.broker_servers
'''

SQL_QUERY_TRADES_ROUTING = '''
    with cte as (
        select book_id, book_name from pkdata.books
    )
    select pkdata.trades_routing.id as id, server_id, (select server_name from pkdata.broker_servers where id = server_id), priority, filter_login, filter_group, filter_symbol, filter_symbol_group, 
    percentage_a, percentage_b, 
    book_a_id, (select book_name from cte where book_id = book_a_id) as book_a_name,
    book_b_id, (select book_name from cte where book_id = book_b_id) as book_b_name,
    pkdata.trades_routing.created_at, pkdata.trades_routing.updated_at
    from pkdata.trades_routing where server_id = {0} order by priority asc
'''

SQL_QUERY_LP_ACCOUNT_INFO = '''
    select "data", b.lp_name, a.record_time_syd 
    from lp.account_info as a
    inner join lp.lp_info as b on b.id = a.lp_id 
    where 1 = 1 
'''

SQL_QUERY_LP_POSITION_INFO = '''
    select "data", b.lp_id, b.lp_name, a.record_time_syd 
    from lp.position as a
    inner join lp.lp_info as b on b.id = a.lp_id 
    where 1 = 1 
'''

SQL_QUERY_INSERT_TRADES_ROUTING = '''
    INSERT INTO "pkdata"."trades_routing" ("id", "priority", "server_id", "filter_login", "filter_group", "filter_symbol", "filter_symbol_group", "percentage_a", "percentage_b", "book_a_id", "book_b_id", "created_at", "updated_at") VALUES 
'''

SQL_QUERY_LOGIN_APR_DATA = '''
    SELECT record_time, profit, equity, balance, dpm FROM "report"."apr" where login = {0} order by record_time
'''

SQL_QUERY_LOGIN_SUMMARY = '''
    with cte as (
        select login,book,
        cast(equity as float), cast(balance as float), cast(profit as float), 
        LEAD(cast(profit as float), 1) OVER (partition by login ORDER BY record_time desc) as previous_profit,
        cast(volume_usd as float), cast(dpm as float),
        row_number() over (partition by login order by record_time desc) as row_id,
        cast(net_deposit as float), cast(deposit as float), cast(withdraw as float), cast(swaps as float)
        from "report"."apr" where login = {0}
    )

    select book, equity, balance, profit, previous_profit, volume_usd, dpm,
    net_deposit, deposit, withdraw, swaps
    from cte where row_id = 1
'''

SQL_QUERY_CLOSE_TRADES_PROFIT = '''
    with cte as (
        select a.login, a.symbol, a.profit, a.cmd, a.volume, a.open_price, a.close_price, a.open_time, a.close_time,
        (select book_name from pkdata.books where book_id = b.book_a) as book_a_name,
        (select book_name from pkdata.books where book_id = b.book_b) as book_b_name,
        a.profit * b.percentage_a as profit_a, a.profit * b.percentage_b as profit_b,
        b.percentage_a, b.percentage_b
        from report.trade_market as a inner join pkdata.trades_book as b on a.ticket = b.ticket
        where a.symbol like '%{0}%' and date(a.close_time) = '{1}'
    )

    select * from cte where book_a_name = '{2}'
'''


SQL_SEARCH_RAW_ORDER_OPEN = '''
    select 
    a."login", a."ticket", a."symbol", a."cmd", a."volume", a."open_time", a."open_price", a."close_time", a."close_price", a."profit", a."sl", a."tp", a."swaps", a."commission", a."comment", a."reason",
    (select book_name from pkdata.books where book_id = b.book_a) as book_a_name,
    b.percentage_a,
    (select book_name from pkdata.books where book_id = b.book_b) as book_b_name,
    b.percentage_b
    from report.trade_open as a inner join pkdata.trades_book as b 
    on a.ticket = b.ticket
    where 1 = 1
'''

SQL_SEARCH_RAW_ORDER_CLOSE = '''
    select 
    a."login", a."ticket", a."symbol", a."cmd", a."volume", a."open_time", a."open_price", a."close_time", a."close_price", a."profit", a."sl", a."tp", a."swaps", a."commission", a."comment", a."reason",
    (select book_name from pkdata.books where book_id = b.book_a) as book_a_name,
    b.percentage_a,
    (select book_name from pkdata.books where book_id = b.book_b) as book_b_name,
    b.percentage_b
    from report.trade_market as a inner join pkdata.trades_book as b 
    on a.ticket = b.ticket
    where 1 = 1
'''

SQL_SEARCH_RAW_ORDER_CON_LOGIN = ''' and a.login in ({0}) '''
SQL_SEARCH_RAW_ORDER_CON_BOOK = ''' and (select book_name from pkdata.books where book_id = b.book_a) in ({0}) '''
SQL_SEARCH_RAW_ORDER_CON_CMD = ''' and a.cmd in ({0}) '''
SQL_SEARCH_RAW_ORDER_CON_REASON = ''' and a.reason in ({0}) '''
SQL_SEARCH_RAW_ORDER_CON_SYMBOL = ''' and a.symbol = '{0}' '''
SQL_SEARCH_RAW_ORDER_CON_OPEN_FROM = ''' and a.open_time >= '{0}' '''
SQL_SEARCH_RAW_ORDER_CON_OPEN_TO = ''' and a.open_time <= '{0}' '''
SQL_SEARCH_RAW_ORDER_CON_CLOSE_FROM = ''' and a.close_time >= '{0}' '''
SQL_SEARCH_RAW_ORDER_CON_CLOSE_TO = ''' and a.close_time <= '{0}' '''
SQL_SEARCH_ORDER_BY = ''' order by {0} {1}'''
SQL_SEARCH_LIMIT = ''' limit {0} '''


SQL_SEARCH_TRANSACTION= '''
    SELECT a.login, c.group_name as group,
    (select book_name from pkdata.books where book_id = b.book_a) as book,
    sum(
        CASE
            WHEN ((a.cmd = 6) 
                AND (a.profit < 0) 
                AND ((a.comment ~* '^tw-') 
                OR (a.comment ~* '^tw -')
                or (a.comment ~* '^tw_')
                or (a.comment ~* '^Transfer Out'))) 
                THEN profit
            ELSE 0
        END) AS task_withdraw,
    sum(
        CASE
            WHEN ((a.cmd = 6) 
                AND (a.profit < 0) 
                AND ((a.comment ~* '^w-') 
                OR (a.comment ~* '^w -')
                or (a.comment ~* '^w_')
                OR (a.comment ilike '%withdraw%')))
                THEN profit
            ELSE 0
        END) AS withdraw,
    sum(
        CASE
            WHEN ((cmd = 6)
                AND (profit > 0)
                AND ((a.comment ~* '^td-') 
                OR (a.comment ~* '^td -')
                or (a.comment ~* '^td_')
                or (a.comment ~* '^Transfer In'))) 
                THEN profit
            ELSE 0
        END) AS task_deposit,
    sum(
        CASE
            WHEN ((cmd = 6) 
                AND (a.profit > 0) 
                AND ((a.comment ~* '^d-') 
                OR (a.comment ~* '^d -')
                or (a.comment ~* '^d_')
                OR (a.comment ilike '%deposite%')))
                THEN profit
            ELSE 0
        END) AS deposit,
    sum(
        CASE
            WHEN (cmd = 7) 
            THEN profit
            ELSE 0
        END) AS credit

    FROM report.transaction as a 
    left join pkdata.trades_book as b on a.ticket = b.ticket
    left join pkdata.users as c on c.login = a.login
    where c.group_name is not NULL or b.book_a is not null
    and a.open_time >= '{0}' and a.close_time <= '{1}'
    group by a.login, book,c.group_name
    having 1=1
'''

SQL_SEARCH_TRANSACTION_LOGIN = ''' and a.login in ({0}) '''

SQL_SEARCH_TRANSACTION_BOOK = ''' and (select book_name from pkdata.books where book_id = b.book_a) in ({0}) '''

SQL_SELECT_PERMISSION = ''' SELECT id, permission_name, cast(permission as json), created_at, updated_at FROM passport.permission '''