# -*- coding:utf-8 -*-
import urllib
import urllib2
import sys
import os
import json
from eyeD3 import *
import time
import threading

reload(sys)
sys.setdefaultencoding('utf-8')

class update:
	key = "apikey=01fba2d8a9c8dd4c05f2e889fd5a97e4"
	def __init__(self,filename,Lock,start_index = 1):
		self.filename = []
		self.filename = filename
		self.mylock = Lock
		self.maxresults = "10"
		self.start_index = start_index
	#	print self.filename[1]
	#返回歌曲信息
	def search(self):
		self.url = "http://api.douban.com/music/subjects"
		self.url = self. url + "?" + "q=" + self.filename[1] + "&start-index=" + str(self.start_index) + "&maxresults=" + self.maxresults +"&alt=json&" + self.key
		#print self.start_index
		#print self.url
		try:
			req = urllib2.Request(self.url)
			fd = urllib2.urlopen(req)
			#print "a"
			data = fd.read()
			entries = json.loads(data)
			author = 'author'
			Data ={}
			#print self.filename[1]
			#满足符合的歌曲总数
			Len = json.dumps(entries['opensearch:totalResults'],ensure_ascii=False)	
			Sum = int(Len[8:len(Len)-2])
			#如果没有查询到结果
			#if self.start_index == 1:
			self.mylock.acquire()
			print self.url
			print  "歌名",self.filename[1]
			if Sum == 0:
				print "Not Found!"
				self.mylock.release()
				return
			#如果仅存在一条结果
			elif Sum == 1:
				entry = entries['entry'][0]
				if author in entry:
					Data['author'] = json.dumps(entry['author'][0]['name'],ensure_ascii = False)
					Data['author'] = Data['author'][8:len(Data['author'])-2]
				else:
					Data['author'] = ''
				Data['Album'] = json.dumps(entry['title'],ensure_ascii = False)
				Data['Album'] = Data['Album'][8:len(Data['Album'])-2] 
				Data['img'] = json.dumps(entry['link'][2],ensure_ascii = False)
				Data['img'] = Data['img'][28:len(Data['img'])]
				self.mylock.release()
			#如果存在多条结果
			else:
				i = 1
				for entry in entries['entry']:
					if author in entry:
						#Data['author'] = json.dumps(entry['author'][0]['name'],ensure_ascii = False) #专辑名
						temp = json.dumps(entry['author'][0]['name'],ensure_ascii = False)
						print i,temp[8:len(temp)-2]
						#print i,json.dumps(entry['author'][0]['name'],ensure_ascii = False)
					else:
						#Data['author'] = ''
						print i,' '
					temp = json.dumps(entry['link'][2],ensure_ascii = False)
					print temp[28:len(temp)-2]
					temp = json.dumps(entry['title'],ensure_ascii = False)
					print temp[8:len(temp)-2]
					print "--------------------------------------------------"
					#Data['img'] = json.dumps(entry['link'][2],ensure_ascii = False)
					#print json.dumps(entry['link'][2],ensure_ascii = False)		#专辑封面url
					#print json.dumps(entry['title'],ensure_ascii = False)
					#Data['Album'] = json.dumps(entry['title'],ensure_ascii=False)  	#歌手名
					i+=1
				if Sum-self.start_index > 0:
					print str(i) + " 下一页"
				id = input("please input the id:\n")
				#根据用户输入更新文件信息
				#如果用户点击了下一页
				if id == i:
					self.start_index += 10
				#	print self.start_index
					self.search()
				else:
					print "您选择了:"
					result = entries['entry'][id-1]
					if author in result:
						Data['author'] = json.dumps(result['author'][0]['name'],ensure_ascii = False)
						Data['author'] = Data['author'][8:len(Data['author'])-2]	#歌手名
						print Data['author']
					Data['img'] = json.dumps(result['link'][2],ensure_ascii = False)	#专辑封面url
					Data['img'] = Data['img'][28:len(Data['img'])-2]
					print Data['img']
					Data['Album'] = json.dumps(result['title'],ensure_ascii = False)	#专辑名
					Data['Album'] = Data['Album'][8:len(Data['Album'])-2]
					print Data['Album']
					print '-----------------------------------------------------------'
				#	time.sleep(3)
					#self.start_index = 1
					#释放锁
					#
					self.mylock.release()
					self.refresh(Data)
			#if self.start_index == 1:
			#	self.mylock.release()
		except:
			print "服务器连接失败!";
		#	self.mylock.release()
	#更新歌曲信息 
	def refresh(self,data):
	#	print data['author']
	#	print data['Album']
	#	print data['img']
		tag = eyeD3.Tag()
		try:
	#		print self.filename[0] + '/' + self.filename[1] + '.mp3'
			path = self.filename[0] + '/' + self.filename[1] + '.mp3'
			if not tag.link(path):#如果mp3文件没有tag信息 设置
				tag.header.setVersion(eyeD3.ID3_V2_3)
			tag.removeImages()
			tag.encoding = '\x01'
			#设置歌手
			tag.setArtist(data['author'])
	#		print tag.getArtist()
			#设置专辑
			tag.setAlbum(data['Album'])
	#		print tag.getAlbum()
			img = urllib.urlopen(data['img']).read()
			temp = file('temp.jpg','wb')
			temp.write(img)
			temp.close()
			tag.addImage(3,'temp.jpg',u"")
			tag.update()
		except:
			print "该mp3文件类型不支持!";
