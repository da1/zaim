from zaim.zaim import Zaim

def paymentFilter(money):
    return filter(lambda x:x['mode']=='payment',money)

def convertPaymentPerDay(money):
    paymentPerDay = {};
    for p in paymentFileter(money['money']):
        date = p['date']
        amount = p['amount']
        if paymentPerDay.has_key(date):
            paymentPerDay[date] += amount
        else:
            paymentPerDay[date] = amount
    return paymentPerDay

if __name__ == '__main__':
    zaim = Zaim()
    result = zaim.money()
    paymentPerDay = convertPaymentPerDay(result)

    print "Date,Amount"
    for date in paymentPerDay.keys():
        print "%s,%d" % (date, paymentPerDay[date])
