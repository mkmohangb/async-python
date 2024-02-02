From [how async/await works in python](https://tenthousandmeters.com/blog/python-behind-the-scenes-12-how-asyncawait-works-in-python/)

All the ```echo_*``` scripts implement an Echo server.
1. ```echo_seq.py``` - with sequential execution, can handle only one client at a time.
2. ```echo_threads.py``` - a thread is spawned when accepting a new client connection
3. ```echo_thread_pool.py``` - pick the next available thread from a pool of threads to handle a new client connection
4. ```echo_io_mux.py``` - Event loop based using selectors to listen for socket events. Not fully non-blocking - as ```sendall``` might block. Uses callback style programming.

- The key insight we can derive with OS threads which doesn't impose callback based model but provides concurrency is the ability of the OS to suspend/resume execution of threads. With python generators we can achieve the same within a function.
  
5. ```echo_yield_io.py``` - Event loop based using generators to yield control
   
- Coroutines are functions that can be suspended by explicitly yielding the control. A true coroutine, however, should also be able to yield the control to other coroutines by calling them, but generators can yield the control only to the caller.
  
6. ```echo_yield_from.py``` - using ```yield_from``` which allows some nice refactoring of the code into subgenerators.

- native coroutine - defined using ```async def``` syntax
- generator based coroutine - generator decorated with ```@types.coroutine```

7. ```echo_async_await.py``` - Using async/await (which is just a syntactic feature on top of generators)

8. ```client.py``` - async/await based client to interact with the server.
