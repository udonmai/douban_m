#!/usr/bin/python
#-*- coding: utf-8 -*-
import wx
import os
import wx.lib.buttons as buttons
from lib import main
from lib import update
from lib import downFav
from eyeD3 import *

class StaticTextFrame(wx.Frame):
		Data = [0] *2
		def __init__(self):
			#将窗口放置屏幕中央
				wx.Frame.__init__(self,None,-1,'豆瓣',size=(400,340),pos=(wx.DisplaySize()[0]/2-400,wx.DisplaySize()[1]/2-300))
				self.panel  = wx.Panel(self,-1)
				#设置背景颜色 （默认为灰色）
				self.panel.SetBackgroundColour('White')
				#创建状态栏
				statusBar = self.CreateStatusBar()
				
				wildcard = "mp3 source (*.mp3)|*.mp3|" \
					"All files (*.*)|*.*"
				self.dialog1 = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
				#self.dialog2 = wx.FileDialog(None, "Choose a file:",os.getcwd()," ",wildcard,wx.OPEN)
				
				self.floderLabel  = wx.StaticText(self.panel,-1,"   -- update Files' tags: --",pos=(60,40))
				self.floderText = wx.TextCtrl(self.panel,-1,pos=(40,67),size=(200,-1))
				self.button1 = buttons.GenButton(self.panel,-1,"Browse",pos=(260,63))
				self.Bind(wx.EVT_BUTTON,self.OpenFloder,self.button1)
				self.button3= buttons.GenButton(self.panel,-1,"Go",pos=(260,100))
				self.Bind(wx.EVT_BUTTON,self.StartUp,self.button3)
				
				self.floderLabel = wx.StaticText(self.panel, -1, "   -- Download your love songs: --", pos = (40,160))
				self.nameLaber = wx.StaticText(self.panel,-1,"username:",pos=(40,180))
				self.usrText = wx.TextCtrl(self.panel,-1,pos=(40,200),size=(200,-1))
					
				self.filLabel = wx.StaticText(self.panel,-1,"password:",pos=(40,230))
				self.pwText = wx.TextCtrl(self.panel,-1,pos=(40,250),size=(200,-1),style=wx.TE_PASSWORD)
					
				self.button2 = buttons.GenButton(self.panel,-1,"Go",pos=(260,195))
				self.Bind(wx.EVT_BUTTON,self.DownGo,self.button2)

				sizer = wx.FlexGridSizer(1, 3, 0, 0)
				self.panel.SetSizer(sizer)
					
		def OpenFloder(self,event):
			if self.dialog1.ShowModal() == wx.ID_OK:
				self.floderText.WriteText(self.dialog1.GetPath())
		#			self.dialog1.Destroy()
					
		def OpenFile(self,event):
			if self.dialog2.ShowModal() == wx.ID_OK:
				self.fileText.WriteText(self.dialog2.GetPath())
	#				self.dialog2.Destroy()
					
		def StartUp(self,event):							
			main.main(self.dialog1.GetPath())
			self.Close(True)

		def DownGo(self,event):
			#print self.usrText.GetValue()
			downFav.main(self.usrText.GetValue(), self.pwText.GetValue())	
					
app = wx.PySimpleApp()
frame = StaticTextFrame()
frame.Show()
app.MainLoop()
