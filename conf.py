

# Подключение к API биржи Gate.io

key = '605b74869f0a70931b55e349d5fe5ca2'
secret = '8e8ca04649ba3e0ed9cd7efb635565b7659328453c111921fd4fff0ad509dbde'

debug = 'debug'

base_currency = 'usdt'  # Название базовой монеты('usdt')
tf = '5m'

# Размер позиции в USDT (примерно)
size_usdt = 0.5
# Количество одновременных позиций
max_poz = 1

# Размер прибыли с позиции и размер выставления следующего ордера
navar = 0.5
mimo = 0.5
#####################################
navar_long = 1 + (navar / 100)     #
navar_short = 1 - (navar / 100)   #
mimo_long = 1 - (mimo / 100)     #
mimo_short = 1 + (mimo / 100)   #
################################
