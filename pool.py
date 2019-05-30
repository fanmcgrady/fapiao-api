import os
import time
from multiprocessing import Pool

import API_test as api


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    # time.sleep(random.random() * 3)
    # print(api.run_qrcode())
    print(api.run_type())
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    p = Pool()
    for i in range(20):
        p.apply_async(long_time_task, args=(i,))
    p.close()
    p.join()
