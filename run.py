
import conf

from classes import AG, Bot, Indicater
import time
import os

ag = AG()
bot = Bot()
idr = Indicater()

paras = bot.whait_list()
kol_poz = 0
data = []

while True:
    for para in paras:
        poz = ag.get_position(contract=para)  # проверяем открыта ли позиция
        df = bot.create_df(para=para)  # создаём датафрейм с последними свечами и сигналами индикаторов
        if poz.size == 0 and kol_poz < conf.max_poz:  # если позиция ещё не открыта ищем вход в сделку
            print('kol_poz_21 - {}'.format(kol_poz))
            bot.debug('debug', '{}: Позиция ещё не открыта'.format(para))
            # print('CCI_1_9 - {} : CCI_1 - {}'.format(df.CCI[-10:-1].mean(), df.CCI[-1]))
            if df.sigCCI[-1] == 1:  # если получен сигнал на LONG
                bot.debug('debug', '{}: Точка входа в LONG'.format(para))
                # Заходим в позицию по рынку . заносим данные заказа в файл
                t = bot.create_poz_big(par=para, side='long')
                if t:
                    kol_poz += 1
                    print('kol_poz_30 - {}'.format(kol_poz))
            elif df.sigCCI[-1] == -1:  # если получен сигнал на SHORT
                bot.debug('debug', '{}: Точка входа в SHORT'.format(para))
                # Заходим в позицию по рынку . заносим данные заказа в файл
                t = bot.create_poz_big(par=para, side='short')
                if t:
                    kol_poz += 1
                    print('kol_poz_37 - {}'.format(kol_poz))
        else:
            if os.path.isfile('{}.json'.format(para)):  # проверяем существует ли JSON-файл
                try:
                    data = bot.read_json(para=para)  # читаем
                except ValueError:
                    data = []
                finally:
                    if data == []:  # если файл пустой или в нём пустой список
                        inf = {'id': '',
                           'contract': poz.contract,
                           'size': poz.size,
                           'price': poz.entry_price,
                           'tkfr': ''}
                        data.append(inf)
                        bot.write_json(data=data, para=para)
                    else:  # если файл не пустой то значит ордера выставлял бот
                        pass
        if poz.size > 0:  # если уже открыта LONG-позиция
            # bot.debug('debug', '{}: LONG-позиция уже открыта'.format(para))
            t = bot.check_profit_long(df=df, para=para)
            if t:
                kol_poz -= 1
                print('kol_poz_59 - {}'.format(kol_poz))
        elif poz.size < 0:  # если уже открыта SHORT-позиция
            # bot.debug('debug', '{}: SHORT-позиция уже открыта'.format(para))
            t = bot.check_profit_short(df=df, para=para)
            if t:
                kol_poz -= 1
                print('kol_poz_65 - {}'.format(kol_poz))

    print('=' * 75)
    time.sleep(15)
