"""
模拟数据结构：
    设备1：（在线）
        终端10：（在线）
            指标1000（104地址=100） 、 指标2000（104地址=200）
        终端20：（在线）
            指标1000（104地址=300）
    设备2：（在线）
        终端30：（离线）
            指标1000（104地址=100）
            指标2000（计算指标）
    设备3：（计算设备）
        终端40：(计算终端）
            指标1000（计算公式=max(设备1终端10指标1000, 设备2终端30指标1000)）
"""
import datetime
import json

import redis

test_formula = {'id': '4', 'formula': '1+1', 'device_id': '2', 'term_id': '30', 'item_id': '2000'}
test_device = {'id': '4', 'name': '测试集中器4', 'ip': '127.0.0.1', 'port': '2407', 'identify': '444', 'status': 'on',
               'protocol': 'iec104'}
test_term = {'id': '40', 'name': '测试终端4', 'address': '44', 'identify': 'term40',
             'protocol': 'dlt645', 'device_id': '1'}
test_item = {'id': '3000', 'name': 'C相电压', 'view_code': '3000', 'func_type': '遥测量'}
test_term_item = {'id': '5', 'term_id': '20', 'item_id': '2000', 'protocol_code': '400', 'base_val': '0',
                  'coefficient': '1'}

formula1 = {'id': '1', 'formula': '1+1', 'device_id': '2', 'term_id': '30', 'item_id': '2000'}
device1 = {'id': '1', 'name': '测试集中器1', 'ip': '127.0.0.1', 'port': '2404', 'status': 'on',
           'identify': '111', 'protocol': 'iec104'}
device2 = {'id': '2', 'name': '测试集中器2', 'ip': '127.0.0.1', 'port': '2405', 'status': 'on',
           'identify': '222', 'protocol': 'iec104'}
device3 = {'id': '3', 'name': '测试集中器3', 'identify': '333', 'protocol': 'formula'}
device_list = [device1, device2, device3]
term10 = {'id': '10', 'name': '测试终端1', 'address': '5', 'identify': 'term10', 'protocol': 'dlt645',
          'device_id': '1'}
term20 = {'id': '20', 'name': '测试终端2', 'address': '6', 'identify': 'term20', 'protocol': 'dlt645',
          'device_id': '1'}
term30 = {'id': '30', 'name': '测试终端3', 'protocol': 'formula', 'device_id': '3'}
item1000 = {'id': '1000', 'name': 'A相电压', 'view_code': '1000', 'func_type': '遥测量'}
item2000 = {'id': '2000', 'name': '继电器开关', 'view_code': '2000', 'func_type': '遥控量'}
item3000 = {'id': '3000', 'name': 'A相电流', 'view_code': '3000', 'func_type': '遥测量'}
item4000 = {'id': '4000', 'name': 'A相谐波含有率', 'view_code': '4000', 'func_type': '遥测量'}
term10_item1000 = {'id': '1', 'term_id': '10', 'item_id': '1000', 'protocol_code': '100', 'code_type': '36',
                   'base_val': '0', 'coefficient': '1'}
term10_item2000 = {'id': '2', 'term_id': '10', 'item_id': '2000', 'protocol_code': '200', 'code_type': '63',
                   'base_val': '0', 'coefficient': '1'}
term20_item1000 = {'id': '3', 'term_id': '20', 'item_id': '1000', 'protocol_code': '100', 'code_type': '63',
                   'base_val': '0', 'coefficient': '1'}
term30_item1000 = {'id': '4', 'term_id': '30', 'item_id': '1000', 'protocol_code': '100', 'code_type': '63',
                   'base_val': '0', 'coefficient': '1'}
device1_term10_item1000 = {
    datetime.datetime(2015, 12, 1, 8, 50, 15, 1).isoformat(): '100',
    datetime.datetime(2015, 12, 1, 8, 50, 15, 2).isoformat(): '101',
    datetime.datetime(2015, 12, 1, 8, 50, 15, 3).isoformat(): '102',
}
device1_term10_item2000 = {
    datetime.datetime(2015, 12, 1, 8, 50, 15, 4).isoformat(): '1',
    datetime.datetime(2015, 12, 1, 8, 50, 15, 5).isoformat(): '0',
    datetime.datetime(2015, 12, 1, 8, 50, 15, 6).isoformat(): '1',
}
device1_term20_item1000 = {
    datetime.datetime(2015, 12, 1, 8, 50, 15, 7).isoformat(): '100',
    datetime.datetime(2015, 12, 1, 8, 50, 15, 8).isoformat(): '101',
    datetime.datetime(2015, 12, 1, 8, 50, 15, 9).isoformat(): '102',
}
device2_term30_item1000 = {
    datetime.datetime(2015, 12, 1, 8, 50, 15, 9): '100',
    datetime.datetime(2015, 12, 1, 8, 50, 15, 10): '101',
    datetime.datetime(2015, 12, 1, 8, 50, 15, 11): '102',
}


def generate():
    redis_client = redis.StrictRedis(db=1, decode_responses=True)
    redis_client.flushdb()
    redis_client.hmset('HS:DEVICE:1', device1)
    redis_client.hmset('HS:DEVICE:2', device2)
    redis_client.hmset('HS:DEVICE:3', device3)
    redis_client.hmset('HS:TERM:10', term10)
    redis_client.hmset('HS:TERM:20', term20)
    redis_client.hmset('HS:TERM:30', term30)
    redis_client.hmset('HS:ITEM:1000', item1000)
    redis_client.hmset('HS:ITEM:2000', item2000)
    redis_client.sadd('SET:DEVICE', 1, 2, 3)
    redis_client.sadd('SET:TERM', 10, 20, 30)
    redis_client.sadd('SET:ITEM', 1000, 2000)
    redis_client.sadd('SET:DEVICE_TERM:1', 10, 20)
    redis_client.sadd('SET:DEVICE_TERM:2', 30)
    redis_client.sadd('SET:TERM_ITEM:10', 1000, 2000)
    redis_client.sadd('SET:TERM_ITEM:20', 1000)
    redis_client.sadd('SET:TERM_ITEM:30', 1000)
    redis_client.hmset('HS:TERM_ITEM:10:1000', term10_item1000)
    redis_client.hmset('HS:TERM_ITEM:10:2000', term10_item2000)
    redis_client.hmset('HS:TERM_ITEM:20:1000', term20_item1000)
    redis_client.hmset('HS:TERM_ITEM:30:1000', term30_item1000)
    redis_client.hmset('HS:MAPPING:IEC104:{DEVICE_ID}:{PROTOCOL_CODE}'.format(
        DEVICE_ID=1, PROTOCOL_CODE=100), term10_item1000)
    redis_client.hmset('HS:MAPPING:IEC104:{DEVICE_ID}:{PROTOCOL_CODE}'.format(
        DEVICE_ID=1, PROTOCOL_CODE=200), term10_item2000)
    redis_client.hmset('HS:MAPPING:IEC104:{DEVICE_ID}:{PROTOCOL_CODE}'.format(
        DEVICE_ID=1, PROTOCOL_CODE=300), term20_item1000)
    redis_client.hmset('HS:MAPPING:IEC104:{DEVICE_ID}:{PROTOCOL_CODE}'.format(
        DEVICE_ID=2, PROTOCOL_CODE=100), term30_item1000)
    redis_client.rpush("LST:DATA_TIME:1:10:1000", *sorted(device1_term10_item1000.keys()))
    redis_client.rpush("LST:DATA_TIME:1:10:2000", *sorted(device1_term10_item2000.keys()))
    redis_client.rpush("LST:DATA_TIME:1:20:1000", *sorted(device1_term20_item1000.keys()))
    redis_client.rpush("LST:DATA_TIME:2:30:1000", *sorted(device2_term30_item1000.keys()))
    redis_client.hmset("HS:DATA:1:10:1000", device1_term10_item1000)
    redis_client.hmset("HS:DATA:1:10:2000", device1_term10_item2000)
    redis_client.hmset("HS:DATA:1:20:1000", device1_term20_item1000)
    redis_client.hmset("HS:DATA:2:30:1000", device2_term30_item1000)
