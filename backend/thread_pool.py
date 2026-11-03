import logging
from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop

_EXECUTOR = ThreadPoolExecutor(max_workers=2)


def run_cpu_bound(target, *args):
    '''Run target(*args) on the CPU-bound pool.

    Returns an awaitable that resolves on the IOLoop thread with the result
    (or raises the exception) of the call. Must be called from the IOLoop thread.
    '''
    logging.info('run_cpu_bound: %s%r', target, args)
    return IOLoop.current().run_in_executor(_EXECUTOR, target, *args)


def run_in_thread(target, *args):
    '''Like run_cpu_bound, but uses the IOLoop's default executor, so slow
    jobs (dataset reloads, uploads) don't starve the CPU-bound pool.'''
    return IOLoop.current().run_in_executor(None, target, *args)
