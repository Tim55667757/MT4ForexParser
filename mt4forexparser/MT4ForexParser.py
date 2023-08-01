# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


# Module: MT4 Forex History Parser.
# Read forex data in MetaTrader 4 .hst-format and convert into .csv file and pandas dataframe.


import os
import sys
sys.path.append("..")
from datetime import datetime
import numpy as np
import pandas as pd
from argparse import ArgumentParser

import mt4forexparser.UniLogger as uLog
import traceback as tb

from pricegenerator import PriceGenerator as pg


# --- Common technical parameters:

uLogger = uLog.UniLogger
uLogger.level = 10  # debug level by default
uLogger.handlers[0].level = 20  # info level by default for STDOUT
# uLogger.handlers[1].level = 50  # disable duplicate logging added by PriceGenerator
# uLogger.handlers[1].level = 10  # debug level by default for log.txt


def MT4ParseToPD(historyFile, outputFile=None):
    """
    Read and parse MetaTrader 4 .hst file. Save to .csv if needed. Return pandas dataframe.
    :param historyFile: full path to MetaTrader 4 .hst-file.
    :param outputFile: full path to .csv output file. If not defined then only return pandas dataframe.
    """
    if historyFile is None:
        raise Exception("Path to MetaTrader 4 history file must be define!")

    uLogger.debug("MT4 history file: [{}]".format(os.path.abspath(historyFile)))

    with open(historyFile, "rb") as fH:
        version = np.frombuffer(fH.read(148)[:4], "i4")
        uLogger.debug("MT4 history file format version: {}".format(version))

        if version == 400:
            dType = [("datetime", "u4"), ("open", "f8"), ("low", "f8"), ("high", "f8"), ("close", "f8"), ("volume", "f8")]
            df = pd.DataFrame(np.frombuffer(fH.read(), dtype=dType))

        elif version == 401:
            dType = [("datetime", "u8"), ("open", "f8"), ("high", "f8"), ("low", "f8"), ("close", "f8"), ("volume", "i8"), ("s", "i4"), ("r", "i8")]
            data = np.frombuffer(fH.read(), dtype=dType)
            df = pd.DataFrame(data).drop(axis=1, labels=["s", "r"])

        else:
            raise Exception("MetaTrader 4 history file has unsupported version: {}".format(version))

        df["datetime"] = pd.to_datetime(df["datetime"], unit="s")
        df["date"] = df["datetime"].apply(lambda x: x.strftime("%Y.%m.%d"))
        df["time"] = df["datetime"].apply(lambda x: x.strftime("%H:%M"))
        df["volume"] = df["volume"].astype(int)

        df = df.drop(axis=1, labels=["datetime"])[["date", "time", "open", "high", "low", "close", "volume"]]

    uLogger.info("It was read {} rows from file [{}]".format(len(df), os.path.abspath(historyFile)))
    uLogger.info("Showing last 3 rows:")
    for line in pd.DataFrame.to_string(
        df[["date", "time", "open", "high", "low", "close", "volume"]][-3:],
        max_cols=20
    ).split("\n"):
        uLogger.info(line)

    if outputFile is not None:
        df.to_csv(outputFile, index=False, header=False)
        uLogger.info("Forex history saved to .csv-formatted file [{}]".format(os.path.abspath(outputFile)))

    else:
        uLogger.debug("--output key is not defined. Parsed history file not saved to .csv-file.")

    return df


def Render(prices: pd.DataFrame, name="Example instrument", show=True):
    """
    Render interactive chart using PriceGenerator library.
    :param prices: Pandas dataframe with prices.
    :param name: Instrument's name for chart title.
    :param show: Show in browser immediately if True.
    """
    chart = pg.PriceGenerator()
    prices["datetime"] = pd.to_datetime(prices["date"] + " " + prices["time"])
    chart.ticker = os.path.basename(name)
    chart.prices = prices
    chart.RenderBokeh(viewInBrowser=show)


def ParseArgs():
    """
    Function get and parse command line keys.
    """
    parser = ArgumentParser()  # command-line string parser

    parser.description = "Metatrader 4 forex history parser. Read, parse and save history as .csv-file or pandas dataframe. Also you can draw an interactive chart. See examples: https://tim55667757.github.io/MT4ForexParser"
    parser.usage = "mt4forexparser [some options] [one command]"

    # options:
    parser.add_argument("--mt4-history", type=str, required=True, help="Option (required): full path to Metatrader 4 forex history file.")
    parser.add_argument("--output", type=str, default=None, help="Option: full path to .csv output file. Default is None, mean that returns only pandas dataframe.")
    parser.add_argument("--debug-level", type=int, default=20, help="Option: showing STDOUT messages of minimal debug level, e.g. 10 = DEBUG, 20 = INFO, 30 = WARNING, 40 = ERROR, 50 = CRITICAL.")

    # commands:
    parser.add_argument("--parse", action="store_true", help="Command: read, parse and save mt4-history as pandas dataframe or .csv-file if --output is define.")
    parser.add_argument("--render", action="store_true", help="Command: use PriceGenerator module to render interactive chart from parsed data. This key only used with --parse key.")

    cmdArgs = parser.parse_args()
    return cmdArgs


def Main():
    """
    Main function for reading, parsing and saving mt4-history as .csv-file or pandas dataframe.
    """
    history = None
    output = None

    args = ParseArgs()  # get and parse command-line parameters
    exitCode = 0

    if args.debug_level:
        uLogger.level = 10  # always debug level by default
        uLogger.handlers[0].level = args.debug_level  # level for STDOUT
        # uLogger.handlers[1].level = 50  # disable duplicate logging added by PriceGenerator
        # uLogger.handlers[1].level = 10  # always debug level for log.txt

    start = datetime.now()
    uLogger.debug("MT4 parser started: {}".format(start.strftime("%Y-%m-%d %H:%M:%S")))

    try:
        # --- set options:

        if args.mt4_history:
            history = args.mt4_history

        if args.output:
            output = args.output

        # --- do one command:

        if args.parse:
            parsedData = MT4ParseToPD(history, output)

            if args.render and parsedData is not None:
                Render(prices=parsedData, name=history, show=True)

        else:
            raise Exception("One of the possible commands must be selected! See: python MT4ForexParser.py --help")

    except Exception:
        exc = tb.format_exc().split("\n")
        for line in exc:
            if line:
                uLogger.debug(line)
        exitCode = 255

    finally:
        finish = datetime.now()

        if exitCode == 0:
            uLogger.debug("All MT4 parser operations are finished success (summary code is 0).")

        else:
            uLogger.error("An errors occurred during the work! See full debug log with --debug-level 10. Summary code: {}".format(exitCode))

        uLogger.debug("MT4 parser work duration: {}".format(finish - start))
        uLogger.debug("MT4 parser work finished: {}".format(finish.strftime("%Y-%m-%d %H:%M:%S")))

        sys.exit(exitCode)


if __name__ == "__main__":
    Main()
