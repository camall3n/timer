from collections import defaultdict
import time

from tabulate import tabulate

class Timer:
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
    def print_stats(cls, csv=False):
        total_time = time.time() - cls._startup_time
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
            row = [field_name, frac, cumulative_time, time_per_call, iters_per_sec, calls]
            if csv:
                print(*row, sep=', ')
            else:
                rows.append(row)

        if not csv:
            table_str = tabulate(rows, headers=headers, floatfmt='.4f')
            final_row = table_str.split('\n')[-1]
            print('-'*len(final_row))
            print(table_str)
            print('-'*len(final_row))
            print(f'Total time: {total_time}')
            print('-'*len(final_row))

    def wrap(tag=None):
        """Function decorator for timing a function, with an optional tag argument"""
        def new_decorator(func):
            _tag = func.__qualname__ if tag is None else tag
            def wrapped_func(*args):
                with Timer(_tag):
                    return func(*args)
            return wrapped_func
        return new_decorator
