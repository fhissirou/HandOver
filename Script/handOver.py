# -*-coding:Latin-1 -*

import serial
import time
import sys
import os
import pickle
from Tkinter import *
import interfaceFrame
from threading import*
import Option
import time
import omc
import omu



VERROU=  RLock()
global CONFIRM
global RING_STATUS
CONFIRM= True
baudrate=9600


def begin_handOver(simple, tmu, ptp, data, vgcs, rec, vbs):
	global RING_STATUS
	Option.RUNNING= True
	RING_STATUS= False
	Option.progress_Bar()
	thread_receives=MobileReceives()
	thread_transmitter= MobileTransmitter(simple, tmu, ptp, data, vgcs, rec, vbs)
	thread_receives.start()
	thread_transmitter.start()


	#thread_limit_waiting= Thread(target= Option.limit_waiting)
	#thread_limit_waiting.start()


class MobileReceives(Thread):

	def __init__(self):
		Thread.__init__(self)
		with VERROU:
			self.phone= serial.Serial(interfaceFrame.VALUE_BOX_COM2.get(), baudrate, timeout=1)
		if self.phone.isOpen():
			self.phone.write(b"ATS0=1\r")
	def run(self):
		global RING_STATUS
		time.sleep(2)
		if self.phone.isOpen():
			with VERROU:
				self.phone.write(b"AT+CBST="+interfaceFrame.VALUE_ENTRY_ATCBST.get()+b'\r')
			time.sleep(3)
			with VERROU:
				self.phone.readlines()

			while Option.RUNNING == True:
				if RING_STATUS == True:
					time.sleep(3)
					reponse= Option.split_chaine(self.phone.readlines(), "")
					if (reponse.find("CONNECT") != -1) or (reponse.find("CONNECT") != -1):
						RING_STATUS= False
					else:
						with VERROU:
							self.phone.write(b"ATA\r")
							time.sleep(2)
						RING_STATUS= False
			with VERROU:
				self.phone.close()
		else:
			print("Can not open '"+interfaceFrame.VALUE_BOX_COM2.get())




class MobileTransmitter(Thread):

	def __init__(self, simple, tmu, ptp, data, vgcs, rec, vbs):
		Thread.__init__(self)
		self.SIMPLE= simple
		self.RTMU= tmu
		self.PTP= ptp
		self.DATA= data
		self.VGCS= vgcs
		self.REC= rec
		self.VBS= vbs
		self.Filename= open(os.path.dirname(__file__)+"/../File/Rapport.txt", "w")
		
		with VERROU:
			self.phone= serial.Serial(interfaceFrame.VALUE_BOX_COM1.get(), baudrate, timeout=1)

	def ptp(self, tmu_mode):
		global RING_STATUS
		nb_atd= 5
		connect_phone=False

		if self.phone.isOpen():
			self.phone.readlines()
			with VERROU:
				self.phone.write(b"ATD"+interfaceFrame.VALUE_ENTRY_PHONE_NUMERO.get()+b";\r")
				time.sleep(2)

			while nb_atd > -1:
				time.sleep(10)
				with VERROU:
					reponse= Option.split_chaine(self.phone.readlines(), "")

					time.sleep(2)
				if reponse.find("OK") != -1:
					RING_STATUS = True
					break
				else:
					with VERROU:
						self.phone.write(b"ATD"+interfaceFrame.VALUE_ENTRY_PHONE_NUMERO.get()+b";\r")
						time.sleep(2)
				nb_atd -=1
			
			if nb_atd > -1:
				time.sleep(30)
				reponse= Option.split_chaine(self.phone.readlines(), "")
				connect_phone= True

				if (RING_STATUS== False) and (Option.RUNNING == True):
					nb=1
					if tmu_mode == True:
						while nb <= self.NBRTMU:
							state_omu1= self.HO_OMU1.reset_tmu()
							state_omu2= self.HO_OMU2.reset_tmu()
							#with VERROU:
							state_ho =self.HO_OMC.run_senario("ptp")
							time.sleep(240)
							nb+=1
							text_save=str(nb)+" - CALL: PTP; MODE: RTMU; OMU1: "+state_omu1+"; OMU2: "+state_omu2+"; HandOver: "+state_ho+";\n"
							print(text_save)
							self.Filename.write(text_save)
					else:
						state_ho= self.HO_OMC.run_senario("ptp")
						text_save="0 - CaLL: PTP; MODE: SiMPLE; HANDOVER: "+state_ho+";\n"
						print(text_save)
						self.Filename.write(text_save)

					connect_phone= False
					with VERROU:
						self.phone.write(b"ATH\r")
						#print("ath")
					time.sleep(2)

			else:
				print("atd"+interfaceFrame.VALUE_ENTRY_PHONE_NUMERO.get()+" ERROR\n")
		else:
			print("Can not open '"+interfaceFrame.VALUE_BOX_COM1.get())


	def data(self, tmu_mode):
		global RING_STATUS
		connect_phone=False
		nb_atd= 5


		if self.phone.isOpen():
			self.phone.readlines()
			with VERROU:
				self.phone.write(b"ATD"+interfaceFrame.VALUE_ENTRY_PHONE_NUMERO.get()+b'\r')
				time.sleep(2)
			while nb_atd > 0:
				time.sleep(10)
				with VERROU:
					reponse= Option.split_chaine(self.phone.readlines(), "")
					time.sleep(2)
				if (reponse.find("OK") != -1):
					RING_STATUS = True
					break
				if (reponse.find("CONNECT") != -1):
					RING_STATUS= False
					connect_phone= True
					break
				else:
					with VERROU:
						self.phone.write(b"ATD"+interfaceFrame.VALUE_ENTRY_PHONE_NUMERO.get()+b'\r')
						time.sleep(2)
				nb_atd-=1
			
			if nb_atd > 0:
				time.sleep(30)
				
				while True: #il faut un tempo le temps d'attente max
					reponse= Option.split_chaine(self.phone.readlines(), "")
					if (reponse.find("CONNECT") != -1) or (connect_phone == True):
						print(reponse)
						connect_phone= True
						break
					if reponse.find("NETWORK OUT OF ORDER") != -1:
						print(reponse)
						connect_phone= False
						break
					#mise a jour du delai d'attente

				if (connect_phone==True) and (Option.RUNNING == True) and (RING_STATUS ==False):
					
					
					if tmu_mode == True:
						nb=1
						while nb <= self.NBRTMU:
							state_omu1 = self.HO_OMU1.reset_tmu()
							state_omu2= self.HO_OMU2.reset_tmu()
							#with VERROU:
							state_ho = self.HO_OMC.run_senario("data")
							print("NB === ", self.NBRTMU)
							text_save=str(nb)+" - CALL: DATA; MODE: RTMU; OMU1: "+state_omu1+"; OMU2: "+state_omu1+"; HandOver: "+state_ho+";\n"
							time.sleep(240)
							nb+=1
							print(text_save)
							self.Filename.write(text_save)
					else:

						state_ho = self.HO_OMC.run_senario("data")
						text_save="0 - CaLL: DATA; MODE: SiMPLE; HANDOVER: "+state_ho+";\n"
						print(text_save)
						self.Filename.write(text_save)

					connect_phone= False
					Option.hang_up_call(self.phone)
				else:
					print("impossible d'etablir un connect")

			else:
				print("atd"+interfaceFrame.VALUE_ENTRY_PHONE_NUMERO.get()+" ERROR\n")
		else:
			print("Can not open '"+interfaceFrame.VALUE_BOX_COM1.get())




	def group_call(self, type_call, tmu_mode):
		global RING_STATUS

		nb_atd= 5
		if self.phone.isOpen():
			str_cmd_call=""
			if type_call == "vgcs":
				str_cmd_call="ATD*17*75#"+interfaceFrame.VALUE_ENTRY_GROUP_ID.get()+";\r"
			elif type_call == "rec":
				str_cmd_call="ATD*17*750#299;\r"
			elif type_call == "vbs":
				str_cmd_call = "ATD*18*75#"+interfaceFrame.VALUE_ENTRY_GROUP_ID.get()+";\r"
			else:
				return None
			self.phone.readlines()
			with VERROU:
				self.phone.write(b""+str_cmd_call)
				time.sleep(2)
				

			while nb_atd > -1:
				time.sleep(3)
				with VERROU:
					reponse= Option.split_chaine(self.phone.readlines(), "")

				if reponse.find("OK") != -1:
					RING_STATUS = True
					break
				else:
					with VERROU:
						self.phone.write(b""+str_cmd_call)
						time.sleep(2)

				nb_atd -=1
			
			if nb_atd > -1:
				time.sleep(10)
				if type_call != "rec":
					suiv= raw_input('Veuillez accepter le groupe call et appuyer sur entrer: ')
				reponse= Option.split_chaine(self.phone.readlines(), "")
				connect_phone= True

				if (RING_STATUS== False) and (Option.RUNNING == True):
					nb=1
					if tmu_mode == True:
						while nb <= self.NBRTMU:
							state_omu1= self.HO_OMU1.reset_tmu()
							state_omu2= self.HO_OMU2.reset_tmu()
							#with VERROU:
							state_ho =self.HO_OMC.run_senario(type_call)
							time.sleep(240)
							nb+=1
							text_save=str(nb)+" - CALL: "+str_cmd_call+"; MODE: RTMU; OMU1: "+state_omu1+"; OMU2: "+state_omu2+"; HandOver: "+state_ho+";\n"
							print(text_save)
							self.Filename.write(text_save)
					else:
						state_ho= self.HO_OMC.run_senario(type_call)
						text_save="0 - CALL: "+str_cmd_call+"; MODE: SiMPLE; HANDOVER: "+state_ho+";\n"
						print(text_save)
						self.Filename.write(text_save)

					connect_phone= False
					with VERROU:
						self.phone.write(b"ATH\r")
					time.sleep(2)
					suiv= raw_input('Veuillez Kill le groupe call et appuyer sur entrer: ')

			else:
				print("atd"+interfaceFrame.VALUE_ENTRY_PHONE_NUMERO.get()+" ERROR\n")
		else:
			print("Can not open '"+interfaceFrame.VALUE_BOX_COM1.get())





	def run(self):
		self.HO_OMC = omc.OMC()

		with VERROU:
			self.HO_OMU1= omu.OMU(interfaceFrame.VALUE_ENTRY_OMU1_IP.get(),\
				interfaceFrame.VALUE_ENTRY_OMU1_USER.get(),\
				interfaceFrame.VALUE_ENTRY_OMU1_PASSWORD.get())

		with VERROU:
			self.HO_OMU2= omu.OMU(interfaceFrame.VALUE_ENTRY_OMU2_IP.get(),\
			 interfaceFrame.VALUE_ENTRY_OMU2_USER.get(),\
			 interfaceFrame.VALUE_ENTRY_OMU2_PASSWORD.get())

		if self.phone.isOpen():
			with VERROU:
				self.phone.write(b"AT+CBST="+interfaceFrame.VALUE_ENTRY_ATCBST.get()+b'\r')
			time.sleep(3)
			with VERROU:
				self.phone.readlines()

		if self.PTP == True:
			if (self.SIMPLE == True) and (Option.RUNNING == True):
				print("ptp_simple_mode")
				self.ptp(False)

			if (self.RTMU == True) and (Option.RUNNING == True):
				self.NBRTMU = int(interfaceFrame.VALUE_ENTRY_NB_RTMU.get())
				print("ptp_tmu_mode")
				self.ptp(True)


		if self.DATA == True:
			if (self.SIMPLE == True) and (Option.RUNNING == True):
				print("data_simple_mode")
				self.data(False)
			if (self.RTMU == True) and (Option.RUNNING == True):
				self.NBRTMU = int(interfaceFrame.VALUE_ENTRY_NB_RTMU.get())
				print("data_tmu_mode")
				self.data(True)

		if self.VGCS == True:
			if (self.SIMPLE == True) and (Option.RUNNING == True):
				print("vgcs_simple_mode")
				self.group_call("vgcs",False)

			if (self.RTMU == True) and (Option.RUNNING == True):
				self.NBRTMU = int(interfaceFrame.VALUE_ENTRY_NB_RTMU.get())
				print("vgcs_tmu_mode")
				self.group_call("vgcs",True)


		if self.REC == True:
			if (self.SIMPLE == True) and (Option.RUNNING == True):
				print("rec_simple_mode")
				self.group_call("rec",False)

			if (self.RTMU == True) and (Option.RUNNING == True):
				self.NBRTMU = int(interfaceFrame.VALUE_ENTRY_NB_RTMU.get())
				print("rtmu_tmu_mode")
				self.group_call("rec",True)


		if self.VBS == True:
			if (self.SIMPLE == True) and (Option.RUNNING == True):
				print("vbs_simple_mode")
				self.group_call("vbs",False)

			if (self.RTMU == True) and (Option.RUNNING == True):
				self.NBRTMU = int(interfaceFrame.VALUE_ENTRY_NB_RTMU.get())
				print("vbs_tmu_mode")
				self.group_call("vbs",True)

		Option.RUNNING= False

		print("Fin de la partie")
		self.Filename.close()