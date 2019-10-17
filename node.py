class Node:
    def __init__(self):
        self.childs = []
        self.name = ''
        self.parent = None
        self.balance = 0.0

    def getTotalBalance(self):
        total = self.balance
        if (len(self.childs) != 0):
            for node in self.childs:
                total += node.getTotalBalance()
        return total

# root = Node()

# child1 = Node()
# child1.parent = root
# child1.balance = 5.5
# child1.parent.childs.append(child1)

# child2 = Node()
# child2.parent = child1
# child2.balance = 5.0
# child2.parent.childs.append(child2)

# child3 = Node()
# child3.parent = child2
# child3.balance = 9.4
# child3.parent.childs.append(child3)

# print(child1.getTotalBalance())
# print(child2.getTotalBalance())
# print(child3.getTotalBalance())

