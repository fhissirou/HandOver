# -*-coding:Latin-1 -*

from ftplib import FTP 
from fabric.api import *
import os
import sys
import interfaceFrame
import time
# La classe OMc permet d'éxécuter des commands dans sur l'OMC
# elle recupère les identfiant de l'utilisateur pour se connecter à l'omc
# son but c'est de faire de handOver et récuperer la liste des calls busy
# Il a besoin de 4 fichiers de commands différents sauvegardé dans le répertoire fhissirou
# Chaune de ces fichiers contients une liste de commande qui permet à l'omc de retourner les infos souhaités
class OMC():

	def __init__(self):
        #On récupère les identifiant que l'utilisateur à saisi depuis l'interface graphique
		env.host_string=interfaceFrame.VALUE_ENTRY_OMC_IP.get()
		env.user=interfaceFrame.VALUE_ENTRY_OMC_USER.get()
		env.password=interfaceFrame.VALUE_ENTRY_OMC_PASSWORD.get()

    #Cette fonction permet d'executer plusieurs fichier sur l'omc
    #elle fait un handOver et verifie que le nombre de call processus busy (cela permet de savoir que le handOver est fait avec succès)
	def run_senario(self, type_call):
        #liste des fichiers trouvant sur l'OMC
		str_force_ho_bsc1= "/usr/local/oam/bin/ds_executeCmdFile.sh -F/OMC/data/cmdFile/root/users/fhissirou/Force_HO_BSC17 -Uoam -Pbssds1995"
		str_force_ho_bsc2= "/usr/local/oam/bin/ds_executeCmdFile.sh -F/OMC/data/cmdFile/root/users/fhissirou/Force_HO_BSC140 -Uoam -Pbssds1995"
		str_call_busy_bsc1= "/usr/local/oam/bin/ds_executeCmdFile.sh -F/OMC/data/cmdFile/root/users/fhissirou/Display_CHANNEL_BSC17 -Uoam -Pbssds1995"
		str_call_busy_bsc2="/usr/local/oam/bin/ds_executeCmdFile.sh -F/OMC/data/cmdFile/root/users/fhissirou/Display_CHANNEL_BSC140 -Uoam -Pbssds1995"
		
        # je vais un cd pour me placer dans le repertoire fhissirou qui se trouve sur l'OMC
		with cd('/OMC/data/cmdFile/root/users/fhissirou/'):
            #je récupère le nombre de call processus busy, normalement tous chacun des mobiles devrait se trouver sur BSC différent
			nbbusy_bsc1_1= self.verif_call_busy(run(str_call_busy_bsc1,shell=False, pty=False))
			nbbusy_bsc2_1= self.verif_call_busy( run(str_call_busy_bsc2,shell=False, pty=False))

            #je fais un force handOver sur le premier BSC 17
            #donc tous les mobiles devront basculer sur le BSC 140
			run(str_force_ho_bsc1,shell=False, pty=False)

            #Je recupère le nombre call bussy sur le 
			nbbusy_bsc1_2= self.verif_call_busy(run(str_call_busy_bsc1,shell=False, pty=False))
			nbbusy_bsc2_2= self.verif_call_busy(run(str_call_busy_bsc2,shell=False, pty=False))
			#je fais un force handOver sur le BSC140
            #donc les mobiles du BSC17 devront retourner dans leur possition initiale 
            run(str_force_ho_bsc2,shell=False, pty=False)
			#je verifie à nouveau le nombre de call bussy
			nbbusy_bsc1_3= self.verif_call_busy(run(str_call_busy_bsc1,shell=False, pty=False))
			nbbusy_bsc2_3= self.verif_call_busy(run(str_call_busy_bsc2,shell=False, pty=False))
			
            # je commpare le nombre de bussy avant, pendant et après le handOver 
            #cela permet de savoir si le HandOver a été success ou error
			if (nbbusy_bsc1_2 != nbbusy_bsc1_1) or (nbbusy_bsc1_2 != nbbusy_bsc1_3):
				if (nbbusy_bsc2_2 != nbbusy_bsc2_1) or (nbbusy_bsc2_2 != nbbusy_bsc2_3):
					return "OK"
				else:
					return "ERROR"
			elif (type_call == "vgcs") or (type_call == "rec"):
				return "OK"

		return "ERROR"


    #Cette fonction retourne le nombre de call bussy sur le BSC en se bassant le mot bussy, TCH et le timeslot
	def verif_call_busy(self, chaine):
		compt= 0
		for line in chaine.split('\n'):
			if (line.find('busy') != -1) and (line.find('TCH') != -1) and (line.find('timeslot') != -1):
				compt+=1
		return compt