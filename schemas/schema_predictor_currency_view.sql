CREATE VIEW vw_all_predictors_with_currencies as (select * from ((select date_time as pred_date_time, trade_price_open as pred_trade_price_open, trade_price_close as pred_trade_price_close, symbol as pred_sym from raw_all_trades_predictors WHERE symbol like '% Index' and symbol <> 'ESM9 Index') b LEFT JOIN (select symbol as curr_map_sym, currency from raw_future_curr_mapping) c ON b.pred_sym = c.curr_map_sym) d LEFT JOIN (select date_time as curr_pred_date_time, trade_price_open as curr_pred_trade_price_open, trade_price_close as curr_pred_trade_price_close, symbol as curr_pred_sym from raw_all_trades_predictors) e ON d.currency = e.curr_pred_sym and d.pred_date_time = e.curr_pred_date_time);