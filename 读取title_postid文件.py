import json

with open('title_postid.json','rb') as fr:
    data = json.load(fr)

s = '''
11130272 操作系统的发展史
11130244 进程基础
11130238 进程调度
11130250 进程的并行和并发
11130263 同步异步阻塞非阻塞
11130239 进程的创建和结束
11130256 Python程序中的进程操作-开启多进程(multiprocess.process)
11130253 Python程序中的进程操作-进程同步(multiprocess.Lock)
11130293 Python程序中的进程操作-进程间通信(multiprocess.Queue)
11130265 Python程序中的进程操作-进程间数据共享(multiprocess.Manager)
11130258 Python程序中的进程操作-进程池(multiprocess.Pool)
'''

for k,v in data.items():
    if k in s:
        print(k,v)