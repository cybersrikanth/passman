from time import sleep
from threading import Thread
import cursor


class DotLoader(Thread):
    def __init__(self, message, delay=0.1):
        super(DotLoader, self).__init__()
        self.forward = ("· ", ". ", " .", " ·")
        self.index = 0
        self.status = True
        self.message = message
        self.delay = delay

    def run(self):
        cursor.hide()
        while self.status:
            print(self.forward[self.index],end=" "+str(self.message))
            sleep(self.delay)
            print("\033[K\r",end="")
            if self.index==3:
                self.index = 0
            else:
                self.index = self.index+1

    def stop(self):
        self.status = False
        print("\033[K\r",end="")
        cursor.show()

