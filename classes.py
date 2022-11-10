

import conf
import datetime
import os
import json
import requests
import gzip
import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
import gate_api
from gate_api.exceptions import ApiException, GateApiException
from decimal import Decimal, ROUND_FLOOR

class AG():
    def __init__(self):
        self.config = gate_api.Configuration(key=conf.key, secret=conf.secret)
        self.client = gate_api.ApiClient(self.config)
        self.future = gate_api.FuturesApi(self.client)

    def get_position(self, contract):
        '''
        получить позицию по определённому контракту
        https://github.com/gateio/gateapi-python/blob/master/docs/FuturesApi.md#get_position
        :return:
        {'adl_ranking': 5,
         'close_order': None,
         'contract': 'DOT_USDT',
         'cross_leverage_limit': '0',
         'entry_price': '6.6418',           средняя цена входа
         'history_pnl': '-0.1909881972',
         'history_point': '0',
         'last_close_pnl': '0.00601015',
         'leverage': '0',
         'leverage_max': '20',
         'liq_price': '0',
         'maintenance_rate': '0.025',
         'margin': '41.10001075514',
         'mark_price': '6.6604',             цена маркировки
         'mode': 'single',
         'pending_orders': 0,                заказы вожидании(лимтные)
         'realised_pnl': '-0.0033209',
         'realised_point': '0',
         'risk_limit': '500000',
         'size': 1,                          количество контрактов в позиции если (-) -short позиция
         'unrealised_pnl': '0.0186',
         'user': 4084077,
         'value': '6.6604'}                  стоимость позиции
        '''

        return self.future.get_position(settle=conf.base_currency, contract=contract)

    # получаем список последних свечей по контракту
    def list_futures_candlesticks(self, contract, interval=conf.tf, limit=500):
        '''
        Получаем список свечей
        https://github.com/gateio/gateapi-python/blob/master/docs/FuturesApi.md#list_futures_candlesticks
        :param contract: торговая пара ('ADA_USDT')
        :return:
                'c': '0.34818',
                'h': '0.34912',
                'l': '0.34752',
                'o': '0.34861',
                't': 1666227600.0,
                'v': 13666
        '''
        return self.future.list_futures_candlesticks(settle=conf.base_currency, contract=contract,
                                                     limit=limit, interval=interval)

    # Получаем информацию об конкретном контракте
    def get_futures_contract(self, contract):
        '''
        Получаем информацию об конкретном контракте
        https://github.com/gateio/gateapi-python/blob/master/docs/FuturesApi.md#get_futures_contract
        :param contract:
        :return:
        {'config_change_time': 1667444588.0,
         'funding_interval': 28800,
         'funding_next_apply': 1667750400.0,
         'funding_rate': '0.000053',
         'in_delisting': False,
         'index_price': '1.9416',
         'last_price': '1.94',
         'leverage_max': '20',                  Максимальное кредитное плечо
         'leverage_min': '1',
         'maintenance_rate': '0.025',
         'maker_fee_rate': '-0.000152',
         'mark_price': '1.942',                 Текущая цена маржи
         'mark_price_round': '0.001',
         'mark_type': 'index',
         'name': 'DYDX_USDT',
         'order_price_deviate': '0.5',
         'order_price_round': '0.001',         Шаг минимальной цены заказа
         'order_size_max': 1000000,
         'order_size_min': 1,                  Минимальный размер заказа, разрешенный контрактом
         'orderbook_id': 1845063984,
         'orders_limit': 50,
         'position_size': 60133297,
         'quanto_multiplier': '0.1',            Множитель, используемый при конвертации валюты
         'ref_discount_rate': '0',
         'ref_rebate_rate': '0.2',
         'risk_limit_base': '500000',
         'risk_limit_max': '5000000',
         'risk_limit_step': '500000',
         'taker_fee_rate': '0.00075',
         'trade_id': 5779215,
         'trade_size': 4027559888,
         'type': 'direct'}
        '''
        return self.future.get_futures_contract(settle=conf.base_currency, contract=contract)

    # Выставляем ордер по рынку
    def create_futures_order(self, side, contract, size):
        '''
            Создать фьючерсный ордер
            https://github.com/gateio/gateapi-python/blob/master/docs/FuturesApi.md#create_futures_order
            :param side:
            :return:
            {'auto_size': None,
             'close': False,
             'contract': 'DOT_USDT',
             'create_time': 1667201990.654,
             'fill_price': '6.6909',
             'finish_as': 'filled',
             'finish_time': 1667201990.654,
             'iceberg': 0,
             'id': 214968443293,
             'is_close': False,
             'is_liq': False,
             'is_reduce_only': False,
             'left': 0,
             'mkfr': '0.00015',
             'price': '0',
             'reduce_only': False,
             'refu': 0,
             'size': -1,
             'status': 'finished',
             'text': 'api',
             'tif': 'ioc',
             'tkfr': '0.0005',
             'user': 4084077}
        '''
        if side == 'short':
            size = -1 * size
        futures_order = {'contract': contract,
                         'price': '0',  # если 0 то рыночный ордер
                         'tif': 'ioc',
                         'size': size}
        return self.future.create_futures_order(settle=conf.base_currency, futures_order=futures_order)



class Bot:
    def __init__(self):
        pass

    # Белый список торговых пар
    def whait_list(self):
        wait_l = ['DYDX_USDT', 'SAND_USDT']  # , 'SOL_USDT' , 'SAND_USDT'
        return wait_l

    # Создаём необходимый датафрейм
    def create_df(self, para):
        # получаем список последних свечей по контракту
        data = AG().list_futures_candlesticks(contract=para)
        # преобразуем список в ДатаФрейм
        df = Bot().frame(data)
        # добавляем индикатор CCI
        df = Indicater().cci(df=df)
        # df.to_csv('dat.csv')
        return df

    # преобразуем список в ДатаФрейм
    def frame(self, data):
        t = []
        c = []
        h = []
        l = []
        o = []
        v = []
        for i in data:
            t.append(int(i.t))
            c.append(float(i.c))
            h.append(float(i.h))
            l.append(float(i.l))
            o.append(float(i.o))
            v.append(float(i.v))
        df = pd.DataFrame({'Time': t, 'Close': c, 'High': h, 'Low': l, 'Open': o, 'Volume': v})
        df['Time'] = pd.to_datetime(df.Time, unit='s')
        df.set_index('Time', inplace=True)
        df = df[df.High != df.Low]
        return df

    def debug(self, var, inf):
        time = self.tm() if var == 'debug' else None
        if conf.debug == 'inform':
            if var == 'inform':
                print(inf)
            elif var == 'debug':
                print('\033[32m {} - {} \033[0;0m'.format(time, inf))
            else:
                print('\033[31m {} \033[0;0m'.format(inf))
        if conf.debug == 'debug':
            if var == 'debug':
                print('\033[32m {} - {} \033[0;0m'.format(time, inf))
            else:
                print('\033[31m {} \033[0;0m'.format(inf))
        if conf.debug == 'error':
            if var == 'error':
                print('\033[31m {} \033[0;0m'.format(inf))

    def tm(self):
        """
        :return: Возвращает текущее время в формате ЧЧ:ММ:СС
        """
        return datetime.datetime.now().strftime('%H:%M:%S')

    # Заходим в позицию или создаё дополнительный заказ по рынку . заносим данные заказа в файл
    def create_poz_big(self, par, side):
        size = Bot().usdt_contract(contract=par)
        s = AG().create_futures_order(side=side, contract=par, size=size)  # открываем позицию
        inf = {'id': s.id,
               'contract': s.contract,
               'size': s.size,
               'price': s.fill_price,
               'tkfr': s.tkfr}
        data = []
        if os.path.isfile('{}.json'.format(s.contract)):
            data = Bot().read_json(s.contract)
        data.append(inf)
        Bot().write_json(data, s.contract)
        return True

    # проверяем профит LONG-позиции
    def check_profit_long(self, df, para):
        k = False
        data = Bot().read_json(para)
        orders = len(data)
        Bot().debug('debug', '{}: исполнено заказов - {}'.format(para, orders))
        gen_size = 0  # количество контрактов в ордер
        sum_price = 0  # общая цена в закрываемых ордерах
        average_price = None  # средняя цена входа закрываемых ордеров
        if 0 < orders <= 5:  # если исполненных ордеров от 1 до 5 то закрываем все в профит
            for i in data:
                gen_size += int(i['size'])
                sum_price += float(i['price'])
            average_price = sum_price / orders

        elif 5 < orders:
            orders = 3
            gen_size = float(data[-1]['size']) + float(data[-2]['size']) + float(data[0]['size'])
            average_price = (float(data[0]['price']) + float(data[-2]['price']) + float(data[-1]['price'])) / orders

        navar_price = average_price * conf.navar_long  # желаемая цена продажи серии ордеров
        mimo_price = float(data[-1]['price']) * conf.mimo_long  # цена дозакупа
        Bot().debug('debug', '{}: Профит - {}, Закуп - {}, Серия - {}'
                    .format(para, navar_price, mimo_price, orders))
        if navar_price < df.Close[-1]:
            AG().create_futures_order(side='short', contract=para, size=gen_size)
            if 0 < orders <= 5:
                data = []
            elif 5 < orders:
                data.pop(-1)
                data.pop(-1)
                data.pop(0)
        elif mimo_price > df.Close[-1]:
            s = AG().create_futures_order(side='long', contract=para, size=data[-1]['size'])
            print(s)
            Bot().debug('debug', '{} : дозакуп'.format(para))
            inf = {'id': s.id,
                   'contract': s.contract,
                   'size': s.size,
                   'price': s.fill_price,
                   'tkfr': s.tkfr}
            data.append(inf)
        if len(data) == 0:
            k = True
        Bot().write_json(data=data, para=para)
        return k

    # проверяем профит SHORT-позиции
    def check_profit_short(self, df, para):
        k = False
        data = Bot().read_json(para)
        orders = len(data)
        Bot().debug('debug', '{}: исполнено заказов - {}'.format(para, orders))
        gen_size = 0  # количество контрактов в ордер
        sum_price = 0  # общая цена в закрываемых ордерах
        average_price = None  # средняя цена входа закрываемых ордеров
        if 0 < orders <= 5:  # если исполненных ордеров от 1 до 5 то закрываем все в профит
            for i in data:
                gen_size += int(i['size'])
                sum_price += float(i['price'])
            average_price = sum_price / len(data)
        elif 5 < orders:
            orders = 3
            gen_size = float(data[-1]['size']) + float(data[-2]['size']) + float(data[0]['size'])
            average_price = (float(data[0]['price']) + float(data[-2]['price']) + float(data[-1]['price'])) / orders
        navar_price = average_price * conf.navar_short  # желаемая цена обратной покупки серии ордеров
        mimo_price = float(data[-1]['price']) * conf.mimo_short  # цена дозакупа
        Bot().debug('debug', '{}: Профит - {}, Закуп - {}, Серия - {}'
                    .format(para, navar_price, mimo_price, orders))
        if navar_price > df.Close[-1]:
            AG().create_futures_order(side='long', contract=para, size=abs(gen_size) * -1)
            if 0 < orders <= 5:
                data = []
            elif 5 < orders:
                data.pop(-1)
                data.pop(-1)
                data.pop(0)
        elif mimo_price < df.Close[-1]:
            s = AG().create_futures_order(side='short', contract=para, size=abs(data[-1]['size']))
            print(s)
            Bot().debug('debug', '{} : дозакуп'.format(para))
            inf = {'id': s.id,
                   'contract': s.contract,
                   'size': s.size,
                   'price': s.fill_price,
                   'tkfr': s.tkfr}
            data.append(inf)
        if len(data) == 0:
            k = True
        Bot().write_json(data=data, para=para)
        return k

    # Высчитываем сколько контрактов на указанную сумму
    def usdt_contract(self, contract):
        data = AG().get_futures_contract(contract=contract)
        k = conf.size_usdt / float(data.mark_price) / float(data.quanto_multiplier) * float(data.leverage_max)
        return round(k)

    def read_json(self, para):
        try:
            with open('{}.json'.format(para)) as f:
                data = json.load(f)
        except FileNotFoundError:
            Bot().write_json(data=[], para=para)
        else:
            return data

    def write_json(self, data, para):
        with open('{}.json'.format(para), 'w') as f:
            json.dump(data, f, indent=2)


class Indicater:

    def __init__(self):
        pass

    def cci(self, df:  'pandas.core.frame.DataFrame') -> 'pandas.core.frame.DataFrame':
        df['CCI'] = ta.cci(df.High, df.Low, df.Close, length=20)
        # По 10 свечам определяем восходящий или низходящий тренд
        chandles = 6
        s = [0] * len(df)
        signal = [0] * len(df)
        for i in range(len(df)):
            if df.CCI[i] > df.CCI[i - chandles:i].mean():
                s[i] = 1
            elif df.CCI[i] < df.CCI[i - chandles:i].mean():
                s[i] = -1
        for i in range(len(df)):
            if s[i] == -1 and s[i-1] == 1:
                signal[i] = -1
            if s[i] == 1 and s[i-1] == -1:
                signal[i] = 1
        df['sigCCI'] = signal
        return df
