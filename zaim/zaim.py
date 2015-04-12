# coding: utf-8
import yaml
import oauth2
import json
from urllib import urlencode

class Zaim:
    __FILE_NAME = 'config.yaml'
    def __init__(self):
        conf = yaml.load(open(self.__FILE_NAME).read())
        self.__consumer_key        = conf['config']['consumer_key']
        self.__consumer_secret     = conf['config']['consumer_secret']
        self.__access_token        = conf['config']['access_token']
        self.__access_token_secret = conf['config']['access_token_secret']
        self.client = self.getClient()

    def getClient(self):
        token    = oauth2.Token(key=self.__access_token, secret=self.__access_token_secret)
        consumer = oauth2.Consumer(key=self.__consumer_key, secret=self.__consumer_secret)
        return oauth2.Client(consumer, token)

    def access(self, method, url, params=""):
        resp, content = self.client.request(url, method=method, body=urlencode(params))
        return json.loads(content)

    def post(self, url, params):
        return self.access('POST', url, params)

    def get(self, url):
        return self.access('GET', url)

    def verify(self):
        return self.get(u"https://api.zaim.net/v2/home/user/verify")

    def money(self):
        return self.get(u"https://api.zaim.net/v2/home/money?start_date=2012-04-01&end_date=2015-03-31")

    def account():
        return get(u"https://api.zaim.net/v2/home/account")

    def category():
        return get(u"https://api.zaim.net/v2/home/category")

    def genre():
        return get(u"https://api.zaim.net/v2/home/genre")

    def payment(self, category_id, genre_id, amount, date, comment):
        params = {
                'category_id'     : category_id,
                'genre_id'        : genre_id,
                'amount'          : amount,
                'comment'         : comment,
                'date'            : date,
                'from_account_id' : money_bug,
                #'receipt_id'      : receipt_id,
            }
        return self.post(u"https://api.zaim.net/v2/home/money/payment", params)

    def income(self, category_id, amount, date, comment):
        params = {
                'category_id'   : category_id,
                'amount'        : amount,
                'date'          : date,
                'to_account_id' : money_bug,
                'comment'       : comment,
            }
        return self.post(u"https://api.zaim.net/v2/home/money/income", params)
