from time import time
from multiprocessing.connection import Connection


class Logger:
    dir = 'artifacts/'
    file = ''

    def __init__(self, filename):
        """
        logger is capable of writing to a file via connection. On init creates
        or replaces given filename to empty one in artifacts.
        """
        self.file = filename
        open(f'{self.dir}{self.file}.txt', 'w').close()

    def write_msg(self, msg=''):
        with open(f'{self.dir}{self.file}.txt', 'a') as fout:
            print(msg, file=fout)

    def write_total(self, start):
        self.write_msg(f'Total time: {time() - start:.4f}s')
        self.write_msg()

    def __call__(self, recv: Connection):
        """
        Recieves messages from connection and writes to current file. Breaks on
        empty string
        """
        msg = recv.recv()
        while msg:
            self.write_msg(msg)
