from zaim.zaim import Zaim
import codecs

class Entity:
    def __init__(self, comment, amount):
        self.comment = comment
        self.amount  = amount
        self.count = 1
    def add(self, amount):
        self.amount += amount
        self.count += 1

def paymentFilter(money):
    return filter(lambda x:x['mode']=='payment',money)

def moneyPerItem(money):
    item = {}
    for m in paymentFilter(money['money']):
        comment = m['comment']
        amount  = m['amount']
        if item.has_key(comment):
            item[comment].add(amount)
        else:
            item[comment] = Entity(comment, amount)
    return item

def toArray(item):
    return map(lambda comment:item[comment], item.keys())

if __name__ == '__main__':
    zaim = Zaim()
    money = zaim.money()
    items = toArray(moneyPerItem(money))
    items.sort(key=lambda it:it.amount)
    items.reverse()

    for item in items:
        print item.comment.encode('utf-8'), item.amount, item.count
