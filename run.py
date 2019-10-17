# Node its the class created to use for every node in the accounts tree.
class Node:
    def __init__(self):
        self.childs = []
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
# ['D $1,000.00'                        , 
#  'N $'                                ,
#  'P 2012/11/25 05:04:00 AG $34.13'    ,
#  'P 2012/11/25 05:04:00 AU $1751.90'  ,
#  'P 2012/11/25 05:04:00 BTC $12.46'   ,
#  'P 2012/11/26 05:04:00 CAD $1.0066'  , 
#  'P 2019/11/22 05:03:00 MXN $20.00'   ]

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

def addNode(accounts, ammount):
    accounts = accounts.split(':')
    print(accounts)


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