import atexit
from collections import defaultdict
from datetime import timedelta
from functools import wraps
import time

from tabulate import tabulate


def time2str(t, abbr=False):
    """
    Convert an amount of time (in seconds) to a fixed-width string

    :param abbr: if `True`, remove leading spaces. Default: `False`.
    """
    dt = timedelta(seconds=t)
    days = dt.days
    secs = dt.seconds
    hrs, remainder = divmod(secs, 3600)
    mins, secs = divmod(remainder, 60)
    micros = dt.microseconds
    s = f'{days:3d}d' if days > 0 else ' ' * 5
    s += f'{hrs:2d}h' if hrs > 0 else ' ' * 3
    s += f'{mins:2d}m' if mins > 0 else ' ' * 3
    s += f'{secs:2d}.{micros:06d}s'
    return s.lstrip() if abbr else s


class Timer:
    """
    Timer class for profiling code blocks and functions

    Timers can be used in a few different ways. The simplest of these is to
    wrap the computation block you'd like to time in a `with` statement:

    ```
    with Timer('my_func'):
        func()
    ```

    Alternatively, you can use @Timer.wrap() to decorate a function:

    ```
    @Timer.wrap()
    def my_func(*args):
        # do stuff
        return

    @Timer.wrap('foo')
    def foo_func(*args):
        # do stuff
        return
    ```

    The decorator syntax automatically uses the function's qualified name as a
    tag, but it accepts an optional tag argument if you'd like to override
    this with your own identifier.

    The timer module will attempt to automatically print statistics at the end
    of program execution. To print manually, use `Timer.stats()`.
    """
    timers = defaultdict(float)
    counters = defaultdict(int)
    _startup_time = time.time()

    def __init__(self, tag):
        self.field_name = tag

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        end = time.time()
        self.duration = end - self.start
        self.timers[self.field_name] += self.duration
        self.counters[self.field_name] += 1

    @classmethod
    def duration(cls):
        return time.time() - cls._startup_time

    @classmethod
    def reset(cls):
        """
        Delete all timers and reset stats
        """
        cls.timers = defaultdict(float)
        cls.counters = defaultdict(int)
        cls._startup_time = time.time()

    @classmethod
    def stats(cls, csv=False, float_precision=6):
        """
        Print timer statistics

        The timer module will attempt to automatically call this function end
        of program execution, but it can also be called manually.

        :param csv:             print results as comma separated values
                                instead of table
        :param float_precision: the number of decimal places for the frac and
                                rate columns

        Sample output:

        ------------------------------------------------------------
        tag        frac       time    percall          rate    calls
        -----  --------  ---------  ---------  ------------  -------
        a      0.035965  0.056589s  0.000057s  17671.164889     1000
        b      0.323265  0.508638s  0.011057s     90.437532       46
        c      0.635810  1.000410s  1.000410s      0.999590        1
        ------------------------------------------------------------
        Total time: 1.573442s
        ------------------------------------------------------------

        This table displays (left to right):

        - `tag`: the identifier string for the computation block or function
        - `frac`: the fraction of the total time that the computation block
                    takes up
        - `time`: the corresponding wallclock time
        - `percall`: the average time per call
        - `rate`: the effective rate of calls per second
        - `calls`: the total number of calls

        The stats are global, so you can `import timer` wherever you need it
        and the stats will print for all timers. The total time since the
        `timer` module was first imported is displayed at the bottom of the
        table.
        """
        total_time = cls.duration()
        headers = ['tag', 'frac', 'time', 'percall', 'rate', 'calls']
        rows = []
        if csv:
            print(*headers, sep=', ')
        for field_name in cls.timers.keys():
            cumulative_time = cls.timers[field_name]
            frac = cumulative_time / total_time
            calls = cls.counters[field_name]
            time_per_call = cumulative_time / calls
            iters_per_sec = 'NaN' if cumulative_time == 0 else (calls / cumulative_time)
            row = [
                field_name,
                frac,
                time2str(cumulative_time),
                time2str(time_per_call),
                iters_per_sec,
                calls,
            ]
            if csv:
                print(*row, sep=', ')
            else:
                rows.append(row)

        if not csv:
            table_str = tabulate(rows,
                                 headers=headers,
                                 floatfmt=f'.{float_precision}f',
                                 colalign=(['left'] + ['right'] * 5))
            final_row = table_str.split('\n')[-1]
            print('-' * len(final_row))
            print(table_str)
            print('-' * len(final_row))
            print(f'Total time: {time2str(total_time, abbr=True)}')
            print('-' * len(final_row))

    def wrap(tag=None):
        """
        Generates a function decorator for timing a function, with an optional tag argument
        """

        def new_decorator(func):
            if tag is not None:
                _tag = tag
            else:
                try:
                    _tag = func.__qualname__
                except AttributeError:
                    _tag = func.__name__

            @wraps(func)
            def wrapped_func(*args, **kwargs):
                with Timer(_tag):
                    return func(*args, **kwargs)

            return wrapped_func

        return new_decorator


atexit.register(Timer.stats)
