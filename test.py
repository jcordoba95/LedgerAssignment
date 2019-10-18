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



priceDbList = []
ledgerImportsList = []
transactionData = []
coinsBalances = {
    "default": "0"
}
# print(sys.argv)

def priceDbParser(file):
    file = open(file, 'r')
    global priceDbList
    priceDbList = file.read().splitlines() 
    file.close()

def main(arguments):
    arguments.remove(arguments[0])
    comesFrom = ''
    priceLoaded = False
    indexLoaded = False
    for arg in arguments:
        if comesFrom == '--price-db':
            priceDbFile(arg)
            priceLoaded = True
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
                    trans.description = data.replace(trans.date, '')
                else:
                    # Add current Transaction to our transactions list
                    transactionData.append(trans)
                    trans = Transaction()
                    trans.date = result.string
                    trans.description = data.replace(trans.date, '')
            
                
                # print(result.string)
            else:
                # New Posting
                posting = Posting()
                # Used to check if the previous char was a blank space
                flag = False

                account = ""
                balances = {}
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

            


            

                
    

if __name__ == '__main__':
    main(sys.argv)