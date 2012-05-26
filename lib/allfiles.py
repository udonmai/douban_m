#!/usr/bin/python
#-*- coding: utf-8 -*- 
import os

class file_list:
	start = 0#起始位置

	def __init__(self, path = ''):
		self.path = path
	
	def listout(self, start, end = None):
		i = start 
		filvename = ''
		path_list = []
		flag = True#标识是否有结束位置的设置
		if end == None:
			flag = False

		for root,dirs,files in os.walk(self.path):
			for filespath in files:
				if not filespath.endswith('mp3'):
					break
				filename = filespath.partition('.mp3')#分片
				path_list.append([root,filename[0]])
				i += 1
				if flag and i == end:
					return path_list

		return path_list		

