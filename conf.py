

# Подключение к API биржи Gate.io

key = '605b74869f0a70931b55e349d5fe5ca2'
secret = '8e8ca04649ba3e0ed9cd7efb635565b7659328453c111921fd4fff0ad509dbde'

debug = 'debug'

base_currency = 'usdt'  # Название базовой монеты('usdt')
tf = '5m'

# Размер позиции в USDT (примерно)
size_usdt = 0.5
# Количество одновременных позиций
max_poz = 2

# Размер прибыли с позиции и размер выставления следующего ордера
navar = 0.5
mimo = 0.5
#####################################   #####
navar_long = 1 + (navar / 100)     #   #
navar_short = 1 - (navar / 100)   #   #
mimo_long = 1 - (mimo / 100)     #   #
mimo_short = 1 + (mimo / 100)   #   #
################################   #####


'''
бот для торговли на фьючерсах на Gate.io
в файле <classe.py> в методе <whait_list> можно записать торговые пары
на которых бот будет торговать, бот откроет те из их по которым  быстрее
сработает индикатор, но не более <max_poz> из этого файла
Вход в позицию по индикатору <CCI - индекс товарного канала>
настройка CCI <classe.py><Indicater.cci>
 
'''
#dydx
[
  {
    "id": "",
    "contract": "DYDX_USDT",
    "size": 0,
    "price": "0",
    "tkfr": ""
  },
  {
    "id": 221255967035,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.748",
    "tkfr": "0.0005"
  },
  {
    "id": 221282399630,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.76",
    "tkfr": "0.0005"
  },
  {
    "id": 221285879413,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.765",
    "tkfr": "0.0005"
  },
  {
    "id": 221286243036,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.772",
    "tkfr": "0.0005"
  },
  {
    "id": 221295270514,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.783",
    "tkfr": "0.0005"
  },
  {
    "id": 221297743693,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.801",
    "tkfr": "0.0005"
  },
  {
    "id": 221298801539,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.806",
    "tkfr": "0.0005"
  },
  {
    "id": 221299085757,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.843",
    "tkfr": "0.0005"
  },
  {
    "id": 221313396983,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.86",
    "tkfr": "0.0005"
  },
  {
    "id": 221313670550,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.869",
    "tkfr": "0.0005"
  },
  {
    "id": 221316134276,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.889",
    "tkfr": "0.0005"
  },
  {
    "id": 221317138284,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.892",
    "tkfr": "0.0005"
  },
  {
    "id": 221318933759,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.914",
    "tkfr": "0.0005"
  },
  {
    "id": 221319207246,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.926",
    "tkfr": "0.0005"
  },
  {
    "id": 221319566784,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.933",
    "tkfr": "0.0005"
  },
  {
    "id": 221321824259,
    "contract": "DYDX_USDT",
    "size": -57,
    "price": "1.941",
    "tkfr": "0.0005"
  }
]
#sand
[
  {
    "id": "",
    "contract": "SAND_USDT",
    "size": 0,
    "price": "0",
    "tkfr": ""
  },
  {
    "id": 221323920465,
    "contract": "SAND_USDT",
    "size": -15,
    "price": "0.6751",
    "tkfr": "0.0005"
  }
]
