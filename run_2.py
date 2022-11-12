
import conf

from classes import AG, Bot, Indicater
import time
import os


ag = AG()
bot = Bot()
idr = Indicater()
paras = conf.whait_list
# Проверяем наличие вспомогательных файлов
for i in paras:
    if not os.path.isfile('stock/{}.json'.format(i)):
        bot.write_json([], i)
kol_poz = 0
# Проверяем количество открытых позиций
poz_list = ag.list_position()
for i in poz_list:
    if i.size != 0 and i.contract in paras:
        kol_poz += 1
    else:
        if os.path.isfile('stock/{}.json'.format(i.contract)):
            bot.write_json([], i.contract)


while True:
    if kol_poz <= conf.max_poz:
        for para in paras:
            poz = ag.get_position(contract=para)  # проверяем открыта ли позиция
            if poz.size > 0:  # если уже открыта LONG-позиция
                df = bot.create_df(para=para)  # создаём датафрейм с последними свечами и сигналами индикаторов
                t = bot.check_profit_long(df=df, para=para)
                if t:
                    kol_poz -= 1
            elif poz.size < 0:  # если уже открыта SHORT-позиция
                df = bot.create_df(para=para)  # создаём датафрейм с последними свечами и сигналами индикаторов
                t = bot.check_profit_short(df=df, para=para)
                if t:
                    kol_poz -= 1
    if kol_poz < conf.max_poz:
        for para in paras:
            if kol_poz >= conf.max_poz:
                break
            poz = ag.get_position(contract=para)  # проверяем открыта ли позиция
            if poz.size == 0:
                bot.debug('debug', '{}: Позиция ещё не открыта'.format(para))
                df = bot.create_df(para=para)  # создаём датафрейм с последними свечами и сигналами индикаторов
                if df.sigCCI[-1] == 1:  # если получен сигнал на LONG
                    bot.debug('debug', '{}: Точка входа в LONG'.format(para))
                    # Заходим в позицию по рынку . заносим данные заказа в файл
                    t = bot.create_poz_big(par=para, side='long')
                    if t:
                        kol_poz += 1
                elif df.sigCCI[-1] == -1:  # если получен сигнал на SHORT
                    bot.debug('debug', '{}: Точка входа в SHORT'.format(para))
                    # Заходим в позицию по рынку . заносим данные заказа в файл
                    t = bot.create_poz_big(par=para, side='short')
                    if t:
                        kol_poz += 1

    print('=' * 75)
    time.sleep(conf.sleep)