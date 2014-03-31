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

def getStrDate(tdatetime, mode):
    if mode == "m":
        return "%s-%s" % (tdatetime.year, tdatetime.month)
    elif "4y":
        return tdatetime.year if tdatetime.month > 3 else tdatetime.year - 1
    else:
        return tdatetime.year

def moneyPerMonth(money, mode):
    perMonth = {}
    for m in money['money']:
        tdatetime = datetime.strptime(m['date'], '%Y-%m-%d')
        strdate = getStrDate(tdatetime, mode)

        if perMonth.has_key(strdate):
            perMonth[strdate].add(m['mode'], m['amount'])
        else:
            perMonth[strdate] = MoneyEntity(tdatetime)
    return perMonth

def toArray(perMonthDic):
    return map(lambda date:perMonthDic[date], perMonthDic.keys())

if __name__ == '__main__':
    mode = "4y" # m or 4y or y
    zaim = Zaim()
    money = zaim.money()
    perMonth = moneyPerMonth(money, mode)

    perMonthArray = toArray(perMonth)
    perMonthArray.sort(key=operator.attrgetter('date'))

    print "date,payment,income"
    for entity in perMonthArray:
        date = getStrDate(entity.date, mode)
        print "%s,%d,%d" % (date, entity.payment, entity.income)

