from time import time
from util import Logger
from concurrent.futures import as_completed


class Pool_Executor_logger:
    def __init__(self, filename='medium'):
        self.logger = Logger(filename)

    def Pool_Executor_func(self, func, Method, *args, **kwargs):
        kwargs['n_jobs'] = kwargs.get('n_jobs') or 10
        self.logger.write_msg(
            f'Starting {Method.__name__} with {kwargs['n_jobs']} workers'
        )
        with Method(max_workers=kwargs['n_jobs']) as executor:
            future_starts = {}
            start = time()
            for i in range(kwargs['n_jobs']):
                kwargs['start'] = i
                future = executor.submit(func, *args, **kwargs)
                future_starts[future] = i
                self.logger.write_msg(f'Started job #{i + 1}')
            result = 0
            for future in as_completed(future_starts.keys()):
                result += future.result()
                self.logger.write_msg(
                    f'Finished job #{future_starts[future] + 1}'
                )
            self.logger.write_msg(f'Result is {result}')
        self.logger.write_total(start)
