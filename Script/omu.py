# -*-coding:Latin-1 -*

#from ftplib import FTP 
#from fabric.api import *
import os
import sys
import telnetlib
import getpass
import time
import re
import random
import time

class OMU():

	def __init__(self, host, user,password):
		self.HOST=host
		
		self.USER=user
		self.PASSWORD=password 
		print(self.HOST, self.USER, self.PASSWORD)
		self.TELNET= telnetlib.Telnet(self.HOST)
		self.TELNET.read_until("login: ")

		self.TELNET.write(self.USER+"\r\n")
		if self.PASSWORD:
			self.TELNET.read_until("Password: ")
			self.TELNET.write(self.PASSWORD+"\n")



		#self.reset_tmu()
	
	def reset_tmu(self):
		self.TMU_reset= False
		self.get_list_tmu()
		tmu = random.choice(self.List_tmu)
		print("\n\nchoice==> "),
		tmu_sbc=tmu+"_sbc"
		print(tmu)
		self.TELNET.write("telci "+tmu_sbc+"\n")
		time.sleep(5)
		self.TELNET.write("bexc freeze\n")
		time.sleep(5)
		self.TELNET.write("Q\n")
		time.sleep(5)
		self.TELNET.write('exit\n')
		time.sleep(5)
		self.TMU_reset= True
		return tmu


	def get_list_tmu(self):
		patterns= r"tmu_[\w\.-]+[0-9]"

		self.TELNET.write("ftViCpTable\n")
		time.sleep(5)
		txt= self.TELNET.read_very_eager()
		self.List_tmu= re.findall(patterns, txt)

