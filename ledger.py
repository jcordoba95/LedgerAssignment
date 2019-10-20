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

class Node:
    def __init__(self):
        self.name = ''
        self.balances = {}
        self.parent = None
        self.childs = []

priceDbList = []
ledgerImportsList = []
transactionData = []
sortedTransactionData = []
auxiliarDatesList = []
root = Node()

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
                sys.exit()
            sortedTransactionData = sorted(transactionData, key=lambda transaction: transaction.date)
        else:
            sortedTransactionData = transactionData
        if 'print' in arguments: ledgerPrint()
        if 'register' in arguments: ledgerRegister()
        if 'balance' in arguments: ledgerBalance()

        print('Ledger finished.')
            
# This function reads the prices_db file.
def priceDbFile(file):
    file = open(file, 'r')
    global priceDbList
    priceDbList = file.read().splitlines() 
    file.close()

# This function iterates through the index files that
# contains the route to ledger files.
def indexFiles(file):
    file = open(file, 'r')
    global ledgerImportsList
    ledgerImportsList = file.read().splitlines()
    file.close()

# This function reads all the !include X.ledger files,
# iterates through the file lines and constructs a 
# data structure where we can work with the information in
# the ledger files.
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
            else:
                # New Posting
                posting = Posting()
                # Used to check if the previous char was a blank space
                flag = False

                account = ""
                data = data[1:]
                # Iterate char by char to split account from amount
                for char in data:
                    if char == '\t':
                        break
                    if char == ' ':
                        if flag:
                            account = account[:-1]
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
                elif len(amount) == 1:
                    number = amount[0].replace('$', '')
                    posting.balances['$'] = float(number)
                    total['$'] = float(number)
                trans.postings.append(posting)
    # Add last transaction into our Transaction list
    if sub:
        index = len(trans.postings) - 1
        trans.postings[index].balances = total
        for coin in trans.postings[index].balances:
            trans.postings[index].balances[coin] *= -1
    transactionData.append(trans)

# This function prints out the transactions in the format
# acceptable by the ledger files.
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

# This function prints out the register of our account's transactions.
def ledgerRegister():
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
                print('{:9} {:20} {:40} {:>15} {:<5}'.format(date, desc, account, left, right))
                # Print accounts current register:
                for key2 in reminders:
                    if reminders.get(key2) == 0:
                        continue
                    if key2 == key:
                        continue
                    elif key2 == '$':
                        right = key2 + ' ' + str(reminders.get(key2))
                        print('{:9} {:20} {:40} {:>15} {:<5}'.format('', '', '', '', right))
                    else:
                        right = str(reminders.get(key2)) + ' ' + key2
                        print('{:9} {:20} {:40} {:>15} {:<5}'.format('', '', '', '', right))

# This function prints out the accounts current balance and total balance.
# This function creates a data structure of a tree of the accounts found
# in the ledger files to operate with the account's balances.
def ledgerBalance():
    for transaction in sortedTransactionData:
        for posting in transaction.postings:
            node = checkExistance(posting.account.split(':'),root)
            for key in posting.balances:
                node.balances[key] = float(node.balances.get(key, 0)) + posting.balances.get(key)
    iterateTree(root)
    # Now the tree has the corresponding values and is ready to be printed
    printTree(root)
    print('-----------------------')
    for key in root.balances:
        val = ''
        if key == '$':
            val = key + '  ' + str(root.balances.get(key))
        else:
            val = str(root.balances.get(key)) + ' ' + key
        print('{:>23}'.format(val))

# Determine the amount of tabulations there has to be for the
# 'balance' command's account nesting
def detTab(node):
    if node.parent != None:
        return detTab(node.parent) + '   '
    return ''

# Prints tree in balance format
def printTree(node):
    tabulation = detTab(node)

    if len(node.childs) != 0:
        for child in node.childs:
            first = True
            for key in child.balances:
                if first:
                    first = False
                    val = ''
                    if key == '$':
                        val = key + ' ' + str(child.balances.get(key))
                    else:
                        val = str(child.balances.get(key)) + ' ' + key
                    print('{:>20}'.format(val) + '  ' + tabulation + '{:<40}'.format(child.name))
                    continue
                val = ''
                if key == '$':
                    val = key + ' ' + str(child.balances.get(key))
                else:
                    val = str(child.balances.get(key)) + ' ' + key
                print('{:>20}'.format(val) + '  ' + tabulation + '{:<40}'.format(child.name))
            printTree(child)

# This function will take our tree of accounts and add to the nodes
# the child's balance amount to their balance dictionary. 
# This includes the root node, where we will store the total 
# amounts of our transactions.
def iterateTree(node):
    if len(node.childs) == 0:
        return node.balances
    # Iterate through node's childs
    for value in node.childs:
        balancesToAdd = iterateTree(value)
        # Add the child's balances to the parent's
        if balancesToAdd != None:
            for key in balancesToAdd:
                node.balances[key] = float(node.balances.get(key, 0)) + balancesToAdd.get(key)  
    return node.balances

# This function creates a node of an account and appends it 
# to our main tree of accounts if it doesn't exist yet.
def checkExistance(elements, node):
    if len(elements) == 0:
        return node
    if len(node.childs) == 0:
        n = Node()
        n.name = elements[0]
        node.childs.append(n)
        n.parent = node
        elements.remove(elements[0])
        return checkExistance(elements, n)

    for value in node.childs:
        if elements[0] == value.name:
            elements.remove(elements[0])
            return checkExistance(elements, value)
    
    # Node doesn't exist yet in breadth.
    n = Node()
    n.name = elements[0]
    node.childs.append(n)
    n.parent = node
    elements.remove(elements[0])
    return checkExistance(elements, n)

if __name__ == '__main__':
    main(sys.argv)