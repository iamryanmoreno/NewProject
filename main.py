from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty, ListProperty)
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore
from os.path import join
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
import urllib2
import json
import requests
from tinydb import TinyDB, Query
import unicodedata
from pprint import pprint
import serial
from base import Base
import threading
import os
import time
from kivy.clock import Clock
import datetime
import serial
import kivy
from kivy.uix.image import AsyncImage
from kivy.uix.carousel import Carousel
import pathlib
import io

print(kivy.__version__)

pop1 = Popup(title='Empty Data', content=Label(text='Missing values in text fields'),size_hint=(None,None),size=(280,100))
pop2 = Popup(title='Page4', content=Label(text='To be continue'),size_hint=(None,None),size=(280,100))
pop_unsucess = Popup(title='Result:', content=Label(text='None'),size_hint=(None,None),size=(280,100))

class Organization(Spinner):
	def run_org(self,ipadd,prt,**kwargs):
		if (ipadd=='' or prt == ''):
			print 'IP Add and Port empty'
		else:
			org_url = "http://"+ipadd+":"+prt+"/organizations"
			org = urllib2.urlopen(org_url)
			data = org.read()
			data = json.loads(data)
			self.values = []
			for i in range (0, len(data['results'])):
				values1 = str(data['results'][i]['organization_name'])
				self.values.append(values1)
		
class Building(Spinner):
	def run_bld(self,ipadd,prt,org,**kwargs):
		self.text = ''
		bld_url = "http://"+ipadd+":"+prt+"/buildings"
		bld = urllib2.urlopen(bld_url)
		data = bld.read()
		data = json.loads(data)
		self.values = []
		org_url = "http://"+ipadd+":"+prt+"/organizations"
		org1 = urllib2.urlopen(org_url)
		org_data = org1.read()
		org1_data = json.loads(org_data)
		organization_id = ""
		for a in range (0, len(org1_data['results'])):
			if (org1_data['results'][a]['organization_name'] == str(org)):
				str_orgID = org1_data['results'][a]['_id']
				organization_id = str_orgID
		
		for i in range (0, len(data['results'])):
			if (data['results'][i]['organization_id'] == organization_id):
				self.values.append((str(data['results'][i]['building_name'])))
				
		print "Organization id: " + organization_id
class Floor(Spinner):
	def run_flr(self,ipadd,prt,bld,**kwargs):
		self.text = ''
		flr_url = "http://"+ipadd+":"+prt+"/floors"
		flr = urllib2.urlopen(flr_url)
		data = flr.read()
		data = json.loads(data)
		self.values = []
		
		bld_url = "http://"+ipadd+":"+prt+"/buildings"
		bld1 = urllib2.urlopen(bld_url)
		bld_data = bld1.read()
		bld1_data = json.loads(bld_data)
		building_id = ""
		for a in range (0, len(bld1_data['results'])):
			if (bld1_data['results'][a]['building_name'] == str(bld)):
				str_bldID = bld1_data['results'][a]['_id']
				building_id = str_bldID
		
		for i in range (0, len(data['results'])):
			if (data['results'][i]['building_id'] == building_id):
				self.values.append((str(data['results'][i]['floor_name'])))
				
		print "Building ID: " + building_id
		

class AppScreen(Screen):
    pass


class FirstForm(AppScreen,Base):
	def __init__(self, **kwargs):
		super(FirstForm, self).__init__(**kwargs)
		filepath = pathlib.Path(__file__).resolve().parent
		fname = str(filepath) + "\save_config.json"
		if os.path.isfile(fname):
			print "\n***** save_config.json DOES exist *****\n"
			Clock.schedule_once(self.callFourth, 2)
		else:
			print "\n***** save_config.json DOES NOT exist *****\n"
			print os.path.isfile(fname)
			Clock.schedule_once(self.callNext, 2)

	def callNext(self,dt):
		self.manager.current = 'secondform'
		print "Loading Splash Screen done"
		
	def callFourth(self,dt):
		self.manager.current = 'fourthform'
		Clock.schedule_interval(self.display_datetime,0.1)
		threading.Thread(target=self.update_data).start()
		filepath = pathlib.Path(__file__).resolve().parent
		fname = str(filepath) + "\chosen.json"
		ippath = str(filepath) + "\save_config.json"
		with open(fname) as data_file:
			data_loaded = json.load(data_file)
			self.dis_org.text = data_loaded['organization']
			print "\n*****************************************\n"
			print '\nOrganization: ' + data_loaded['organization']
			print 'Building: ' + data_loaded['building']
			print 'Floor: ' + data_loaded['floor']
			
		
		with open(ippath) as path_file:
			path_loaded = json.load(path_file)
			print '\nIP: ' + path_loaded['ip_add']
			print 'Port: ' + path_loaded['port']
			print "\n*****************************************\n"
			
	def display_datetime(self, *args):
		date_now = datetime.datetime.now().strftime('%a %d %b %Y')
		time_now = datetime.datetime.now().strftime('%I:%M %p')
		self.lb_date.text = date_now
		self.lb_time.text = time_now
		
	def update_data(self, *args):
		line_num = 0
		filepath = pathlib.Path(__file__).resolve().parent
		fname1 = str(filepath)
		if self.debug:
			f = open(fname1 + '\sample.txt', 'r')
			lines = f.readlines()
		while True:
			if self.debug:
				if line_num == len(lines) - 1:
					line_num = 0
				else:
					line_num += 1
				data = lines[line_num][:-1]
				print "Line number: ", line_num
			else:
				data = ''
			if data.startswith('[02]'):
				data_header = data[4:6]
				data_list = ['00', '02']
				if data_header in data_list:
					content = data[7:-5]
					tmp = '[b][color=FFEC1F]' + content + '[/color][/b]'
					self.glb_amt.text = tmp
			time.sleep(.5)
	
class SecondForm(AppScreen):
        def enter_ip(self,ipadd,prt,**kwargs):
			if (ipadd=='' or prt == ''):
				print pop1.title
				pop1.open()
			else:
				super(SecondForm,self).__init__(**kwargs)
				search_url = "http://"+ipadd+":"+prt+"/heartbeat"
				print "\n"+"http://"+ipadd+":"+prt+"/heartbeat"+"\n"
				
				try:
					to_unicode = unicode
				except NameError:
					to_unicode = str
					
				# Define data
				data = {'ip_add': ipadd,'port': prt}

				# Write JSON file
				filepath = pathlib.Path(__file__).resolve().parent
				fname = str(filepath) + "\save_config.json"
				
				with io.open(fname, 'w', encoding='utf8') as outfile:
					str_ = json.dumps(data,
									  indent=4, sort_keys=True,
									  separators=(',', ': '), ensure_ascii=False)
					outfile.write(to_unicode(str_))

				# Read JSON file
				with open(fname) as data_file:
					data_loaded = json.load(data_file)

				print "Here it is " + str(data == data_loaded)
				
				
				self.request = UrlRequest(search_url, self.res)
				print self.request
				print "Result: before success", self.request.result,"\n"
				


				
        def res(self,ipadd,prt,*args):
			print "Result: after success", self.request.result
			self.manager.current = 'thirdform'
			
        def back(self,*args):
			self.manager.current = 'secondform'
			
        def start(self):
			url = 'loader2.gif'
			return CenteredAsyncImage(source=url)
			
class ThirdForm(AppScreen):	
	def open_popup(self):
		pop2.open()
	def proceed(self,ipadd,prt,org,bld,flr,*args):
	
	
		flr_url = "http://"+ipadd+":"+prt+"/floors"
		flr1 = urllib2.urlopen(flr_url)
		data = flr1.read()
		data = json.loads(data)
		
		floor_id = ""
		for a in range (0, len(data['results'])):
			if (data['results'][a]['floor_name'] == str(flr)):
				str_flrID = data['results'][a]['_id']
				floor_id = str_flrID
		
		print "Floor ID: " + floor_id
		
		try:
			to_unicode = unicode
		except NameError:
			to_unicode = str
					
		# Define data
		data = {'organization': org,'building': bld, 'floor': flr}

		# Write JSON file
		filepath = pathlib.Path(__file__).resolve().parent
		fname = str(filepath) + "\chosen.json"
				
		with io.open(fname, 'w', encoding='utf8') as outfile:
			str_ = json.dumps(data,
							indent=4, sort_keys=True,
							separators=(',', ': '), ensure_ascii=False)
			outfile.write(to_unicode(str_))
		# Read JSON file
		with open(fname) as data_file:
			data_loaded = json.load(data_file)

		print "Here it is " + str(data == data_loaded)

		
		#print "Organization: " + org + "\n" + "Building: " + bld + "\n" + "Floor: "+ flr + "\n"
		self.manager.current = 'fourthform'

class FourthForm(AppScreen,App,Base):
    def build(self):
        Base.__init__(self)
        Clock.schedule_interval(self.display_datetime,0.1)
        threading.Thread(target=self.update_data).start()
        return self.root
		
    def display_datetime(self, *args):
        #time_now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        date_now = datetime.datetime.now().strftime('%a %d %b %Y')
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        self.lb_date.text = date_now
        self.lb_time.text = time_now
		
    def update_data(self, *args):
        line_num = 0
        if self.debug:
            f = open(self.cur_dir + 'sample.txt', 'r')
            lines = f.readlines()
        while True:
            if self.debug:
                if line_num == len(lines) - 1:
                    line_num = 0
                else:
                    line_num += 1
                data = lines[line_num][:-1]
                print "Line number: ", line_num
            else:
                data = ''
            if data.startswith('[02]'):
                data_header = data[4:6]
                data_list = ['00', '02']
                if data_header in data_list:
                    content = data[7:-5]
                    tmp = '[b][color=FFEC1F]' + content + '[/color][/b]'
                    self.glb_amt.text = tmp
            time.sleep(.5)
			
class CenteredAsyncImage(AsyncImage):
	pass

class FormCarousel1(Carousel):
	pass
class FormCarousel2(Carousel):
	pass
class FormCarousel3(Carousel):
	pass
	
class main(App):
    def build(self):
        config = self.config
        self.title = "App title here"
        self.root = Builder.load_file('main.kv')
        return self.root
				
				
if __name__=='__main__':
	main().run()
