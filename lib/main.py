#!/usr/bin/python
#-*- coding: utf-8 -*-

from lib import allfiles
from lib import update
from lib import queue
import threading
from Queue import Queue

mylock = threading.RLock()

class main:
	#目录下所有mp3文件列表
	def __init__(self,path = ''):
		list = allfiles.file_list(path)
		mnames = list.listout(0)
	# mnames 元素个数
		num = len(mnames)
	#print num
	# 设置 queue 最多同时可以执行10个线程
		que = Queue(maxsize = 10)
	#print queue.maxsize
	# 建立producer子线程
	# 第二个 num 为 mnames 中mp3文件个数
	# 第四个参数为输出锁
		pro = queue.producer(que,num,mnames,mylock)
		pro.start()
		pro.join




