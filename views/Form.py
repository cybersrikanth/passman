import os
from time import sleep

class Form:
    clearCode = "\033[2K"
    moveUpCode = "\033[F"
    newLine = "\n"
    beginLine = "\r"

    def __init__(self):
        self.getScreenSize()

    def getScreenSize(self):
        self.columns, self.lines = os.get_terminal_size()

    def retRed(self, string):
        return "\033[91m{}\033[00m".format(string)

    def allocateScreen(self):
        self.getScreenSize()
        print("-"*self.columns,end="")
        print(self.newLine*int(self.lines-1),end="")
        print("-"*self.columns,end="")
        print(self.moveUpCode*int(self.lines-2),end="")

    def clearScreen(self):
        self.getScreenSize()
        print((self.clearCode+self.moveUpCode)*int(self.lines-1),end="")
        print((self.clearCode+self.newLine)*int(self.lines-1),end="")
        print((self.clearCode+self.moveUpCode)*int(self.lines),end="")

    def refreshScreen(self):
        self.clearScreen()
        self.allocateScreen()

    def clearLines(self, lines):
        if lines == 1:
            print(self.clearCode,end="")
        else:
            print(self.clearCode,end="")
            print((self.moveUpCode+self.clearCode)*int(lines-1),end="")
            
    def passLines(self, lines):
        print((self.clearCode+self.newLine)*lines,end="")

    def printCenter(self, string, symbol):
        len_sym = len(symbol)
        len_str = len(string)+2
        one_side = (self.columns-len_str)//(2*len_sym)
        print((symbol*one_side),string,(symbol*one_side))

    def printRight(self, string, symbol):
        len_sym = len(symbol)
        len_str = len(string)
        side = (self.columns - len_str)//len_sym
        print((symbol*side)+string)