from lib.tools import data
class STOCKS():
    def __init__(self):
        self.__stocks = data.get('DATA/STOCKS')

    def getSymbols(self):
        symbols = list(self.__stocks.keys())
        symbols.sort()
        return symbols

    def getName(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['name']
        else:
            return None

    def getType(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['type']
        else:
            return None
    
    def getSubType(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['subType']
        else:
            return None
    
    def getBusinessSummary(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['businessSummary']
        else:
            return None

    def getExchange(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['exchange']
        else:
            return None

    def getExchangeName(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['exchangeName']
        else:
            return None

    def getSector(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['sector']
        else:
            return None

    def getIndustry(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['industry']
        else:
            return None

    def getCountry(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['country']
        else:
            return None

    def getIndex(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['index']
        else:
            return None

    def getYield(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['yield']
        else:
            return None

    def getDividendYield(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['dividendYield']
        else:
            return None

    def getDividendAnnual(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['dividendAnnual']
        else:
            return None

    def getPreviousClose(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['previousClose']
        else:
            return None

    def getTrailingPE(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['trailingPE']
        else:
            return None

    def getForwardPE(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['forwardPE']
        else:
            return None
    def getTrailingEPS(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['trailingEPS']
        else:
            return None

    def getForwardEPS(self, symbol):
        if symbol in self.__stocks:
            return self.__stocks[symbol]['forwardEPS']
        else:
            return None
