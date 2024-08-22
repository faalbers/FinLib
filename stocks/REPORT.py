import requests
from config.keys import *
from pprint import pp
from lib.tools import store
import yfinance as yf
import pandas as pd
from datetime import datetime
import lib.etrade as etrade

class REPORT():
    def __getETRADEData(self):
        # get FMP data
        etData = self.__data['ETRADE'] = {'timeStamp': int((datetime.timestamp(datetime.now()))), 'data': {}}
        etData = etData['data']

        session = etrade.Session()
        quotes = session.getQuotes([self.symbol], detailFlag='ALL')
        if quotes.error:
            print('Data request failed: ETRADE ALL %s' % self.symbol)
        etData['ALL'] = quotes.quoteData[0]

        if etData['ALL']['Product']['securityType'] == 'MF':
            quotes = session.getQuotes([self.symbol], detailFlag='MF_DETAIL')
            if quotes.error:
                print('Data request failed: ETRADE ALL %s' % self.symbol)

    def __getYFINANCEData(self):
        # get FMP data
        yfData = self.__data['YFINANCE'] = {'timeStamp': int((datetime.timestamp(datetime.now()))), 'data': {}}
        yfData = yfData['data']
        
        ticker = yf.Ticker(self.symbol)
        yfData['info'] = ticker.info
        yfData['financials'] = ticker.financials
        yfData['dividends'] = ticker.dividends
        # ticker.balancesheet
        # ticker.earnings
        # ticker.calendar
        # ticker.cashflow
        # ticker.major_holders
        # ticker.institutional_holders
        # ticker.mutualfund_holders
        # ticker.quarterly_balancesheet
        # ticker.quarterly_cashflow
        # ticker.quarterly_earnings
        # ticker.quarterly_financials
        # ticker.quarterly_incomestmt
    
    def __getFMPData(self):
        # get FMP data
        fmpData = self.__data['FMP'] = {'timeStamp': int((datetime.timestamp(datetime.now()))), 'data': {}}
        fmpData = fmpData['data']
        
        fmpUrl = 'https://financialmodelingprep.com/api/'
        urls = {
            'profile': 'v3/profile/%s' % self.symbol,
            'quote-order': 'v3/quote-order/%s' % self.symbol,
            'stock_dividend': 'v3/historical-price-full/stock_dividend/%s' % self.symbol,
            'key-metrics-ttm': 'v3/key-metrics-ttm/%s' % self.symbol,
            'key-metrics-annual': 'v3/key-metrics/%s?period=annual' % self.symbol,
            # 'key-metrics-quarter': 'v3/key-metrics/%s?period=quarter' % self.symbol,
            'ratios-ttm': 'v3/ratios-ttm/%s' % self.symbol,
            'ratios-annual': 'v3/ratios/%s?period=annual' % self.symbol,
            # 'ratios-quarter': 'v3/ratios/%s?period=quarter' % self.symbol,
        }
        for dataName, url in urls.items():
            reqUrl = fmpUrl+url
            if '?' in reqUrl:
                reqUrl += '&apikey='+KEYS['FMP']['KEY']
            else:
                reqUrl += '?apikey='+KEYS['FMP']['KEY']
            result = requests.get(reqUrl)
            if result.status_code == 200:
                result = result.json()
            else:
                print('Data request failed: %s' % reqUrl)
                if result.status_code == 403:
                    print('Error Message: %s' % result.json()['Error Message'])
            fmpData[dataName] = result

    def __logDataRecurse(self, data, logFile, level):
        dataTypes = set()
        levelTabs = '\t'*level
        if isinstance(data, dict):
            for key, dictData in  data.items():
                logFile.write('\n%s%s: ' % (levelTabs, key))
                self.__logDataRecurse(dictData, logFile, level+1)
        elif isinstance(data, list):
            for listData in  data:
                self.__logDataRecurse(listData, logFile, level)
        elif isinstance(data, pd.Series):
            for key, sData in data.items():
                logFile.write('\n%s%s: %s' % (levelTabs, key, sData))
        elif isinstance(data, pd.DataFrame):
            for column in data.columns:
                logFile.write('\n%s%s: ' % (levelTabs, column))
                for key, sData in data[column].items():
                    logFile.write('\n%s%s: %s' % ('\t'*(level+1), key, sData))
        else:
            self.__dataTypes.add(type(data))
            logFile.write('%s' % data)

    def __logData(self):
        for reportName, rData in self.__data.items():
            with open("LOG/REPORT_%s_%s.log" % (reportName, self.symbol), "w") as logFile:
                logFile.write('%s: %s REPORT\n' % (self.symbol, reportName))
                logFile.write('creation date: %s\n' % datetime.fromtimestamp(rData['timeStamp']))
                self.__logDataRecurse(rData['data'], logFile, 0)

    def __init__(self, symbol):
        self.symbol = symbol
        self.__data = {}
        self.__dataTypes = set()

        self.__getFMPData()
        self.__getYFINANCEData()
        self.__getETRADEData()

        self.__logData()
        print(self.__dataTypes)

