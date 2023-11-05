import numpy as np


class Stack:
    def __init__(self, size) -> None:
        self.__head = -1
        self.__stack = np.empty(size, dtype=list)  # Inicialize a lista vazia
        self.size = size

    def is_full(self):
        return self.__head == self.size - 1

    def is_empty(self):
        return self.__head == -1

    def push(self, data):
        if self.is_full():
            raise Exception("Stack is full")

        self.__head += 1
        self.__stack[self.__head] = data  # Use append para adicionar um elemento à lista
        return self.__stack[self.__head]

    def pop(self):
        if self.is_empty():
            raise Exception("Stack is empty")

        self.__head -= 1
        return self.__stack.pop()  # Use pop para remover e retornar o último elemento da lista

    def peek(self):
        if self.is_empty():
            raise Exception("Stack is empty")

        return self.__stack[self.__head + 1]

    def show(self):
        for i in range(self.__head, -1, -1):
            print(self.__stack[i])
