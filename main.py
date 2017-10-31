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

pop1 = Popup(title='Empty Data', content=Label(text='Missing values in text fields'),size_hint=(None,None),size=(280,100))
pop2 = Popup(title='Page4', content=Label(text='To be continue'),size_hint=(None,None),size=(280,100))
pop_unsucess = Popup(title='Result:', content=Label(text='None'),size_hint=(None,None),size=(280,100))

class Organization(Spinner):
	def run_org(self,ipadd,prt,**kwargs):
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
		new_strOrgID = ""
		for a in range (0, len(org1_data['results'])):
			if (org1_data['results'][a]['organization_name'] == str(org)):
				str_orgID = org1_data['results'][a]['_id']
				new_strOrgID = str_orgID
		
		for i in range (0, len(data['results'])):
			if (data['results'][i]['organization_id'] == new_strOrgID):
				self.values.append((str(data['results'][i]['building_name'])))
	
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
		new_strBldID = ""
		for a in range (0, len(bld1_data['results'])):
			if (bld1_data['results'][a]['building_name'] == str(bld)):
				str_bldID = bld1_data['results'][a]['_id']
				new_strBldID = str_bldID
		
		for i in range (0, len(data['results'])):
			if (data['results'][i]['building_id'] == new_strBldID):
				self.values.append((str(data['results'][i]['floor_name'])))

class AppScreen(Screen):
    pass


class FirstForm(AppScreen):
	splash = NumericProperty()
	def __init__(self, **kwargs):
		super(FirstForm, self).__init__(**kwargs)
		Clock.schedule_once(self.callNext, 3)

	def callNext(self,dt):
		self.manager.current = 'secondform'
		print "Hi this is call Next Function of loading 1"
		
		
	
class SecondForm(AppScreen):
        def enter_ip(self,ipadd,prt,**kwargs):
			if (ipadd=='' or prt == ''):
				print pop1.title
				pop1.open()
			else:
				super(SecondForm,self).__init__(**kwargs)
				search_url = "http://"+ipadd+":"+prt+"/heartbeat"
				print "\n"+"http://"+ipadd+":"+prt+"/heartbeat"+"\n"
				self.request = UrlRequest(search_url, self.res)
				print self.request
				print "Result: before success", self.request.result,"\n"
				
        def res(self,*args):
			print "Result: after success", self.request.result
			self.manager.current = 'thirdform'
			
        def back(self,*args):
			self.manager.current = 'secondform'
			
			
class ThirdForm(AppScreen):	
		def open_popup(self):
			pop2.open()

		
class main(App):
    def build(self):
        config = self.config
        self.title = "App title here"
        self.root = Builder.load_file('main.kv')
        return self.root
				
				
if __name__=='__main__':
	main().run()
