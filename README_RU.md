# MT4ForexParser

[![build](https://travis-ci.org/Tim55667757/MT4ForexParser.svg)](https://travis-ci.org/Tim55667757/MT4ForexParser)
[![pypi](https://img.shields.io/pypi/v/MT4ForexParser.svg)](https://pypi.python.org/pypi/MT4ForexParser)
[![license](https://img.shields.io/pypi/l/MT4ForexParser.svg)](https://github.com/Tim55667757/MT4ForexParser/blob/master/LICENSE)

У всех трейдеров периодически возникает необходимость получить исторические данные по валютам Forex для дальнейшего анализа цен и построения графиков. Чаще всего эти данные поставляются на платной основе, либо вам приходится тратить много времени на ручную выгрузку данных на специальных сайтах.

Однако большинство Forex брокеров работают с торговой платформой MetaTrader 4 и загружают туда данные в специальном бинарном .hst-формате MetaTrader 4 (не в .csv). Этим можно воспользоваться и получить исторические свечи подключившись к серверу брокера в демо-режиме, который есть почти у всех брокеров. При этом сжатый бинарный .hst-файл будет скачан локально в рабочий каталог MetaTrader 4.

Далее можно запустить python-модулем mt4forexparser, который умеет читать файлы формата .hst и сохранять их как текстовый .csv-файл или pandas dataframe. Вы получите таблицу, которая содержит колонки данных в следующей последовательности: "date", "time", "open", "high", "low", "close", "volume". Одна строка — это набор данных для построения одной "японской свечи" (candlestick).

See english readme here: https://github.com/Tim55667757/MT4ForexParser/blob/master/README.md


## Как установить

Проще всего использовать установку через PyPI:
```commandline
pip install mt4forexparser
```

После этого можно проверить установку командой:
```commandline
pip show mt4forexparser
```


## Примеры использования

### Из командной строки

Внутренняя справка по ключам:
```commandline
mt4forexparser --help
```

Вывод:
```
usage: python MT4ForexParser.py [some options] [one command]

Metatrader 4 forex history parser. Read, parse and save history as .csv-file
or pandas dataframe.

optional arguments:
  -h, --help            show this help message and exit
  --mt4-history MT4_HISTORY
                        Option (required): full path to Metatrader 4 forex
                        history file.
  --output OUTPUT       Option: full path to .csv output file. Default is
                        None, mean that returns only pandas dataframe.
  --debug-level DEBUG_LEVEL
                        Option: showing STDOUT messages of minimal debug
                        level, e.g. 10 = DEBUG, 20 = INFO, 30 = WARNING,
                        40 = ERROR, 50 = CRITICAL.
  --parse               Command: read, parse and save mt4-history as pandas
                        dataframe or .csv-file if --output is define.

Process finished with exit code 0
```

Поддерживаются две версии форматов файлов .hst: 400 и 401, они определяются автоматически. Попробуйте проверить работу парсера через командную строку на двух приложенных файлах различного формата: ./tests/EURUSD240_old_format_400.hst и ./tests/EURUSD240_new_format_401.hst.

Команда запуска может быть такая:
```commandline
mt4forexparser --mt4-history ./tests/EURUSD240_old_format_400.hst --output ./tests/EURUSD240_old_format_400.csv --debug-level 10 --parse
```

В случае успеха вы должны получить вывод логов примерно следующего содержания:
```
MT4ForexParser.py   L:118  DEBUG   [2020-07-21 20:47:00,134] MT4 parser started: 2020-07-21 20:47:00
MT4ForexParser.py   L:38   DEBUG   [2020-07-21 20:47:00,134] MT4 history file: [./tests/EURUSD240_old_format_400.hst]
MT4ForexParser.py   L:42   DEBUG   [2020-07-21 20:47:00,171] MT4 history file format version: [400]
MT4ForexParser.py   L:63   INFO    [2020-07-21 20:47:00,334] It was read 5909 rows from file [./tests/EURUSD240_old_format_400.hst]
MT4ForexParser.py   L:64   INFO    [2020-07-21 20:47:00,334] Showing last 3 rows:
MT4ForexParser.py   L:69   INFO    [2020-07-21 20:47:00,339]             date   time     open     high      low    close  volume
MT4ForexParser.py   L:69   INFO    [2020-07-21 20:47:00,339] 5906  2013.10.18  12:00  1.36918  1.37036  1.36690  1.36780    8193
MT4ForexParser.py   L:69   INFO    [2020-07-21 20:47:00,340] 5907  2013.10.18  16:00  1.36779  1.36993  1.36773  1.36795    6639
MT4ForexParser.py   L:69   INFO    [2020-07-21 20:47:00,340] 5908  2013.10.18  20:00  1.36793  1.36849  1.36765  1.36839    1955
MT4ForexParser.py   L:73   INFO    [2020-07-21 20:47:00,383] Forex history saved to .csv-formatted file [./tests/EURUSD240_old_format_400.csv]
MT4ForexParser.py   L:148  DEBUG   [2020-07-21 20:47:00,384] All MT4 parser operations are finished success (summary code is 0).
MT4ForexParser.py   L:153  DEBUG   [2020-07-21 20:47:00,384] MT4 parser work duration: 0:00:00.249747
MT4ForexParser.py   L:154  DEBUG   [2020-07-21 20:47:00,384] MT4 parser work finished: 2020-07-21 20:47:00

Process finished with exit code 0
```

При этом вы получите .csv-файл ./tests/EURUSD240_old_format_400.csv следующего содержания (всего 5909 строк):
```
2009.12.21,00:00,1.4311,1.4347,1.4311,1.4342,5504
2009.12.21,04:00,1.4342,1.4357,1.4327,1.4334,5234
2009.12.21,08:00,1.4334,1.4342,1.428,1.4337,8366
...
2013.10.18,12:00,1.36918,1.37036,1.3669,1.3678,8193
2013.10.18,16:00,1.36779,1.36993,1.36773,1.36795,6639
2013.10.18,20:00,1.36793,1.36849,1.36765,1.36839,1955
```

Аналогично для парсинга файла нового формата:
```commandline
mt4forexparser --mt4-history ./tests/EURUSD240_new_format_401.hst --output ./tests/EURUSD240_new_format_401.csv --debug-level 10 --parse
```

В случае успеха вы получите примерно такой вывод логов:
```
MT4ForexParser.py   L:118  DEBUG   [2020-07-21 20:55:42,594] MT4 parser started: 2020-07-21 20:55:42
MT4ForexParser.py   L:38   DEBUG   [2020-07-21 20:55:42,595] MT4 history file: [./tests/EURUSD240_new_format_401.hst]
MT4ForexParser.py   L:42   DEBUG   [2020-07-21 20:55:42,675] MT4 history file format version: [401]
MT4ForexParser.py   L:63   INFO    [2020-07-21 20:55:43,098] It was read 12969 rows from file [./tests/EURUSD240_new_format_401.hst]
MT4ForexParser.py   L:64   INFO    [2020-07-21 20:55:43,099] Showing last 3 rows:
MT4ForexParser.py   L:69   INFO    [2020-07-21 20:55:43,103]              date   time     open     high      low    close  volume
MT4ForexParser.py   L:69   INFO    [2020-07-21 20:55:43,104] 12966  2019.07.08  08:00  1.12305  1.12339  1.12190  1.12310    8894
MT4ForexParser.py   L:69   INFO    [2020-07-21 20:55:43,104] 12967  2019.07.08  12:00  1.12309  1.12322  1.12123  1.12228    9257
MT4ForexParser.py   L:69   INFO    [2020-07-21 20:55:43,104] 12968  2019.07.08  16:00  1.12228  1.12240  1.12091  1.12153    7381
MT4ForexParser.py   L:73   INFO    [2020-07-21 20:55:43,187] Forex history saved to .csv-formatted file [./tests/EURUSD240_new_format_401.csv]
MT4ForexParser.py   L:148  DEBUG   [2020-07-21 20:55:43,188] All MT4 parser operations are finished success (summary code is 0).
MT4ForexParser.py   L:153  DEBUG   [2020-07-21 20:55:43,188] MT4 parser work duration: 0:00:00.594304
MT4ForexParser.py   L:154  DEBUG   [2020-07-21 20:55:43,189] MT4 parser work finished: 2020-07-21 20:55:43

Process finished with exit code 0
```

Файл ./tests/EURUSD240_new_format_401.csv будет полностью аналогичный и включать те же самые столбцы "date", "time", "open", "high", "low", "close", "volume" (всего 12969 строк):
```
2009.12.21,00:00,1.4311,1.4347,1.4311,1.4342,5504
2009.12.21,04:00,1.4342,1.4357,1.4327,1.4334,5234
2009.12.21,08:00,1.4334,1.4342,1.428,1.4337,8366
...
2019.07.08,08:00,1.12305,1.12339,1.1219,1.1231,8894
2019.07.08,12:00,1.12309,1.12322,1.12123,1.12228,9257
2019.07.08,16:00,1.12228,1.1224,1.12091,1.12153,7381
```

Кроме того, вы можете построить интерактивный график цен (используя библиотеку [PriceGenerator](https://github.com/Tim55667757/PriceGenerator)). Для этого укажите ключ `--render` после ключа `--parse`:
```commandline
mt4forexparser --mt4-history ./tests/EURUSD240_new_format_401.hst --output test.csv --parse --render
```

После выполнения команды выше вы получите три файла:
- `test.csv` — файл в формате .csv, который содержит цены (пример: [./media/test.csv](./media/test.csv));
- `index.html` — график цен и статистику, отрисованные при помощи библиотеки Bokeh и сохранённые в .html-файл (пример: [./media/index.html](./media/index.html));
- `index.html.md` — статистика в текстовом виде, сохранённая в маркдаун-формате (пример: [./media/index.html.md](./media/index.html.md)).

![](./media/index.html.png)


### Через импорт модуля

Рассмотрим на примере парсинга файла истории нового формата (версии 401 для MetaTrader 4) ./tests/EURUSD240_new_format_401.hst:
```
from mt4forexparser.MT4ForexParser import MT4ParseToPD as Parser

# Распарсим исторические свечи и сохраним данные в переменную типа pandas dataframe.
# Для сохранения свечей в файл можно указать переменную outputFile="./tests/EURUSD240_new_format_401.csv"
# Если переменная outputFile не будет указана, модуль вернёт только данные в формате pandas dataframe.
df = Parser(historyFile="./tests/EURUSD240_new_format_401.hst")
print(df)  # выведем данные по свечам в формате pandas dataframe
```

При запуске получим полностью аналогичный вывод:
```
...
>>> print(df)
             date   time     open     high      low    close  volume
0      2009.12.21  00:00  1.43110  1.43470  1.43110  1.43420    5504
1      2009.12.21  04:00  1.43420  1.43570  1.43270  1.43340    5234
2      2009.12.21  08:00  1.43340  1.43420  1.42800  1.43370    8366
3      2009.12.21  12:00  1.43370  1.43710  1.43300  1.43330    8456
4      2009.12.21  16:00  1.43320  1.43350  1.42860  1.42940    8488
...           ...    ...      ...      ...      ...      ...     ...
12964  2019.07.08  00:00  1.12230  1.12293  1.12192  1.12204    3455
12965  2019.07.08  04:00  1.12205  1.12307  1.12203  1.12307    4173
12966  2019.07.08  08:00  1.12305  1.12339  1.12190  1.12310    8894
12967  2019.07.08  12:00  1.12309  1.12322  1.12123  1.12228    9257
12968  2019.07.08  16:00  1.12228  1.12240  1.12091  1.12153    7381
```


Успехов вам в автоматизации биржевой торговли! ;)
