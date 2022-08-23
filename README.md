# timer
A simple timer for profiling python code.

## Installation

```bash
pip install git+https://github.com/camall3n/timer.git
```

## Basic Usage

The library provides the `Timer` class, which can be used in a few different ways.

The simplest of these is to wrap the computation block you'd like to time in a `with` statement:

```python
with Timer('my_func'):
    func()
```

The `'my_func'` string is a way to tag a block of computation for ease of interpreting the results of the profiling. At any point during program execution, you can call `Timer.print_stats()` to see the results:

```text
------------------------------------------------------
tag        frac    time    percall       rate    calls
-------  ------  ------  ---------  ---------  -------
my_func  0.6180  0.0005     0.0005  1828.3801        1
------------------------------------------------------
Total time: 0.000885009765625
------------------------------------------------------
```

For each specified `tag` identifier, this table displays (left to right) the fraction of the total time that the computation block takes up, its corresponding wallclock time, the time per call (in seconds), the effective rate of calls per second, and the total number of calls.

The stats are global, so you can import it wherever you need one (`from timer import Timer`) and then just call `Timer.print_stats()` once at the end of the main scope (or whenever you want to check). The total time since the `timer` module was first imported is displayed at the bottom of the table.

## Decorator Usage

You can also use the `Timer.wrap()` decorator to conveniently time functions:

```python
@Timer.wrap()
def my_func(*args):
    # do stuff
    return

class Foo:
    @Timer.wrap()
    def foo_fn():
        # foo stuff
        return
```

The decorator will automatically provide a tag string using the function's fully-qualified name (`.__qualname__`). In the above code snippet, the tag strings would be `'my_func'` and `'Foo.foo_fn'`.

Note the use of parentheses in `Timer.wrap()`. Normal decorators don't need parentheses, but `Timer.wrap()` is actually a decorator-generating function, which is why it needs them. The upshot of doing it this way is that it allows the decorator to accept an optional argument for manually setting the tag string:

```python
class Foo:
    @Timer.wrap('foo')
    def foo_fn():
        # foo stuff
        return
```

The decorator syntax is equivalent to wrapping all occurrences of a function call using the `with Timer('tag'):` syntax and the same tag for each.

## Example

The following example is available in the `test/` directory.

Command:

```bash
python test/test.py
```

Source:

```python
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
```

Output:

```text
--------------------------------------------------------------
tag               frac    time    percall        rate    calls
--------------  ------  ------  ---------  ----------  -------
a               1.7615  0.1403     0.0001  14257.5868     2000
my_func         0.0083  0.0007     0.0000  69753.4288       46
Thing.do_stuff  0.0100  0.0008     0.0008   1251.6574        1
c               0.0019  0.0002     0.0002   6615.6215        1
--------------------------------------------------------------
Total time: 0.07963228225708008
--------------------------------------------------------------
```
