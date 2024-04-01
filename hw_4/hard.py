from util import logger, reset
from time import time, sleep
from multiprocessing import Queue, Pipe, Process
from multiprocessing.connection import Connection
from codecs import encode

start = time()


def main_chat(send: Connection):
    msg = input('Oh hi! input msg to code (empty to exit): ')
    while msg:
        send.send(msg)
        msg = input(': ')


def handle_A(recv: Connection, send: Connection):
    TIMEOUT_S = 5
    queue = Queue()
    msg = recv.recv()
    while msg:
        write_msg(
            f'received message from main at {time() - start:.2f}s: {msg}'
        )
        queue.put(msg)
        sleep(TIMEOUT_S)
        send.send(queue.get().lower())
        write_msg(f'sent message to B at {time() - start:.2f}s: {msg}')
        msg = recv.recv()


def handle_B(recv: Connection, send: Connection):
    msg = recv.recv()
    while msg:
        write_msg(f'received message from A at {time() - start:.2f}s: {msg}')
        send.send(encode(msg, 'rot13'))
        write_msg(f'sent message to printer at {time() - start:.2f}s: {msg}')
        msg = recv.recv()


def printer(recv: Connection):
    code = recv.recv()
    while code:
        write_msg(f'received message from B at {time() - start:.2f}s: {code}')
        if not code:
            break
        print(f'Here is your code: {code}')
        print(':', end=' ')


a_recv, main_send = Pipe()
b_recv, a_send = Pipe()
printer_connection, b_send = Pipe()

a = Process(target=handle_A, args=(a_recv, a_send))
b = Process(target=handle_B, args=(b_recv, b_send))
prinet_process = Process(target=printer, args=(printer_connection,))

if __name__ == '__main__':
    reset('hard')
    a.start()
    b.start()
    prinet_process.start()

    main_chat(main_send)

    main_send.send('')
    a_send.send('')
    b_send.send('')

    a.join()
    b.join()
    prinet_process.join()
