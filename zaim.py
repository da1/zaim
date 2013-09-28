# coding: utf-8
import codecs
import csv
from datetime import datetime

import sys
import requests
import oauth2
import urlparse
import json
from urllib import urlencode
import time

consumer_key        = u""
consumer_secret     = u""
access_token        = u""
access_token_secret = u""

money_bug = 3866790 # おさいふ

def conv2genre(data):
    table = {
        1: 59762094, #食料品
        2: 60441990, #生活
        3: 60441493, #娯楽
        4: 59762121, #家賃
        5: 60441486, #水道光熱費
        6: 12850219, #給与所得
        7: 60441491, #本
        8: 60442193, #奨学金
            }
    return table[data]

def conv2category(data):
    idTable = {
        1: 12850225, #食料品
        2: 12850226, #日用雑貨
        3: 12850232, #エンタメ
        4: 12850230, #住まい
        5: 12850229, #水道・光熱
        6: 12850219, #給与所得
        7: 12850232, #エンタメ 本
        8: 12850233, #教育・教養 '奨学金'
            }
    return idTable[data]

def date_now():
    return datetime.now().strftime("%Y-%m-%d")

def verify():
    return get(u"https://api.zaim.net/v2/home/user/verify")

def getClient():
    token = oauth2.Token(key=access_token, secret=access_token_secret)
    consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
    return oauth2.Client(consumer, token)

def access(method, url, params=""):
    client = getClient()
    resp, content = client.request(url, method=method, body=urlencode(params))
    return json.loads(content)

def post(url, params):
    return access('POST', url, params)

def get(url):
    return access('GET', url)

def money():
    return get(u"https://api.zaim.net/v2/home/money")

def payment(category_id, genre_id, amount, date, comment):
    params = {
            'category_id'     : category_id,
            'genre_id'        : genre_id,
            'amount'          : amount,
            'comment'         : comment,
            'date'            : date,
            'from_account_id' : money_bug,
            #'receipt_id'      : receipt_id,
        }
    return post(u"https://api.zaim.net/v2/home/money/payment", params)

def income(category_id, amount, date, comment):
    params = {
            'category_id'   : category_id,
            'amount'        : amount,
            'date'          : date,
            'to_account_id' : money_bug,
            'comment'       : comment,
        }
    return post(u"https://api.zaim.net/v2/home/money/income", params)

def account():
    return get(u"https://api.zaim.net/v2/home/account")

def category():
    return get(u"https://api.zaim.net/v2/home/category")

def genre():
    return get(u"https://api.zaim.net/v2/home/genre")

def money():
    return get(u"https://api.zaim.net/v2/home/money")

def remQuote(text):
    return text[1:-1]

def convertDate(tstr):
    tdatetime = datetime.strptime(tstr, '%Y%m%d%H%M%S')
    return tdatetime.strftime('%Y-%m-%d')

def reader(row):
    return {
            'date': convertDate(remQuote(row[3])),
            'type': 'income' if remQuote(row[4]) == '1' else 'payment',
            'category': int(remQuote(row[5])),
            'amount': abs(int(float(remQuote(row[6])))),
            'name': remQuote(row[7]),
            'memo': remQuote(row[8]),
            }

def show_category():
    print "id,name,parent"
    for c in category()['categories']:
        print "%s,%s,%s" % (c['id'], c['name'].encode('utf-8'), c['parent_category_id'])

def show_ganre():
    print "id,name,parent"
    for g in genre()['genres']:
        print "%s,%s,%s" % (g['id'], g['name'].encode('utf-8'), g['parent_genre_id'])

def mover():
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        spamReader = csv.reader(f)
        count = 0
        for row in spamReader:
            data = reader(row)
            if data['type'] == 'payment':
                payment(conv2category(data['category']), conv2genre(data['category']), data['amount'], data['date'], data['name'])
            else:
                income(conv2category(data['category']), data['amount'], data['date'], data['name'])
            print data['name'], data['amount'], data['date'], conv2category(data['category'])
            count+=1

def readToCSV():
    result = money()
    moneyPerDay = {};
    for m in filter(lambda x:x['mode']=='payment',result['money']):
        date = m['date']
        amount = m['amount']
        if moneyPerDay.has_key(date):
            moneyPerDay[date] += amount
        else:
            moneyPerDay[date] = amount
    for date in moneyPerDay.keys():
        print "%s,%d" % (date, moneyPerDay[date])

if __name__ == '__main__':
    readToCSV()
