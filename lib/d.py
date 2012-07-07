#! 
# -*- coding:utf-8 -*- 
from BeautifulSoup import BeautifulSoup
from eyeD3 import *
import sys
import downQ
import threading
from Queue import Queue
import urllib,urllib2,cookielib,re
from urllib import urlencode
 
def handle(s):
    return s.replace("&lt;","<").replace("&gt;",">").replace("\\","")
   
def fhandle(s):
    return s.replace("/","and").replace(" ","")

#修改tag信息
def modify(path, s1, s2, s3, img_path):
	tag = eyeD3.Tag()
	tag.link(path)
	if not tag.link(path):
		tag.header.setVersion(eyeD3.ID3_V2_3)
	tag.encoding = '\x01'
	
	tag.setTitle(s1)
	tag.setArtist(s2)
	tag.setAlbum(s3)

	img = urllib.urlopen(img_path).read()
	temp = file('temp.jpg','wb')
	temp.write(img)
	temp.close()
	tag.addImage(3,'temp.jpg',u"")
	tag.update()
 
def get(myurl,cj):
    url2="http://douban.fm/j/mine/playlist?type=n&h=&channel=0&context=channel:0|subject_id:%d"
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    req=urllib2.Request(myurl)
    req.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    #req.add_header('Cookie',cookie)
    content=urllib2.urlopen(req).read()
    soup=BeautifulSoup(str(content))
    soup=soup.find("div", { "id" : "record_viewer" })
    for div in soup.findAll("div", { "class" : "info_wrapper" }):
		div=div.find("div",{ "class" : "song_info" })
		a=div.contents[1]
		p1,p2,p3=div.contents[3].findAll("p")
		print a["href"]+"\nsong:"+handle(p1.string)+"\nsinger:"+handle(p2.string)+"\nalbum:"+handle(p3.a.string)
		p=re.compile(r'(\d+)')
		m=p.search(a["href"])
		num=int(m.groups()[0])
		url3=url2%num
		#print url3
		mark=False
		#获取专辑封面
		sub_path = a["href"]#专辑链接
		req2 = urllib2.Request(sub_path)
		content2 = urllib2.urlopen(req2).read()
		soup2 = BeautifulSoup(str(content2))
		soup2 = soup2.find("div", {"id" : "mainpic"})
		img_pathc = soup2.contents[0]
		img_path = img_pathc["href"]

		try:
			for j in range(100):
				content=urllib2.urlopen(url3).read()
				c=eval(content)
				c=c['song']
				for i in c:
					if unicode(str(i['title']),'utf-8')==handle(p1.string):
						local = "Incoming/" + fhandle(handle(p1.string)) + "-" + fhandle(handle(p2.string)) + ".mp3"
						urllib.urlretrieve(i['url'].replace('\\',''), local)
						modify(local, fhandle(handle(p1.string)), fhandle(handle(p2.string)), fhandle(handle(p3.a.string)), img_path)
						mark=True
						break
				if mark:
					break
			if mark:
				print "succeed!\n"
			else: print "fail!\n"
		except Exception as e:
			print e.message

def login(usrname, pwd):
	#https://www.douban.com/accounts/login
	#alias form_password
	cj = cookielib.LWPCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	opener.addheaders = [
			("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.5) Gecko/20031107 Debian/1.5-3"), 
			("Accept", "text/html, image/jpeg, image/png, text/*, image/*, */*")
			]

	data = {
			'source' : 'radio',
			'alias' : usrname,
			'form_password' : pwd
			}

	urldata = urlencode(data)
	r = opener.open("http://douban.fm/j/login", urldata)
	
	#result = r.read()
	#print result
	cj.save('cookie')
	
	return cj

def main():
    url="http://douban.fm/mine?start=%d&type=liked"
    #cookie=raw_input('cookie:')

    #print u,p
	#print 'please input your douban ID'
    u = raw_input('username:')
    p = raw_input('password:')
    cj = login(u, p)
	
    print "you should enter the pages you want to download"
    #page0=int(raw_input('page from:'))
    page1=int(raw_input('page to:'))
    num = page1
    que = Queue(maxsize = 10)
    process = downQ.producer(que, num, url, cj)
    process.start()
    process.join

    #u = raw_input('username:')
    #p = raw_input('password:')
    #login(u, p)

    #for i in range(page1):
    #   get(url%(i*15),cookie)
 
if __name__ == "__main__":
    main()
