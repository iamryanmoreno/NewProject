from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from base import Base
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
			self.values.append((str(data['results'][i]['organization_name'])))
		
		
class Building(Spinner):
	def run_bld(self,ipadd,prt,org,**kwargs):
		org_url = "http://"+ipadd+":"+prt+"/buildings"
		org = urllib2.urlopen(org_url)
		data = org.read()
		data = json.loads(data)
		self.values = []
	
class Floor(Spinner):
	def run_flr(self,ipadd,prt,**kwargs):
		org_url = "http://"+ipadd+":"+prt+"/floors"
		org = urllib2.urlopen(org_url)
		get_values = org.read()
		get_values = json.loads(get_values)
		get_values = json.load(urllib2.urlopen(org_url))
		self.values = get_values


class AppScreen(Screen):
    pass

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
				
				'''
				db = TinyDB('D:/savemuna.json')
				User = Query()
				db.insert({'ip': ipadd, 'port': prt})
				result = db.search(User.ip == ipadd)
				print result
				'''
        def res(self,*args):
			print "Result: after success", self.request.result
			self.manager.current = 'thirdform'
			
			
class ThirdForm(AppScreen):	
		def open_popup(self):
			pop2.open()
		
class MainWindow(AppScreen):
        def exit_app(self):
                sys.exit()

class First(App, Base):
    def work(self):
        self = Builder.load_file('main.kv')
		
class main(App):
        def build(self):
                "Splash Screen"
                wing = Image(source='img/dummy.png', pos=(800,800))
                animation = Animation(x=0,y=0,d=2,t='out_bounce');
                animation.start(wing)
                Clock.schedule_once(First.work,100)
                self = Builder.load_file('main.kv')
                return self
				
class main1(App, Base):
				
        def build(self):
                config = self.config
                self.title = "App title here"
                self.root = Builder.load_file('main.kv')
                Base.__init__(self)
                return self.root
				
if __name__=='__main__':
	main().run()
