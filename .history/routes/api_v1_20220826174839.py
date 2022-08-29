# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from resources import auth_user, auth, alert_mandate, alert_fast_trade, alert_trade_on_credit, alert_large_exposure, alert_locking_position, alert_net_volume, alert_profit_taker, alert_watch_list, alert_large_volume
from resources import book, broker, broker_server, trades_routing, frontend_settings, lp, statistic, tick_spread, permission

api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

# api.add_resource(auth_user.AuthUserResource, '/auth-user')
api.add_resource(auth_user.VerifyResource, '/verify')
api.add_resource(auth_user.AuthResource, '/auth')
api.add_resource(auth_user.UserResource, '/user')
api.add_resource(permission.PermissionResource, '/permission')

# api.add_resource(auth.Auth, '/auth')
api.add_resource(book.BookResource, '/book')
api.add_resource(book.PkBookResource, '/book/pk')
api.add_resource(broker.BrokerResource, '/broker')
api.add_resource(broker_server.BrokerServerResource, '/broker-server')
api.add_resource(trades_routing.TradesRoutingResource, '/trades-routing')
api.add_resource(frontend_settings.LayoutAlertResource, '/frontend-settings/layout-alert')

api.add_resource(tick_spread.TickSpreadResource, '/data/tick-spread')

# lp
api.add_resource(lp.LPInfoResource, '/lp/info')
api.add_resource(lp.LPAccountInfoResource, '/lp/account')
api.add_resource(lp.LPPositionResource, '/lp/position')
api.add_resource(lp.LPMappingSymbolResource, '/lp/map-symbol')
api.add_resource(lp.LPPositionRecResource, '/lp/position-rec')

api.add_resource(statistic.StatisticLoginHistory, '/login/history')
api.add_resource(statistic.StatisticLoginSummary, '/login/summary')
api.add_resource(statistic.StatisticSymbolCloseTrades, '/symbol/summary/close')

# alert & config
api.add_resource(alert_large_volume.AlertLargeVolumeResource, '/alert/data/large-volume')
api.add_resource(alert_large_volume.ConfigLargeVolumeResource, '/alert/config/large-volume')

api.add_resource(alert_fast_trade.AlertFastTradeResource, '/alert/data/fast-trade')
api.add_resource(alert_fast_trade.ConfigFastTradeResource, '/alert/config/fast-trade')

api.add_resource(alert_mandate.AlertMandateResource, '/alert/data/mandate')
api.add_resource(alert_mandate.ConfigMandateResource, '/alert/config/mandate')

api.add_resource(alert_net_volume.AlertNetVolumeResource, '/alert/data/net-volume')
api.add_resource(alert_net_volume.ConfigNetVolumeResource, '/alert/config/net-volume')

api.add_resource(alert_profit_taker.AlertProfitTakerResource, '/alert/data/profit-taker')
api.add_resource(alert_profit_taker.ConfigProfitTakerResource, '/alert/config/profit-taker')

api.add_resource(alert_trade_on_credit.AlertTradeOnCreditResource, '/alert/data/trade-on-credit')
api.add_resource(alert_trade_on_credit.ConfigTradeOnCreditResource, '/alert/config/trade-on-credit')

api.add_resource(alert_large_exposure.AlertLargeExposureResource, '/alert/data/large-exposure')
api.add_resource(alert_large_exposure.ConfigLargeExposureResource, '/alert/config/large-exposure')

api.add_resource(alert_locking_position.AlertLockingPositionResource, '/alert/data/locking-position')
api.add_resource(alert_locking_position.ConfigLockingPositionResource, '/alert/config/locking-position')

api.add_resource(alert_watch_list.AlertWatchListResource, '/alert/data/watch-list')
api.add_resource(alert_watch_list.ConfigWatchListResource, '/alert/config/watch-list')

# api.add_resource(tick_spread.TickSpreadResource, '/data/tick-spread')

