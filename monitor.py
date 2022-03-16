from multiprocessing import Value
from multiprocessing import Condition, Lock

class Table():
    def __init__(self, NPHIL, manager):
        self.currentphil = None
        self.neating = Value('i',0)
        self.phil = manager.list([False]*NPHIL)
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)
        
    def set_current_phil(self, i):
        self.currentphil = i
        
    def nocomenlados(self):
        return self.phil[(self.currentphil - 1) % len(self.phil)] == False and self.phil[(self.currentphil +1)%len(self.phil)] == False

    def wants_eat(self,i):
        self.mutex.acquire()
        self.freefork.wait_for(self.nocomenlados)
        self.phil[i] = True
        self.neating.value += 1
        self.mutex.release()

    def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False
        self.neating.value -= 1
        self.freefork.notify_all()
        self.mutex.release()

class CheatMonitor():
    def __init__(self):
        self.eating = Value('i',0) 
        self.mutex = Lock()
        self.othereating = Condition (self.mutex)
    
    def algunocomiendo(self):
        return self.eating.value > 1
        
    def is_eating(self, i):
        self.mutex.acquire()
        self.eating.value += 1
        self.othereating.notify_all()
        self.mutex.release()
        
    def wants_think(self, i):
        self.mutex.acquire()
        self.othereating.wait_for(self.algunocomiendo)
        self.eating.value -= 1
        self.mutex.release()

class AnticheatTable():
    def __init__(self, NPHIL,manager):
        self.currentphil = None
        self.hungry = manager.list([False]*NPHIL)
        self.phil = manager.list([False]*NPHIL)
        self.neating = Value('i',0)
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)
        self.chungry = Condition(self.mutex)
        
    def set_current_phil(self, i):
        self.currentphil = i
        
    def nocomenlados(self):
        return self.phil[(self.currentphil - 1) % len(self.phil)] == False and self.phil[(self.currentphil +1)%len(self.phil)] == False
    
    def drchanohungry(self):
        return self.hungry[(self.currentphil + 1) % len(self.phil)] == False
    
    def wants_eat(self,i):
        self.mutex.acquire()
        self.chungry.wait_for(self.drchanohungry)
        self.hungry[i] = True
        self.freefork.wait_for(self.nocomenlados)
        self.phil[i] = True
        self.neating.value += 1
        self.hungry[i] = False
        self.chungry.notify_all()
        self.mutex.release()

    def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False
        self.neating.value -= 1
        self.freefork.notify()
        self.mutex.release()

        
