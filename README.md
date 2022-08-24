# timer
A simple timer for profiling python code.

## Installation

```bash
pip install git+https://github.com/camall3n/timer.git
```

## Usage

Timers can be used in a few different ways. The simplest of these is to wrap the computation block you'd like to time in a `with` statement:

```python
from timer import Timer

with Timer('my_func'):
    func()
```

Alternatively, you can use `@Timer.wrap()` to decorate a function:

```python
@Timer.wrap()
def my_func(*args):
    # do stuff
    return

@Timer.wrap('foo')
def foo_func(*args):
    # do stuff
    return
```

The decorator syntax automatically uses the function's qualified name as a tag (e.g. `__classname__.__name__`), but it accepts an optional tag argument if you'd like to override this with your own identifier (e.g. `'foo'`). Decorator syntax is equivalent to wrapping all occurrences of a function call using the `with` syntax and specifying the same tag for each occurrence.

> Note the use of parentheses in `@Timer.wrap()`. Normal decorators don't need parentheses, but `Timer.wrap()` is actually a decorator-generating function, which is why it needs them.

## Printing Statistics

The timer module will attempt to automatically print statistics at the end of program execution. To print manually, use `Timer.print_stats()`.

```text
----------------------------------------------------------
tag          frac       time    percall      rate    calls
-------  --------  ---------  ---------  --------  -------
my_func  0.857573  1.000504s  1.000504s  0.999496        1
----------------------------------------------------------
Total time: 1.166669s
----------------------------------------------------------
```

This table displays (left to right):

- `tag`: the identifier string for the computation block or function
- `frac`: the fraction of the total time that the computation block takes up
- `time`: the corresponding wallclock time
- `percall`: the average time per call
- `rate`: the effective rate of calls per second
- `calls`: the total number of calls

The stats are global, so you can `import timer` wherever you need it and the stats will print for all timers. The total time since the `timer` module was first imported is displayed at the bottom of the table.

## Example

The following example is available in the `test/` directory.

Command:

```bash
python test/test.py
```

Source:

```python
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
```

Output:

```text
---------------------------------------------------------------------
tag                 frac       time    percall          rate    calls
--------------  --------  ---------  ---------  ------------  -------
a               0.026705  0.051122s  0.000051s  19561.160340     1000
my_func         0.285803  0.547121s  0.011894s     84.076532       46
Thing.do_stuff  0.158690  0.303786s  0.303786s      3.291793        1
c               0.525156  1.005321s  1.005321s      0.994707        1
---------------------------------------------------------------------
Total time: 1.914330s
---------------------------------------------------------------------
```
