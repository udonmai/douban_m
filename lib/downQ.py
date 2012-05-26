# -*- coding: utf-8 -*-
import threading
import time
import downFav
from Queue import Queue


# -*- 类接受两个参数 
# -*- name 在信号量队列中的编号
# -*- queue 信号量队列

class customer(threading.Thread):
	Data = []
	def __init__(self, n, que, url, cookie):
		threading.Thread.__init__(self)
		self.que = que
		self.n = n
		self.url = url
		self.cookie = cookie

	def run(self):
		downFav.get(self.url%(self.n*15), self.cookie)
		self.que.get()

# -*- 接受两个参数	
# -*- queue 信号量队列	
# -*- num 总的信息数量

class producer(threading.Thread):
	def __init__(self, queue, num, url, cookie):
		threading.Thread.__init__(self)
		self.num = num
		self.que = queue
		self.url = url
		self.cookie = cookie

	def run(self):
		i = 0
		while i < self.num:
			n = i%self.que.maxsize
			self.que.put(n)
			#创建一个新进程
			c = customer(n, self.que, self.url, self.cookie)
			c.start()
			
			i += 1
