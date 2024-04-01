from time import time
from util import Logger


class Bootstrap:
    def __init__(self, iterations=10, filename='easy'):
        self.iterations = iterations
        self.logger = Logger(filename)

    def bootstrap(self, func, *args, **kwargs):
        self.logger.write_msg(f'Bootstrapping {func.__name__}:')
        start_total = time()
        for iter in range(self.iterations):
            start = time()
            func(*args, **kwargs)
            self.logger.write_msg(
                f'Iteration {iter} took {time() - start:.4f}s'
            )
        self.logger.write_total(start_total)

    def bootstrap_Method(self, func, Method, *args, **kwargs):
        self.logger.write_msg(
            f'Bootstrapping {func.__name__} using {Method.__name__}:'
        )
        tps = [
            Method(target=func, args=args, kwargs=kwargs)
            for i in range(self.iterations)
        ]
        start = time()
        start_total = time()
        for tp in tps:
            tp.start()
        for iter, tp in enumerate(tps):
            tp.join()
            self.logger.write_msg(
                f'Iteration {iter} took {time() - start:.4f}s'
            )
            start = time()
        self.logger.write_total(start_total)
