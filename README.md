# timer
A simple timer for profiling python code.

The way you use it is as follows:

```python
from timer import Timer

def main():
    with Timer('total'):
        # initialize stuff
        done = False
        obs = env.reset()

        while not done:
            with Timer('agent.get_action'):
                action = agent.get_action()
            with Timer('env.step'):
                next_obs, reward, done, _ = env.step(action)
            with Timer('agent.update'):
                agent.update(obs, action, reward, next_obs)

    Timer.print_stats()
```

Basically you wrap anything you want to time in a with `Timer('label'):` block, where `label` is an arbitrary string. Then you print the stats at the end and it will tell you how much wall-clock time, the number of calls, and the calls per second.
The stats are global, so you can `import timer` wherever you need one and then just call `Timer.print_stats()` once at the end of the main scope.
