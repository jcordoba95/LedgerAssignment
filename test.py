import sys
import re

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
    if indexLoaded and priceLoaded and len(arguments) > 4:
        # Read now the other flags
        print(arguments)


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
    datePattern = '/([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))/'
    file = open(file, 'r')
    rows = file.read().splitlines()
    for data in rows:
        if not data.startswith(';'):
            if data[0].isdigit():
                
                regex = re.compile(datePattern)
                date = data.split(' ')[0]
                result = regex.search(date)
                
                print('asd:')
                print(result.group(1))

                
    

if __name__ == '__main__':
    main(sys.argv)