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
    for line in ledgerImportsList:
        if line.startswith('!include'):
            buildTree(line.split(' ')[1])
            break #Prueba
    


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
    
    for value in node.childs:
        if elements[0] == value.name:
            elements.remove(elements[0])
            return breadthSearch(elements, value)

    n = Node()
    n.name = elements[0]
    node.childs.append(n)
    elements.remove(elements[0])
    breadthSearch(elements, n)
            


        
        



def addNode(accounts, ammount):
    global root
    accounts = accounts.split(':')
    print(accounts)
    node = breadthSearch(accounts, root.childs)
    node.balance =+ ammount


def buildTree(file):
    file = open(file, 'r')
    fileList = file.read().splitlines()
    file.close()
    flag = ''
    pastLine = ''
    for line in fileList:
        if not line.startswith(';'):
            if line[0].isdigit():
                # Nuevos datos.
                # SUBSTRACT from pastLine the double the ammount
                flag = 'new'
            elif line[0] == '\t':
                accountsAmount = line.split('\t')
                pastLine = accountsAmount
                if len(accountsAmount) > 3:
                    # This means it has the accounts and the amount
                    accounts = accountsAmount[1]
                    amount = accountsAmount[3]
                    # Method to add to tree new element
                    addNode(accounts, amount)

                # print(accountsAmount)
            pastLine = line






if __name__ == '__main__':
    main('prices_db', 'index.ledger')