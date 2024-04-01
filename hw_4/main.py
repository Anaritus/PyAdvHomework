from easy import Bootstrap
from medium import Pool_Executor_logger
from threading import Thread
from multiprocessing import Process
from func import fib, integrate
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import math


BIG_NUM = int(1e5)


def solve_easy():
    easy = Bootstrap()
    easy.bootstrap(fib, BIG_NUM)
    easy.bootstrap_Method(fib, Thread, BIG_NUM)
    easy.bootstrap_Method(fib, Process, BIG_NUM)


def solve_middle():
    def get_args(Method):
        return (integrate, Method, math.cos, 0, math.pi / 2)

    pool_exe = Pool_Executor_logger()

    for n_jobs in range(1, 20):
        pool_exe.Pool_Executor_func(
            *get_args(ThreadPoolExecutor), n_jobs=n_jobs
        )
        pool_exe.Pool_Executor_func(
            *get_args(ProcessPoolExecutor), n_jobs=n_jobs
        )


# def solve_hard():
#     main.start()


if __name__ == '__main__':
    mode = int(input('Task to solve(1-3): '))
    if mode == 1:
        solve_easy()
    elif mode == 2:
        solve_middle()
