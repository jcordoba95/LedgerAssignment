# Node its the class created to use for every node in the accounts tree.
class Node:
    def __init__(self):
        self.childs = []
        self.name = ''
        self.parent = None
        self.balance = 0.0

    # Brings total balance from current amount + childs amounts added up.
    def getTotalBalance(self):
        total = self.balance
        if (len(self.childs) != 0):
            for node in self.childs:
                total += node.getTotalBalance()
        return total


ledgerImportsList = []
priceDbList = []
root = Node()

def main(price_db, f):
    global ledgerImportsList
    priceDbParser(price_db)
    ledgerImports(f)
    # Create our tree from every transaction in the '!include' files found in index.ledger
    for line in ledgerImportsList:
        if line.startswith('!include'):
            buildTree(line.split(' ')[1])
            break #Prueba

# Missing Regex portion
def ledgerPrint():
    for importLine in ledgerImportsList:
        if importLine.startswith('!include'):
            file = open(importLine.split(' ')[1], 'r')
            fileList = file.read().splitlines()
            file.close()
            for line in fileList:
                if not line.startswith(';'):
                    print(line)

            

def priceDbParser(file):
    file = open(file, 'r')
    global priceDbList
    priceDbList = file.read().splitlines() 
    file.close()
    
def ledgerImports(f):
    file = open(f, 'r')
    global ledgerImportsList
    ledgerImportsList = file.read().splitlines()
    file.close()

def breadthSearch(elements, node):
    if len(elements) == 0:
        return node
    if len(node.childs) == 0:
        n = Node()
        n.name = elements[0]
        node.childs.append(n)
        n.parent = node
        elements.remove(elements[0])
        return breadthSearch(elements, n)

    for value in node.childs:
        if elements[0] == value.name:
            elements.remove(elements[0])
            return breadthSearch(elements, value)

    # Node doesn't exist yet in breadth.
    n = Node()
    n.name = elements[0]
    node.childs.append(n)
    n.parent = node
    elements.remove(elements[0])
    return breadthSearch(elements, n)



        
        



def addNode(accounts, amount):
    global root
    accounts = accounts.split(':')
    node = breadthSearch(accounts, root)

    node.balance += float(amount[1:])

def subtractFromNode(accounts, amount):
    global root
    accounts = accounts.split(':')
    node = breadthSearch(accounts, root)
    amount = amount * -1.0
    # amount = float(amount)

    node.balance += amount

def buildTree(file):
    file = open(file, 'r')
    fileList = file.read().splitlines()
    file.close()
    flag = 'new'
    pastLine = ''
    totalAmount = 0.0
    for line in fileList:
        if not line.startswith(';'):
            if line[0].isdigit() and flag == 'sub':
                # New Data.
                subtractCorrection(flag, pastLine, totalAmount)   
                totalAmount = 0.0
                flag = 'new'
            elif line[0] == '\t':
                accountsAmount = line.split('\t')
                accounts = accountsAmount[1]
                # pastLine = accountsAmount
                if len(accountsAmount) > 3:
                    # This means it has the accounts and the amount
                    amount = accountsAmount[3]
                    totalAmount += float(amount[1:])
                    # Method to add to tree new element
                    addNode(accounts, amount)
                else:
                    # Subtract to this line what is in     totalAmount.
                    if totalAmount > 0.0:
                        subtractFromNode(accounts, totalAmount)
                    flag = 'sub'
                # Header of transaction in 'line'
                # print(accountsAmount)
            pastLine = line
    subtractCorrection(flag, pastLine, totalAmount)
    

def subtractCorrection(flag, pastLine, totalAmount):
    if flag != 'sub' and totalAmount > 0.0:
        # SUBSTRACT from pastLine the amount AND total amount.
        accountsAmount = pastLine.split('\t')
        accounts = accountsAmount[1]
        subtractFromNode(accounts, totalAmount)



if __name__ == '__main__':
    main('prices_db', 'index.ledger')