from collections import deque
import selectors
import socket

class EventLoopYieldFrom:
    def __init__(self):
        self.tasks_to_run = deque([])
        self.sel = selectors.DefaultSelector()

    def create_task(self, coro):
        self.tasks_to_run.append(coro)

    def sock_recv(self, sock, n):
        yield 'wait_read', sock
        return sock.recv(n)

    def sock_sendall(self, sock, data):
        yield 'wait_write', sock
        sock.sendall(data)

    def sock_accept(self, sock):
        yield 'wait_read', sock
        return sock.accept()

    def run(self):
        while True:
            if self.tasks_to_run:
                task = self.tasks_to_run.popleft()
                try:
                    op, arg = next(task)
                except StopIteration:
                    continue

                if op == 'wait_read':
                    self.sel.register(arg, selectors.EVENT_READ, task)
                elif op == 'wait_write':
                    self.sel.register(arg, selectors.EVENT_WRITE, task)
                else:
                    raise ValueError('Unknown event loop operation: ', op)
            else:
                for key, _ in self.sel.select():
                    task = key.data
                    sock = key.fileobj
                    self.sel.unregister(sock)
                    self.create_task(task)

loop = EventLoopYieldFrom()

def run_server(host='127.0.0.1', port=55556):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = yield from loop.sock_accept(sock)
        print('Connection from ', addr)
        loop.create_task(handle_client(client_sock))

def handle_client(sock):
    while True:
        received_data = yield from loop.sock_recv(sock, 4096)
        if not received_data:
            break
        yield from loop.sock_sendall(sock, received_data)

    print('Client disconnected: ', sock.getpeername())
    sock.close()

if __name__ == '__main__':
    loop.create_task(run_server())
    loop.run()
