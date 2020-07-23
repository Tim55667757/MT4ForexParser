# -*- coding: utf-8 -*-

import pytest
import os
import pandas as pd
from mt4forexparser import MT4ForexParser

class TestBaseMethods():

    @pytest.fixture(scope='function', autouse=True)
    def init(self):
        MT4ForexParser.uLogger.level = 50  # Disable debug logging while test, logger CRITICAL = 50
        MT4ForexParser.uLogger.handlers[0].level = 50  # Disable debug logging for STDOUT
        MT4ForexParser.uLogger.handlers[1].level = 50  # Disable debug logging for log.txt

    def test_ParserReturnPandasDataframe(self):
        testData = [
            [os.path.abspath("tests/EURUSD240_old_format_400.hst"), os.path.abspath("tests/EURUSD240_old_format_400.csv")],
            [os.path.abspath("tests/EURUSD240_new_format_401.hst"), os.path.abspath("tests/EURUSD240_new_format_401.csv")],
            [os.path.abspath("tests/EURUSD240_old_format_400.hst"), None],
            [os.path.abspath("tests/EURUSD240_new_format_401.hst"), None],
        ]
        for test in testData:
            result = MT4ForexParser.MT4ParseToPD(historyFile=test[0], outputFile=test[1])
            assert isinstance(result, pd.DataFrame) is True, "Expected Pandas DataFrame result output!"

    def test_ParserCreateOutputFile(self):
        MT4ForexParser.MT4ParseToPD(
            historyFile=os.path.abspath("tests/EURUSD240_new_format_401.hst"),
            outputFile=os.path.abspath("tests/test.csv")
        )
        assert os.path.exists(os.path.abspath("tests/test.csv")), "Output file must be created after parser work finished!"
