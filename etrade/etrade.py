import webbrowser, requests
from rauth import OAuth1Service
from config.keys import *

# pip install rauth

class Session():
    def __init__(self):
        etrade = OAuth1Service(
            name="etrade",
            consumer_key=KEYS['ETRADE']['KEY'],
            consumer_secret=KEYS['ETRADE']['SECRET'],
            request_token_url="https://api.etrade.com/oauth/request_token",
            access_token_url="https://api.etrade.com/oauth/access_token",
            authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
            base_url='https://api.etrade.com')
        
        request_token, request_token_secret = etrade.get_request_token(
            params={"oauth_callback": "oob", "format": "json"})

        authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
        webbrowser.open(authorize_url)
        text_code = input("Please accept agreement and enter text code from browser: ")

        self._session = etrade.get_auth_session(request_token,
                                        request_token_secret,
                                        params={"oauth_verifier": text_code})

    def __del__(self):
        print('kill session')
        url = 'https://api.etrade.com/oauth/revoke_access_token'
        try:
            self._session.get(url)
        except:
            pass

    def getQuotes(self, symbols, detailFlag='ALL'):
        if not isinstance(symbols, list):
            print('symbols need to be a list of symbols !')
            return None
        symbolsString = ','.join(symbols)
        params = {'detailFlag': detailFlag, 'overrideSymbolCount': 'true'}
        response = self._session.get('https://api.etrade.com/v1/market/quote/%s.json' % symbolsString, params=params)
        return Quotes(response)

class Quotes():
    def __init__(self, response):
        self.status_code = response.status_code
        self.url = response.url
        self.error = False
        self.errorMessage = None
        self.errorCode = None
        self.messages = []
        self.quoteData = []
        try:
            data = response.json()
        except:
            self.error = True
            self.errorMessage = 'JSON decode failed'
            return
        if 'Error' in data:
            self.error = True
            if 'code' in data['Error']:
                self.errorCode = data['Error']['code']
            if 'message' in data['Error']:
                self.errorMessage = data['Error']['message']
        if 'QuoteResponse' in data:
            data = data['QuoteResponse']
            if 'Messages' in data:
                for message in data['Messages']['Message']:
                    self.messages.append('%s: %s' % (message['type'], message['description']))
            if 'QuoteData' in data:
                self.quoteData = data['QuoteData']
