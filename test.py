import sys
import re

class Transaction:
    def __init__(self):
        self.date = ""
        self.description = ""
        self.postings = []


class Posting:
    def __init__(self):
        self.account = ""
        self.balances = {}
        # "coin"    : amount,
        # "BTC"     : 0.0,
        # "$"       : 300.00
        # etc.



priceDbList = []
ledgerImportsList = []
transactionData = []
sortedTransactionData = []
balCoins = {}

def priceDbParser(file):
    file = open(file, 'r')
    global priceDbList
    priceDbList = file.read().splitlines() 
    file.close()

def main(arguments):
    global sortedTransactionData
    arguments.remove(arguments[0])
    comesFrom = ''
    indexLoaded = False
    for arg in arguments:
        if comesFrom == '--price-db':
            priceDbFile(arg)
            comesFrom = ''
            continue
        if comesFrom == '-f':
            indexFiles(arg)
            indexLoaded = True
            comesFrom = ''
            continue
        if arg == '--price-db':
            comesFrom = '--price-db'
            continue
        if arg == '-f':
            comesFrom = '-f'
            continue
    for line in ledgerImportsList:
        if line.startswith('!include'):
            includeParser(line.split(' ')[1])

    if indexLoaded:
        # Read now the other flags
        if '--sort' in arguments:
            sort = ''
            flag = False
            for arg in arguments:
                if arg == '--sort':
                    flag = True
                    continue
                if flag:
                    sort = arg
                    break
            if not sort:
                print("Missing --sort parameter date.")
            # TODO: Sort stuff goes here:
            sortedTransactionData = transactionData

        else:
            sortedTransactionData = transactionData
        if 'print' in arguments: ledgerPrint()
        if 'register' in arguments: ledgerRegister()
            
            
        


def priceDbFile(file):
    file = open(file, 'r')
    global priceDbList
    priceDbList = file.read().splitlines() 
    file.close()

def indexFiles(file):
    file = open(file, 'r')
    global ledgerImportsList
    ledgerImportsList = file.read().splitlines()
    file.close()

def includeParser(file):
    datePattern = re.compile(r"\d{4}/\d{1,2}/\d{1,2}")
    regex = re.compile(datePattern)
    file = open(file, 'r')
    rows = file.read().splitlines()
    trans = Transaction()
    total = {}
    sub = False
    for data in rows:
        if not data.startswith(';'):
            if data[0].isdigit():
                date = data.split(' ')[0]
                result = regex.search(date)

                # Add inverted values from total to the last Posting
                if sub:
                    index = len(trans.postings) - 1
                    trans.postings[index].balances = total
                    for coin in trans.postings[index].balances:
                        trans.postings[index].balances[coin] *= -1
                    # Add current Transaction to our transactions list
                    transactionData.append(trans)
                    trans = Transaction()
                    sub = False
                total = {}

                if len(trans.postings) == 0:
                    # First transaction in the iteration
                    trans.date = result.string
                    trans.description = data.replace(trans.date + ' ', '')
                else:
                    # Add current Transaction to our transactions list
                    transactionData.append(trans)
                    trans = Transaction()
                    trans.date = result.string
                    trans.description = data.replace(trans.date + ' ', '')
            
                
                # print(result.string)
            else:
                # New Posting
                posting = Posting()
                # Used to check if the previous char was a blank space
                flag = False

                account = ""
                data = data[1:]
                # Iterate to split account from amount
                for char in data:
                    if char == '\t':
                        break
                    if char == ' ':
                        if flag:
                            break
                        flag = True
                    elif char.isalpha():
                        flag = False
                    account += char
                    
                posting.account = account
                amount = data.replace(account, '')
                amount = amount.split()

                if len(amount) == 0:
                    # Add the total negative amount to posting.amount
                    sub = True
                    
                elif len(amount) == 2:
                    posting.balances[amount[1]] = float(amount[0])
                    total[amount[1]] = float(amount[0])
                    
                    # amount = float(amount[0])
                elif len(amount) == 1:
                    number = amount[0].replace('$', '')
                    posting.balances['$'] = float(number)
                    total['$'] = float(number)

                    # amount = amount[0].replace('$', '')
                trans.postings.append(posting)
    # END FOR
    
    # Add last transaction into our Transaction list
    if sub:
        index = len(trans.postings) - 1
        trans.postings[index].balances = total
        for coin in trans.postings[index].balances:
            trans.postings[index].balances[coin] *= -1
    transactionData.append(trans)

def ledgerPrint():
    for transaction in sortedTransactionData:
        print('\n')
        print(transaction.date + ' ' + transaction.description)
        for posting in transaction.postings:
            account = '\t' + posting.account
            amount = ''
            for key in posting.balances:
                if key == '$':
                    amount = key + ' ' + str(posting.balances[key])
                else:
                    amount = str(posting.balances[key]) + ' ' + key

            print('{:45}{:>5}'.format(account, amount))

def ledgerRegister():
    # date  desc  acc  movement   coins totals
    # :9    :20   :20  :>5            :>5
    reminders = {}
    for transaction in sortedTransactionData:
        date = transaction.date
        desc = transaction.description
        if len(desc) > 20:
            cant = len(desc) - 17
            desc = desc[:-cant]
            desc += '..'
        account = ''

        for posting in transaction.postings:
            account = posting.account
            for key in posting.balances:
                # Determine amount in left & right side:
                reminders[key] = float(reminders.get(key, '0')) + posting.balances[key]
                left = ''
                right = ''
                if key == '$':
                    left = key + ' ' + str(posting.balances.get(key))
                    right = key + ' ' + str(reminders.get(key, '0'))
                else:
                    left = str(posting.balances.get(key)) + ' ' + key
                    right = str(reminders.get(key, '0')) + ' ' + key
                # Print first value of the transaction
                print('{:9}{:20}{:20}{:>10}{:>10}'.format(date, desc, account, left, right))
                # Print accounts current register:
                for key2 in reminders:
                    if reminders.get(key2) == 0:
                        continue
                    if key2 == key:
                        continue
                    elif key2 == '$':
                        right = key2 + ' ' + str(reminders.get(key2))
                        print('{:9}{:20}{:20}{:>10}{:>10}'.format('', '', '', '', right))
                    else:
                        right = str(reminders.get(key2)) + ' ' + key2
                        print('{:9}{:20}{:20}{:>10}{:>10}'.format('', '', '', '', right))

if __name__ == '__main__':
    main(sys.argv)