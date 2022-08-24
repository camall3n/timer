import time
from timer import Timer

N = 1000

def a(i):
    with Timer('a'):
        return sum([x for x in range(i)])

@Timer.wrap('my_func')
def b():
    time.sleep(0.01)

class Thing:
    @Timer.wrap()
    def do_stuff(self):
        time.sleep(.3)

def c():
    time.sleep(1)

def main():
    [b() for i in range(N) if a(i) < N]

    Thing().do_stuff()

    with Timer('c'):
        c()

if __name__=='__main__':
    main()
