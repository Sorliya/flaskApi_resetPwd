# -*- coding: utf-8 -*-
import hashlib
from .code import CODE_MSG_MAP
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from datetime import date, datetime, timedelta
from pytz import timezone 
import time   
import decimal
import re
import pandas as pd
from passlib.hash import pbkdf2_sha256 as sha256

class JSONEncoder(json.JSONEncoder):
    """
        Custom json serializer
    """
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, decimal.Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)

def generate_hash(password):
    """Generate hashed password

    Args:
        password (string): original password

    Returns:
        string: hashed result
    """
    return sha256.hash(password)

def verify_hash(password, hash):
    """Compare hashed password

    Args:
        password    (_type_): _description_
        hash        (bool): _description_

    Returns:
        _type_: _description_
    """
    return sha256.verify(password, hash)


def pretty_result(code, msg=None, data=None):
    if msg is None:
        msg = CODE_MSG_MAP.get(code)
    return { 'code': code, 'msg': msg, 'data': data }

def hash_md5(data):
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

def get_age(year, month, day):
    now = datetime.now()
    now_year, now_month, now_day = now.year, now.month, now.day

    if year >= now_year:
        return 0
    elif month > now_month or (month == now_month and day > now_day):
        return now_year - year - 1
    else:
        return now_year - year

def time_str_to_int(datetime_str):
    """Convert datetime string to integer

    Args:
        datetime (_type_): _description_

    Returns:
        _type_: _description_
    """
    dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return to_integer(dt)

def to_integer(dt_time):
    return int((dt_time - datetime(1970,1,1)).total_seconds())

def time_to_int(dateobj):
    """Convert datetime to integer

    Args:
        dateobj (datetime): datetime to be converted

    Returns:
        int: datetime in integer format
    """
    total = int(dateobj.strftime('%S'))
    total += int(dateobj.strftime('%M')) * 60
    total += int(dateobj.strftime('%H')) * 60 * 60
    total += (int(dateobj.strftime('%j')) - 1) * 60 * 60 * 24
    total += (int(dateobj.strftime('%Y')) - 1970) * 60 * 60 * 24 * 365
    return total

def get_mt4_time():
    """Get mt4 server time in datatime format

    Returns:
        datetime: server time
    """
    tz = timezone('US/Eastern')
    server_current_time = datetime.now(tz) + timedelta(hours=7)
    return server_current_time

def get_mt4_time_string():
    """Get mt4 server time in string format

    Returns:
        string: server time
    """
    tz = timezone('US/Eastern')
    server_current_time = (datetime.now(tz) + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
    return server_current_time
    
def get_mt4_time_integer():
    """Get mt4 server time in integer format

    Returns:
        int: server current time in seconds
    """
    tz = timezone('US/Eastern')
    server_current_time = datetime.now(tz) + timedelta(hours=7)
    return time_to_int(server_current_time)

def is_weekday_server():
    """Check if current server time is weekday or weekend

    Returns:
        boolean: if in weekday return true, if weekend return false
    """
    weekday = [0,1,2,3,4]
    
    current_time = get_mt4_time()

    if current_time.weekday() in weekday:
        return True

    return False

def is_tue_sat_server():
    """Check if current server time is in between tuesday to saturday

    Returns:
        boolean: if in weekday return true, if weekend return false
    """
    weekday = [1,2,3,4,5]
    
    current_time = get_mt4_time()

    if current_time.weekday() in weekday:
        return True

    return False


def convert_query_result_dict(data):
    """
        Convert queryt result to list of dict
    """
    result = []
    for item in data:
        result.append(dict(zip(list(item._fields), item)))

    return result

def keep_numeric(a):
    return re.sub("[^0-9_.]", "", a)

def process_lp_account(data, lp_name, updated_at):
    
    result = []
    
    if lp_name == 'invast':
        result = pd.DataFrame(json.loads(data))
        
        result = result[['requiredMarginInNative','availableMarginInNative','balance','unrealizedNativePL']]
        result['equity'] = result['balance'].apply(keep_numeric).astype(float) + result['unrealizedNativePL'].apply(keep_numeric).astype(float)
        result['LP'] = 'invast'
        result['Credit'] = None
        result['Margin Utilization %'] = (result['requiredMarginInNative'].apply(keep_numeric).astype(float)/result['availableMarginInNative'].apply(keep_numeric).astype(float))*100
        result.columns = ['Margin','Free Margin','Balance','Unrealized P&L','Equity','LP','Credit','Margin Utilization %']
        for column_name in ['Margin','Free Margin','Balance','Unrealized P&L']:
            result[column_name] = result[column_name].apply(keep_numeric).astype(float)

        result['updated_at'] = updated_at

    if lp_name == 'fxcm':
        result = pd.DataFrame(json.loads(data))
        
        result = result[['balance','grossPL','equity','usdMr','usableMargin','usableMarginPerc']]
        result['LP'] = 'fxcm'
        result['Credit'] = None
        result = result[['LP','balance','Credit','grossPL','equity','usdMr','usableMargin','usableMarginPerc']]
        result.columns = ['LP','Balance','Credit','Unrealized P&L','Equity','Margin','Free Margin','Margin Utilization %']
        result['Margin Utilization %'] = 100 - result['Margin Utilization %']
        result['updated_at'] = updated_at
    
    if lp_name == 'cfh':
        result_cfh = pd.DataFrame(json.loads(data))
        result_cfh = result_cfh[['Balance','CreditLimit','OpenPL','MarginRequirement','Equity','AvailableForMarginTrading']]
        result_cfh['LP'] = 'cfh'
        result_cfh['usableMarginPerc'] = result_cfh['MarginRequirement']*100/result_cfh['Equity']
        result_cfh = result_cfh.round(2)
        result = result_cfh[['LP','Balance','CreditLimit','OpenPL','Equity','MarginRequirement','AvailableForMarginTrading','usableMarginPerc']]
        result.columns = ['LP','Balance','Credit','Unrealized P&L','Equity','Margin','Free Margin','Margin Utilization %']
        result['updated_at'] = updated_at

    if lp_name == 'srw':
        result_srw = pd.DataFrame(json.loads(data))
        result = result_srw[['LP','Balance','Credit','Unrealized P&L','Equity','Margin','Free Margin','Margin Utilization %']]
        result.columns = ['LP','Balance','Credit','Unrealized P&L','Equity','Margin','Free Margin','Margin Utilization %']
        for column_name in ['Balance','Credit','Unrealized P&L','Equity','Margin','Free Margin','Margin Utilization %']:
            result[column_name] = result[column_name].apply(keep_numeric).astype(float)
        
        result = result[result['LP'] == 'Fortuneprime']
        result['updated_at'] = updated_at
            
    if lp_name == 'isprime':
        result_isprime = pd.DataFrame(json.loads(data))
        result_isprime = result_isprime[['collateral','unrealisedPnl','netEquity','requirement','marginExcess','marginUtilisation']]
        result_isprime['LP'] = 'isprime'
        result_isprime['Credit'] = None
        result = result_isprime[['LP','collateral','Credit','unrealisedPnl','netEquity','requirement','marginExcess','marginUtilisation']]
        result.columns = ['LP','Balance','Credit','Unrealized P&L','Equity','Margin','Free Margin','Margin Utilization %']
        result['Margin Utilization %'] = result['Margin Utilization %']*100
        result['updated_at'] = updated_at

    if lp_name == 'lmax':
        result = pd.DataFrame(json.loads(data)['wallets'])
        result['LP'] = 'lmax'
        result = result[['LP', 'credit', 'balance']]
        result.columns = ['LP','Credit', 'Balance']
        result['Unrealized P&L'] = 'N/A'
        result['Equity'] = 'N/A'
        result['Margin'] = 'N/A'
        result['Free Margin'] = 'N/A'
        result['Margin Utilization %'] = 'N/A'
        result['updated_at'] = updated_at

    if lp_name == 'eightcap':
        
        result = pd.DataFrame(json.loads(data))
        result['updated_at'] = updated_at

    if lp_name == 'trademax':
        
        result = pd.DataFrame(json.loads(data))
        result['updated_at'] = updated_at
        result = result[result['LP'] == 'PTS']

    
    if lp_name == 'b2c2':
        data = [json.loads(data)]
        # print("B2C2: ", json.loads(data))
        result = pd.DataFrame(data)
        result['LP'] = 'b2c2'
        result = result[['LP', 'equity', 'margin_requirement', 'margin_usage']]
        result.columns = ['LP','Equity','Margin','Margin Utilization %']
        result['Balance'] = 'N/A'
        result['Credit'] = 'N/A'
        result['Unrealized P&L'] = 'N/A'
        result['Free Margin'] = 'N/A'
        result['updated_at'] = updated_at

    if lp_name == 'cmc':

        result_temp = None
        
        for item in json.loads(data):
            result_temp = item

        result_cmc = pd.DataFrame(result_temp)
        result_cmc = result_cmc[['cash','accountValue','unrealisedProfitAndLoss','positionMargin']]
        
        result_cmc['Credit'] = None
        result_cmc['LP'] = 'cmc'
        result_cmc['Balance'] = result_cmc['cash']
        result_cmc['Equity'] = result_cmc['accountValue']
        
        result_cmc['Free Margin'] = result_cmc['accountValue'] - result_cmc['positionMargin']
        result_cmc['Margin Utilization %'] = result_cmc['positionMargin']/result_cmc['accountValue']
        
        result_cmc['Free Margin'] =  result_cmc['accountValue'] - result_cmc['positionMargin']
        result_cmc['Margin Utilization %'] =  result_cmc['positionMargin']*100/result_cmc['accountValue']

        result = result_cmc[['LP','Balance','Credit','unrealisedProfitAndLoss','Equity','positionMargin','Free Margin','Margin Utilization %']]
        result.columns = ['LP','Balance','Credit','Unrealized P&L','Equity','Margin','Free Margin','Margin Utilization %']
        result['updated_at'] = updated_at
        
    result['Free Margin'] = result['Free Margin'].apply(lambda x: round(x, 2))
    result['Balance'] = result['Balance'].apply(lambda x: round(x, 2))
    result['Margin'] = result['Margin'].apply(lambda x: round(x, 2))
    result['Unrealized P&L'] = result['Unrealized P&L'].apply(lambda x: round(x, 2))
    result['Equity'] = result['Equity'].apply(lambda x: round(x, 2))
    result['Margin Utilization %'] = result['Margin Utilization %'].apply(lambda x: round(x, 2))
    
    result = result.to_dict('records')
    if len(result) == 0:
        return []
    else:
        result = result[0]
    return result
