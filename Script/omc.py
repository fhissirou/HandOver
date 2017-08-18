# -*-coding:Latin-1 -*

from ftplib import FTP 
from fabric.api import *
import os
import sys
import interfaceFrame
import time
class OMC():

	def __init__(self):
		env.host_string=interfaceFrame.VALUE_ENTRY_OMC_IP.get()
		env.user=interfaceFrame.VALUE_ENTRY_OMC_USER.get()
		env.password=interfaceFrame.VALUE_ENTRY_OMC_PASSWORD.get()

	def run_senario(self, type_call):
		str_force_ho_bsc1= "/usr/local/oam/bin/ds_executeCmdFile.sh -F/OMC/data/cmdFile/root/users/fhissirou/Force_HO_BSC17 -Uoam -Pbssds1995"
		str_force_ho_bsc2= "/usr/local/oam/bin/ds_executeCmdFile.sh -F/OMC/data/cmdFile/root/users/fhissirou/Force_HO_BSC140 -Uoam -Pbssds1995"
		str_call_busy_bsc1= "/usr/local/oam/bin/ds_executeCmdFile.sh -F/OMC/data/cmdFile/root/users/fhissirou/Display_CHANNEL_BSC17 -Uoam -Pbssds1995"
		str_call_busy_bsc2="/usr/local/oam/bin/ds_executeCmdFile.sh -F/OMC/data/cmdFile/root/users/fhissirou/Display_CHANNEL_BSC140 -Uoam -Pbssds1995"
		
		with cd('/OMC/data/cmdFile/root/users/fhissirou/'):
			nbbusy_bsc1_1= self.verif_call_busy(run(str_call_busy_bsc1,shell=False, pty=False))
			nbbusy_bsc2_1= self.verif_call_busy( run(str_call_busy_bsc2,shell=False, pty=False))

			run(str_force_ho_bsc1,shell=False, pty=False)
			nbbusy_bsc1_2= self.verif_call_busy(run(str_call_busy_bsc1,shell=False, pty=False))

			nbbusy_bsc2_2= self.verif_call_busy(run(str_call_busy_bsc2,shell=False, pty=False))
			run(str_force_ho_bsc2,shell=False, pty=False)
			
			nbbusy_bsc1_3= self.verif_call_busy(run(str_call_busy_bsc1,shell=False, pty=False))
			nbbusy_bsc2_3= self.verif_call_busy(run(str_call_busy_bsc2,shell=False, pty=False))
			
			
			if (nbbusy_bsc1_2 != nbbusy_bsc1_1) or (nbbusy_bsc1_2 != nbbusy_bsc1_3):
				if (nbbusy_bsc2_2 != nbbusy_bsc2_1) or (nbbusy_bsc2_2 != nbbusy_bsc2_3):
					return "OK"
				else:
					return "ERROR"
			elif (type_call == "vgcs") or (type_call == "rec"):
				return "OK"

		return "ERROR"


	def verif_call_busy(self, chaine):
		compt= 0
		for line in chaine.split('\n'):
			if (line.find('busy') != -1) and (line.find('TCH') != -1) and (line.find('timeslot') != -1):
				compt+=1
		return compt