from zaim.zaim import Zaim
from datetime import datetime
import operator

class MoneyEntity:
    def __init__(self, date):
        self.date    = date
        self.payment = 0
        self.income  = 0
    def add(self, mode, amount):
        if mode == 'payment':
            self.payment += amount
        elif mode == 'income':
            self.income += amount
        else:
            raise Exception, "unknown mode %s"%(mode)

def moneyPerMonth(money):
    perMonth = {}
    for m in money['money']:
        tdatetime = datetime.strptime(m['date'], '%Y-%m-%d')
        strdate   = "%s-%s" % (tdatetime.year, tdatetime.month)

        if perMonth.has_key(strdate):
            perMonth[strdate].add(m['mode'], m['amount'])
        else:
            perMonth[strdate] = MoneyEntity(tdatetime)
    return perMonth

def toArray(perMonthDic):
    return map(lambda date:perMonthDic[date], perMonthDic.keys())

if __name__ == '__main__':
    zaim = Zaim()
    money = zaim.money()
    perMonth = moneyPerMonth(money)

    perMonthArray = toArray(perMonth)
    perMonthArray.sort(key=operator.attrgetter('date'))
    perMonthArray.reverse()

    print "date,payment,income"
    for entity in perMonthArray:
        date = "%s-%s" % (entity.date.year, entity.date.month)
        print "%s,%d,%d" % (date, entity.payment, entity.income)

