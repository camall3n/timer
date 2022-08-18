from timer import Timer

N = 1000

@Timer.wrap()
def a(i):
    with Timer('a'):
        return sum([x for x in range(i)])

@Timer.wrap('my_func')
def b(i):
    return sum([x**2 for x in range(i)])

class Thing:
    @Timer.wrap()
    def do_stuff(self):
        return sum([x**2 for x in range(N)])

def c():
    return sum([x for x in range(N)])

def main():
    for i in range(N):
        if a(i) < N:
            b(i)

    Thing().do_stuff()

    with Timer('c'):
        c()

    Timer.print_stats()

if __name__=='__main__':
    main()
