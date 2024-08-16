from config.config import *
import lib.scrape as scrape
from lib.tools import data
from copy import deepcopy
from pprint import pp
class STOCKS():
    # symbol template
    __symbol = {
        'name': set(),
        'type': set(),
        'subType': set(),
        'businessSummary': set(),
        'exchange': set(),
        'exchangeName': set(),
        'sector': set(),
        'industry': set(),
        'country': set(),
        'index': set(),
        'yield': set(),
        'dividendAnnual': set(),
        'dividendYield': set(),
        'previousClose': set(),
        'trailingPE': set(),
        'forwardPE': set(),
        'trailingEPS': set(),
        'forwardEPS': set(),
    }
    def __rebuildDatabase(self):
        # start database
        self.__stocks = {}

        # gather from FMP Stocks
        # fmp = scrape.FMP(refresh=True)
        fmp = scrape.FMP()
        fmpStocks = fmp.getData()
        for stock in fmpStocks:
            symbol = stock['symbol']
            self.__stocks[symbol] = deepcopy(self.__symbol)
            self.__stocks[symbol]['name'].add(stock['name'])
            self.__stocks[symbol]['type'].add(stock['type'].upper())
            self.__stocks[symbol]['exchange'].add(stock['exchangeShortName'])
            self.__stocks[symbol]['exchangeName'].add(stock['exchange'])

        # gather nasdaq stock screener
        nasdaqss = scrape.NASDAQSS()
        nasdaqStockScreener = nasdaqss.getData()
        for x in nasdaqStockScreener.index:
            nstock = nasdaqStockScreener.iloc[x]
            symbol = nstock['Symbol']
            if symbol != symbol:
                continue
            if not symbol in self.__stocks:
                self.__stocks[symbol] = deepcopy(self.__symbol)
            # if 'Common Stock' in nstock['Name']:
            #     pass
            # elif 'Ordinary Shares' in nstock['Name']:
            #     pass
            # elif 'Ordinary Share' in nstock['Name']:
            #     pass
            # elif 'Depositary Shares' in nstock['Name']:
            #     pass
            # elif 'Depositary Share' in nstock['Name']:
            #     pass
            # elif 'Depository Shares' in nstock['Name']:
            #     pass
            # elif 'Common Shares' in nstock['Name']:
            #     pass
            # else:
            #     print(nstock['Name'])
            self.__stocks[symbol]['name'].add(nstock['Name'])
            self.__stocks[symbol]['type'].add('STOCK')
            self.__stocks[symbol]['sector'].add(nstock['Sector'])
            self.__stocks[symbol]['industry'].add(nstock['Industry'])
            self.__stocks[symbol]['country'].add(nstock['Country'])

        # gather nasdaq ETF screener
        nasdaqetfs = scrape.NASDAQETFS()
        nasdaqETFScreener = nasdaqetfs.getData()
        for x in nasdaqETFScreener.index:
            nstock = nasdaqETFScreener.iloc[x]
            symbol = nstock['SYMBOL']
            if symbol.startswith('Data as of'):
                continue
            if symbol != symbol:
                continue
            if not symbol in self.__stocks:
                self.__stocks[symbol] = deepcopy(self.__symbol)
            self.__stocks[symbol]['name'].add(nstock['NAME'])
            self.__stocks[symbol]['type'].add('ETF')

        # gather SPDRS data
        spdrs = scrape.SPDRS()
        for sector, sectorData in spdrs.getData().items():
            for x in sectorData['data'].index:
                nstock = sectorData['data'].iloc[x]
                symbol = nstock['Symbol']
                if not symbol in self.__stocks:
                    self.__stocks[symbol] = deepcopy(self.__symbol)
                self.__stocks[symbol]['name'].add(nstock['Company Name'])

        # gather YahooFin Indices
        # yahoofin = scrape.YAHOOFIN(refresh=True)
        yahoofin = scrape.YAHOOFIN()
        for index, symbols in yahoofin.getData().items():
            for symbol in symbols:
                if not symbol in self.__stocks:
                    self.__stocks[symbol] = deepcopy(self.__symbol)
                self.__stocks[symbol]['index'].add(index)

        # get symbols for YFINANCE and save them first
        # symbols = fmp.getSymbols()
        # symbols = symbols.union(nasdaqss.getSymbols())
        # symbols = symbols.union(nasdaqetfs.getSymbols())
        # symbols = symbols.union(spdrs.getSymbols())
        # symbols = symbols.union(yahoofin.getSymbols())
        # symbols = list(symbols)
        # symbols.sort()
        symbols = ['AAPL', 'VITAX', 'ANET', 'BBD', 'VZ', 'HHH']

        # get yfinance info
        # yfinance = scrape.YFINANCE(symbols=symbols, refresh=True)
        yfinance = scrape.YFINANCE()
        # yfinance.printDataStructure()
        for symbol, stockData in yfinance.getData().items():
            if not symbol in self.__stocks:
                self.__stocks[symbol] = deepcopy(self.__symbol)
            if 'info' in stockData:
                info = stockData['info']
                self.__stocks[symbol]['index'].add(index)
                if 'longName' in info:
                    self.__stocks[symbol]['name'].add(info['longName'])
                if 'quoteType' in info:
                    self.__stocks[symbol]['type'].add(info['quoteType'].upper())
                if 'longBusinessSummary' in info:
                    self.__stocks[symbol]['businessSummary'].add(info['longBusinessSummary'])
                if 'exchange' in info:
                    self.__stocks[symbol]['exchange'].add(info['exchange'])
                if 'sector' in info:
                    self.__stocks[symbol]['sector'].add(info['sector'])
                if 'industry' in info:
                    self.__stocks[symbol]['industry'].add(info['industry'])
                if 'country' in info:
                    self.__stocks[symbol]['country'].add(info['country'])
                if 'yield' in info:
                    self.__stocks[symbol]['yield'].add(info['yield'])
                if 'dividendRate' in info:
                    self.__stocks[symbol]['dividendAnnual'].add(info['dividendRate'])
                if 'dividendYield' in info:
                    self.__stocks[symbol]['dividendYield'].add(info['dividendYield']*100)
                if 'previousClose' in info:
                    self.__stocks[symbol]['previousClose'].add(info['previousClose'])
                if 'trailingPE' in info:
                    self.__stocks[symbol]['trailingPE'].add(info['trailingPE'])
                if 'forwardPE' in info:
                    self.__stocks[symbol]['forwardPE'].add(info['forwardPE'])
                if 'trailingEps' in info:
                    self.__stocks[symbol]['trailingEPS'].add(info['trailingEps'])
                if 'forwardEps' in info:
                    self.__stocks[symbol]['forwardEPS'].add(info['forwardEps'])
                # if 'category' in info:
                #     self.__stocks[symbol]['category'].add(info['category'])
                # if 'currency' in info:
                #     self.__stocks[symbol]['currency'].add(info['currency'])
                # if 'fundFamily' in info:
                #     self.__stocks[symbol]['fundFamily'].add(info['fundFamily'])
                # if 'lastDividendValue' in info:
                #     self.__stocks[symbol]['lastDividendValue'].add(info['lastDividendValue'])
                # if 'lastDividendDate' in info:
                #     self.__stocks[symbol]['lastDividendDate'].add(info['lastDividendDate'])
                # if 'exDividendDate' in info:
                #     self.__stocks[symbol]['exDividendDate'].add(info['exDividendDate'])
                # if 'previousClose' in info:
                #     self.__stocks[symbol]['previousClose'].add(info['previousClose'])

        # {'info': {'address1': '1095 Avenue of the Americas',
        #           'city': 'New York',
        #           'state': 'NY',
        #           'zip': '10036',
        #           'country': 'United States',
        #           'phone': '212 395 1000',
        #           'website': 'https://www.verizon.com',
        #           'industry': 'Telecom Services',
        #           'industryKey': 'telecom-services',
        #           'industryDisp': 'Telecom Services',
        #           'sector': 'Communication Services',
        #           'sectorKey': 'communication-services',
        #           'sectorDisp': 'Communication Services',
        #           'longBusinessSummary': 'Verizon Communications Inc., through its '
        #                                  'subsidiaries, engages in the provision of '
        #                                  'communications, technology, information, and '
        #                                  'entertainment products and services to '
        #                                  'consumers, businesses, and governmental '
        #                                  'entities worldwide. It operates in two '
        #                                  'segments, Verizon Consumer Group (Consumer) '
        #                                  'and Verizon Business Group (Business). The '
        #                                  'Consumer segment provides wireless services '
        #                                  'across the wireless networks in the United '
        #                                  'States under the Verizon and TracFone brands '
        #                                  'and through wholesale and other '
        #                                  'arrangements; and fixed wireless access '
        #                                  '(FWA) broadband through its wireless '
        #                                  'networks, as well as related equipment and '
        #                                  'devices, such as smartphones, tablets, smart '
        #                                  'watches, and other wireless-enabled '
        #                                  'connected devices. The segment also offers '
        #                                  'wireline services in the Mid-Atlantic and '
        #                                  'Northeastern United States, as well as '
        #                                  'Washington D.C. through its fiber-optic '
        #                                  'network, Verizon Fios product portfolio, and '
        #                                  'a copper-based network. The Business segment '
        #                                  'provides wireless and wireline '
        #                                  'communications services and products, '
        #                                  'including FWA broadband, data, video and '
        #                                  'conferencing, corporate networking, security '
        #                                  'and managed network, local and long-distance '
        #                                  'voice, and network access services to '
        #                                  'deliver various IoT services and products to '
        #                                  'businesses, government customers, and '
        #                                  'wireless and wireline carriers in the United '
        #                                  'States and internationally. The company was '
        #                                  'formerly known as Bell Atlantic Corporation '
        #                                  'and changed its name to Verizon '
        #                                  'Communications Inc. in June 2000. Verizon '
        #                                  'Communications Inc. was incorporated in 1983 '
        #                                  'and is headquartered in New York, New York.',
        #           'fullTimeEmployees': 103900,
        #           'companyOfficers': [{'maxAge': 1,
        #                                'name': 'Mr. Hans E. Vestberg',
        #                                'age': 58,
        #                                'title': 'Chairman & CEO',
        #                                'yearBorn': 1965,
        #                                'fiscalYear': 2023,
        #                                'totalPay': 6129275,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Mr. Anthony T. Skiadas',
        #                                'age': 54,
        #                                'title': 'Executive VP & CFO',
        #                                'yearBorn': 1969,
        #                                'fiscalYear': 2023,
        #                                'totalPay': 1931244,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Mr. Kyle  Malady',
        #                                'age': 55,
        #                                'title': 'Executive VP & CEO of Verizon '
        #                                         'Business Group',
        #                                'yearBorn': 1968,
        #                                'fiscalYear': 2023,
        #                                'totalPay': 2807217,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Mr. Sowmyanarayan  Sampath',
        #                                'age': 46,
        #                                'title': 'Executive VP & CEO of Verizon '
        #                                         'Consumer Group',
        #                                'yearBorn': 1977,
        #                                'fiscalYear': 2023,
        #                                'totalPay': 2879913,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Ms. Mary-Lee  Stillwell',
        #                                'age': 49,
        #                                'title': 'Senior VP of Accounting & External '
        #                                         'Reporting and Controller',
        #                                'yearBorn': 1974,
        #                                'fiscalYear': 2023,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Mr. Joseph J. Russo',
        #                                'title': 'Executive VP & President of Global '
        #                                         'Networks and Technology',
        #                                'fiscalYear': 2023,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Mr. Brady  Connor',
        #                                'title': 'Senior Vice President of Investor '
        #                                         'Relations',
        #                                'fiscalYear': 2023,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Ms. Vandana  Venkatesh',
        #                                'age': 50,
        #                                'title': 'Executive VP & Chief Legal Officer',
        #                                'yearBorn': 1973,
        #                                'fiscalYear': 2023,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Ms. Stacy  Sharpe',
        #                                'title': 'Executive VP & Chief Communications '
        #                                         'Officer',
        #                                'fiscalYear': 2023,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0},
        #                               {'maxAge': 1,
        #                                'name': 'Ms. Leslie  Berland',
        #                                'title': 'Executive VP & Chief Marketing '
        #                                         'Officer',
        #                                'fiscalYear': 2023,
        #                                'exercisedValue': 0,
        #                                'unexercisedValue': 0}],
        #           'auditRisk': 1,
        #           'boardRisk': 6,
        #           'compensationRisk': 1,
        #           'shareHolderRightsRisk': 3,
        #           'overallRisk': 1,
        #           'governanceEpochDate': 1722470400,
        #           'compensationAsOfEpochDate': 1703980800,
        #           'irWebsite': 'http://www22.verizon.com/investor/',
        #           'maxAge': 86400,
        #           'priceHint': 2,
        #           'previousClose': 40.9,
        #           'open': 40.84,
        #           'dayLow': 40.0,
        #           'dayHigh': 40.92,
        #           'regularMarketPreviousClose': 40.9,
        #           'regularMarketOpen': 40.84,
        #           'regularMarketDayLow': 40.0,
        #           'regularMarketDayHigh': 40.92,
        #           'dividendRate': 2.66,
        #           'dividendYield': 0.065,
        #           'exDividendDate': 1720569600,
        #           'payoutRatio': 1.0,
        #           'fiveYearAvgDividendYield': 5.41,
        #           'beta': 0.393,
        #           'trailingPE': 15.052631,
        #           'forwardPE': 8.537313,
        #           'volume': 13684129,
        #           'regularMarketVolume': 13684129,
        #           'averageVolume': 17482032,
        #           'averageVolume10days': 16386190,
        #           'averageDailyVolume10Day': 16386190,
        #           'bid': 40.18,
        #           'ask': 40.19,
        #           'bidSize': 1800,
        #           'askSize': 2900,
        #           'marketCap': 168549187584,
        #           'fiftyTwoWeekLow': 30.14,
        #           'fiftyTwoWeekHigh': 43.42,
        #           'priceToSalesTrailing12Months': 1.2555529,
        #           'fiftyDayAverage': 40.6866,
        #           'twoHundredDayAverage': 39.6368,
        #           'trailingAnnualDividendRate': 2.66,
        #           'trailingAnnualDividendYield': 0.06503668,
        #           'currency': 'USD',
        #           'enterpriseValue': 349379362816,
        #           'profitMargins': 0.08382,
        #           'floatShares': 4203500382,
        #           'sharesOutstanding': 4209520128,
        #           'sharesShort': 47992126,
        #           'sharesShortPriorMonth': 46457794,
        #           'sharesShortPreviousMonthDate': 1719532800,
        #           'dateShortInterest': 1722384000,
        #           'sharesPercentSharesOut': 0.0114,
        #           'heldPercentInsiders': 0.00043000001,
        #           'heldPercentInstitutions': 0.64475,
        #           'shortRatio': 2.56,
        #           'shortPercentOfFloat': 0.0114,
        #           'impliedSharesOutstanding': 4209520128,
        #           'bookValue': 22.846,
        #           'priceToBook': 1.7526044,
        #           'lastFiscalYearEnd': 1703980800,
        #           'nextFiscalYearEnd': 1735603200,
        #           'mostRecentQuarter': 1719705600,
        #           'earningsQuarterlyGrowth': -0.012,
        #           'netIncomeToCommon': 11251999744,
        #           'trailingEps': 2.66,
        #           'forwardEps': 4.69,
        #           'pegRatio': 10.91,
        #           'lastSplitFactor': '1000000:937889',
        #           'lastSplitDate': 1278028800,
        #           'enterpriseToRevenue': 2.603,
        #           'enterpriseToEbitda': 7.262,
        #           '52WeekChange': 0.23714459,
        #           'SandP52WeekChange': 0.24822903,
        #           'lastDividendValue': 0.665,
        #           'lastDividendDate': 1720569600,
        #           'exchange': 'NYQ',
        #           'quoteType': 'EQUITY',
        #           'symbol': 'VZ',
        #           'underlyingSymbol': 'VZ',
        #           'shortName': 'Verizon Communications Inc.',
        #           'longName': 'Verizon Communications Inc.',
        #           'firstTradeDateEpochUtc': 438273000,
        #           'timeZoneFullName': 'America/New_York',
        #           'timeZoneShortName': 'EDT',
        #           'uuid': 'a708480c-0400-3ea0-b2d3-ca752db5c3b1',
        #           'messageBoardId': 'finmb_415798',
        #           'gmtOffSetMilliseconds': -14400000,
        #           'currentPrice': 40.04,
        #           'targetHighPrice': 55.0,
        #           'targetLowPrice': 35.0,
        #           'targetMeanPrice': 45.6,
        #           'targetMedianPrice': 46.0,
        #           'recommendationMean': 2.5,
        #           'recommendationKey': 'buy',
        #           'numberOfAnalystOpinions': 25,
        #           'totalCash': 2487000064,
        #           'totalCashPerShare': 0.591,
        #           'ebitda': 48111001600,
        #           'totalDebt': 178329993216,
        #           'quickRatio': 0.471,
        #           'currentRatio': 0.626,
        #           'totalRevenue': 134243000320,
        #           'debtToEquity': 182.829,
        #           'revenuePerShare': 31.849,
        #           'returnOnAssets': 0.04982,
        #           'returnOnEquity': 0.120950006,
        #           'freeCashflow': 8379500032,
        #           'operatingCashflow': 36024000512,
        #           'earningsGrowth': -0.009,
        #           'revenueGrowth': 0.006,
        #           'grossMargins': 0.59853,
        #           'ebitdaMargins': 0.35839,
        #           'operatingMargins': 0.23128,
        #           'financialCurrency': 'USD',
        #           'trailingPegRatio': 1.161},
        #  'financials':                                                         2023-12-31      2022-12-31          2021-12-31      2020-12-31  2019-12-31
        # Tax Effect Of Unusual Items                          -1593504000.0    -248787000.0   -818690754.588715     -30186000.0         NaN
        # Tax Rate For Calcs                                           0.288           0.231            0.231203           0.234         NaN
        # Normalized EBITDA                                    45668000000.0   50060000000.0       52652000000.0   45063000000.0         NaN
        # Total Unusual Items                                  -5533000000.0   -1077000000.0       -3541000000.0    -129000000.0         NaN
        # Total Unusual Items Excluding Goodwill               -5533000000.0   -1077000000.0       -3541000000.0    -129000000.0         NaN
        # Net Income From Continuing Operation Net Minori...   11614000000.0   21256000000.0       22065000000.0   17801000000.0         NaN
        # Reconciled Depreciation                              17624000000.0   17099000000.0       16206000000.0   16720000000.0         NaN
        # Reconciled Cost Of Revenue                           54887000000.0   59133000000.0       56301000000.0   51201000000.0         NaN
        # EBITDA                                               40135000000.0   48983000000.0       49111000000.0   44934000000.0         NaN
        # EBIT                                                 22511000000.0   31884000000.0       32905000000.0   28214000000.0         NaN
        # Net Interest Income                                  -5170000000.0   -3467000000.0       -3437000000.0   -4182000000.0         NaN
        # Interest Expense                                      5524000000.0    3613000000.0        3485000000.0    4247000000.0         NaN
        # Interest Income                                        354000000.0     146000000.0          48000000.0      65000000.0         NaN
        # Normalized Income                                    15553496000.0   22084213000.0  24787309245.411285   17899814000.0         NaN
        # Net Income From Continuing And Discontinued Ope...   11614000000.0   21256000000.0       22065000000.0   17801000000.0         NaN
        # Total Expenses                                      105256000000.0  106368000000.0      101165000000.0   99494000000.0         NaN
        # Total Operating Income As Reported                   22877000000.0   30467000000.0       32448000000.0   28798000000.0         NaN
        # Diluted Average Shares                                4215000000.0    4204000000.0        4150000000.0    4142000000.0         NaN
        # Basic Average Shares                                  4211000000.0    4202000000.0        4148000000.0    4140000000.0         NaN
        # Diluted EPS                                                   2.75            5.06                5.32             4.3         NaN
        # Basic EPS                                                     2.76            5.06                5.32             4.3         NaN
        # Diluted NI Availto Com Stockholders                  11614000000.0   21256000000.0       22065000000.0   17801000000.0         NaN
        # Net Income Common Stockholders                       11614000000.0   21256000000.0       22065000000.0   17801000000.0         NaN
        # Net Income                                           11614000000.0   21256000000.0       22065000000.0   17801000000.0         NaN
        # Minority Interests                                    -481000000.0    -492000000.0        -553000000.0    -547000000.0         NaN
        # Net Income Including Noncontrolling Interests        12095000000.0   21748000000.0       22618000000.0   18348000000.0         NaN
        # Net Income Continuous Operations                     12095000000.0   21748000000.0       22618000000.0   18348000000.0         NaN
        # Tax Provision                                         4892000000.0    6523000000.0        6802000000.0    5619000000.0         NaN
        # Pretax Income                                        16987000000.0   28271000000.0       29420000000.0   23967000000.0         NaN
        # Other Income Expense                                 -6561000000.0    1271000000.0         409000000.0    -649000000.0         NaN
        # Other Non Operating Income Expenses                   -975000000.0    2304000000.0        3805000000.0    -475000000.0         NaN
        # Special Income Charges                               -5533000000.0   -1077000000.0       -3541000000.0    -129000000.0         NaN
        # Gain On Sale Of Business                                       NaN             NaN                 NaN             NaN  94000000.0
        # Other Special Charges                                 -308000000.0    1077000000.0        3541000000.0     129000000.0         NaN
        # Impairment Of Capital Assets                          5841000000.0             0.0                 0.0             0.0         NaN
        # Earnings From Equity Interest                          -53000000.0      44000000.0         145000000.0     -45000000.0         NaN
        # Net Non Operating Interest Income Expense            -5170000000.0   -3467000000.0       -3437000000.0   -4182000000.0         NaN
        # Interest Expense Non Operating                        5524000000.0    3613000000.0        3485000000.0    4247000000.0         NaN
        # Interest Income Non Operating                          354000000.0     146000000.0          48000000.0      65000000.0         NaN
        # Operating Income                                     28718000000.0   30467000000.0       32448000000.0   28798000000.0         NaN
        # Operating Expense                                    50369000000.0   47235000000.0       44864000000.0   48293000000.0         NaN
        # Depreciation Amortization Depletion Income Stat...   17624000000.0   17099000000.0       16206000000.0   16720000000.0         NaN
        # Depreciation And Amortization In Income Statement    17624000000.0   17099000000.0       16206000000.0   16720000000.0         NaN
        # Selling General And Administration                   32745000000.0   30136000000.0       28658000000.0   31573000000.0         NaN
        # Gross Profit                                         79087000000.0   77702000000.0       77312000000.0   77091000000.0         NaN
        # Cost Of Revenue                                      54887000000.0   59133000000.0       56301000000.0   51201000000.0         NaN
        # Total Revenue                                       133974000000.0  136835000000.0      133613000000.0  128292000000.0         NaN
        # Operating Revenue                                   133974000000.0  136835000000.0      133613000000.0  128292000000.0         NaN}


        # get ETRADE info
        # etrade = scrape.ETRADE(symbols=symbols, refresh=True)
        etrade = scrape.ETRADE()
        # etrade.printDataStructure()
        etradeData = etrade.getData()
        keys = set()
        for quoteType in ['ALL', 'MF_DETAIL']:
            isMF_DETAIL = quoteType == 'MF_DETAIL'
            for quote in etradeData[quoteType]:
                symbol = quote['Product']['symbol']
                self.__stocks[symbol]['type'].add(quote['Product']['securityType'])
                if 'securitySubType' in quote['Product']:
                    self.__stocks[symbol]['subType'].add(quote['Product']['securitySubType'])
                if not symbol in self.__stocks:
                    self.__stocks[symbol] = deepcopy(self.__symbol)
                if 'MutualFund' in quote:
                    quote = quote['MutualFund']
                    isMF = True
                elif 'All' in quote:
                    quote = quote['All']
                    isMF = False
                self.__stocks[symbol]['name'].add(quote['symbolDescription'])
                
                if isMF:
                    pass
                else:
                    self.__stocks[symbol]['dividendYield'].add(quote['yield'])
                    self.__stocks[symbol]['trailingPE'].add(quote['pe'])
                    self.__stocks[symbol]['trailingEPS'].add(quote['eps'])
        print(keys)

        # isMF = False
        # quoteType = None
        # if 'ALL' in etradeData:
        #     quoteType = 'ALL'
        # elif 'MF_DETAIL' in etradeData:
        #     quoteType = 'MF_DETAIL'
        #     isMF = True
        # for quote in etradeData[quoteType]:
        #     symbol = quote['Product']['symbol']
        #     if 'securitySubType' in quote['Product']:
        #         self.__stocks[symbol]['type'].add(quote['Product']['securitySubType'])
        #     if 'All' in quote:
        #         quote = quote['All']
        #     elif 'MutualFund' in quote:
        #         quote = quote['MutualFund']
        #     self.__stocks[symbol]['name'].add(quote['symbolDescription'])
        #     if isMF:
        #         pass
        #     else:
        #         if quoteType == 'ALL' and 'dividend' not in quote:
        #             pp(quote)
        #             break
        #         # self.__stocks[symbol]['dividendRate'].add(quote['dividend'])
        # pp(paramsProduct)
        data.save('DATA_TEMP/STOCKS', self.__stocks)

        # {'dateTime': '16:28:32 EDT 08-13-2024',
        #  'dateTimeUTC': 1723580912,
        #  'quoteStatus': 'CLOSING',
        #  'ahFlag': 'true',
        #  'hasMiniOptions': False,
        #  'All': {'adjustedFlag': False,
        #          'ask': 145.25,
        #          'askSize': 100,
        #          'askTime': '16:28:32 EDT 08-13-2024',
        #          'bid': 128.5,
        #          'bidExchange': '',
        #          'bidSize': 100,
        #          'bidTime': '16:28:32 EDT 08-13-2024',
        #          'changeClose': 1.82,
        #          'changeClosePercentage': 1.34,
        #          'companyName': 'AGILENT TECHNOLOGIES INC COM',
        #          'daysToExpiration': 0,
        #          'dirLast': '1',
        #          'dividend': 0.236,
        #          'eps': 4.22,
        #          'estEarnings': 5.204,
        #          'exDividendDate': 1719963961,
        #          'high': 137.7,
        #          'high52': 155.35,
        #          'lastTrade': 137.42,
        #          'low': 135.33,
        #          'low52': 96.8,
        #          'open': 135.83,
        #          'openInterest': 0,
        #          'optionStyle': '',
        #          'optionUnderlier': '',
        #          'previousClose': 135.6,
        #          'previousDayVolume': 1347171,
        #          'primaryExchange': 'NYSE',
        #          'symbolDescription': 'AGILENT TECHNOLOGIES INC COM',
        #          'totalVolume': 1157979,
        #          'upc': 0,
        #          'cashDeliverable': 0,
        #          'marketCap': 40093659200.0,
        #          'sharesOutstanding': 291760000,
        #          'nextEarningDate': '',
        #          'beta': 0.84,
        #          'yield': 0.6962,
        #          'declaredDividend': 0.236,
        #          'dividendPayableDate': 1721864761,
        #          'pe': 32.1643,
        #          'week52LowDate': 1698709561,
        #          'week52HiDate': 1715989561,
        #          'intrinsicValue': 0.0,
        #          'timePremium': 0.0,
        #          'optionMultiplier': 0.0,
        #          'contractSize': 0.0,
        #          'expirationDate': 0,
        #          'timeOfLastTrade': 1723579800,
        #          'averageVolume': 1716831,
        #          'ExtendedHourQuoteDetail': {'lastPrice': 137.42,
        #                                      'change': 1.82,
        #                                      'percentChange': 1.34,
        #                                      'bid': 128.5,
        #                                      'bidSize': 100,
        #                                      'ask': 145.25,
        #                                      'askSize': 100,
        #                                      'volume': 1157979,
        #                                      'timeOfLastTrade': 1723580912,
        #                                      'timeZone': 'EST',
        #                                      'quoteStatus': 'EH_REALTIME'}},
        #  'Product': {'symbol': 'A', 'securityType': 'EQ'}}
        # data['data']['MF_DETAIL']: <class 'list'>
        # Item 0:
        # {'dateTime': '00:01:00 EDT 08-13-2024',
        #  'dateTimeUTC': 1723521660,
        #  'quoteStatus': 'CLOSING',
        #  'ahFlag': 'true',
        #  'timeZone': 'EST',
        #  'dstFlag': True,
        #  'MutualFund': {'symbolDescription': 'American Beacon Balanced Inv',
        #                 'cusip': '02368A828',
        #                 'changeClose': 0.1,
        #                 'previousClose': 12.36,
        #                 'transactionFee': 'No Transaction Fee Found',
        #                 'earlyRedemptionFee': '0',
        #                 'availability': 'Open to New Buy and Sell',
        #                 'initialInvestment': 0.0,
        #                 'subsequentInvestment': 0.0,
        #                 'fundFamily': 'AMERICAN BEACON',
        #                 'fundName': 'American Beacon Balanced Inv',
        #                 'changeClosePercentage': 0.81,
        #                 'timeOfLastTrade': 1723521660,
        #                 'netAssetValue': 12.46,
        #                 'publicOfferPrice': 12.46,
        #                 'netExpenseRatio': 1.05,
        #                 'grossExpenseRatio': 1.05,
        #                 'orderCutoffTime': 1600,
        #                 'salesCharge': 'None',
        #                 'initialIraInvestment': 0.0,
        #                 'subsequentIraInvestment': 0.0,
        #                 'fundInceptionDate': 775713600,
        #                 'averageAnnualReturns': 0.0,
        #                 'sevenDayCurrentYield': 0.0,
        #                 'annualTotalReturn': 12.46,
        #                 'weightedAverageMaturity': 0.0,
        #                 'averageAnnualReturn1Yr': 12.6302,
        #                 'averageAnnualReturn3Yr': 3.7185,
        #                 'averageAnnualReturn5Yr': 7.3998,
        #                 'averageAnnualReturn10Yr': 6.2859,
        #                 'high52': 12.66,
        #                 'low52': 10.51,
        #                 'week52LowDate': 1698451333,
        #                 'week52HiDate': 1722470533,
        #                 'exchangeName': 'US Mutual Fund Providers',
        #                 'sinceInception': 7.7187,
        #                 'quarterlySinceInception': 7.6192,
        #                 'lastTrade': 12.46,
        #                 'actual12B1Fee': 0,
        #                 'performanceAsOfDate': '2024-07-31',
        #                 'qtrlyPerformanceAsOfDate': '2024-06-30',
        #                 'morningStarCategory': 'Moderate Allocation',
        #                 'monthlyTrailingReturn1Y': 12.74478,
        #                 'monthlyTrailingReturn3Y': 4.99608,
        #                 'monthlyTrailingReturn5Y': 8.02979,
        #                 'monthlyTrailingReturn10Y': 6.77386,
        #                 'etradeEarlyRedemptionFee': 'None',
        #                 'maxSalesLoad': 0,
        #                 'monthlyTrailingReturnYTD': 8.65286,
        #                 'monthlyTrailingReturn1M': 3.453,
        #                 'monthlyTrailingReturn3M': 6.39152,
        #                 'monthlyTrailingReturn6M': 8.28517,
        #                 'qtrlyTrailingReturnYTD': 5.0263,
        #                 'qtrlyTrailingReturn1M': 0,
        #                 'qtrlyTrailingReturn3M': -0.7851,
        #                 'qtrlyTrailingReturn6M': 5.0263,
        #                 'exchangeCode': 'BETA',
        #                 'NetAssets': {'value': 113907183, 'asOfDate': 1722398400},
        #                 'Redemption': {'isFrontEnd': '0',
        #                                'frontEndValues': [],
        #                                'isSales': '0',
        #                                'salesDurationType': '',
        #                                'salesValues': []}},
        #  'Product': {'symbol': 'AABPX', 'securityType': 'MF'}}
    def __init__(self, refresh=REFRESH):
        if refresh:
            self.__rebuildDatabase()
        else:
            self.__stocks = data.get('DATA_TEMP/STOCKS')

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
