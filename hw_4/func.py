def integrate(f, a, b, start=0, n_jobs=1, n_iter=10_000_000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(start, n_iter, n_jobs):
        acc += f(a + i * step) * step
    return acc


def fib(n):
    prev, cur = 0, 1
    for i in range(n):
        prev, cur = cur, prev + cur
    return cur
