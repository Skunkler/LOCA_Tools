class Queue:

    def __init__(self):
        self.__items = []

    def push(self,item):
        self.__items.insert(0,item)

    def pop(self):
        return self.__items.pop()
    
