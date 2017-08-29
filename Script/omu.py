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


# Cette classe permet de se connect à l'OMU pour réseter le TMU de façon aléatoire.
# Elle a deux fonction reset_tmu qui reset les TMU et get_list_tmu qui retourne la liste des TMU présent dans OMU
# Pour cela il prend comme paramètre:
# host: C'est l'adresse ip du OMC
# User: c'est le nom d'utilisateur de L'OMC
# Password: C'est le password de l'utilisateur

class OMU():

	def __init__(self, host, user,password):
		self.HOST=host
		
		self.USER=user
		self.PASSWORD=password 
		self.TELNET= telnetlib.Telnet(self.HOST)
		self.TELNET.read_until("login: ")
        #On recupère le champ correspondant au nom Utilisateur
		self.TELNET.write(self.USER+"\r\n")

		if self.PASSWORD:
            #On verifie que l'OMC est à attend le saisi du mot de passe
			self.TELNET.read_until("Password: ")
            #On envoi le mot passe à l'OMC
			self.TELNET.write(self.PASSWORD+"\n")



		#self.reset_tmu()
	#Cette fonction reset TMU passé en argument
	def reset_tmu(self, tmu):
		self.TMU_reset= False
        #OMU reconnait les identifiant du TMU par tmu0_sbc alors j'ajoute "_sbc" au
		print("\n\nchoice==> "),
		tmu_sbc=tmu+"_sbc"
		print(tmu)
        #j'envoie la command pour sélectionner le tmu
		self.TELNET.write("telci "+tmu_sbc+"\n")
        #j'attend 5s pour que l'OMC est le temps nécessaire pour éxécuter la command précedente
		time.sleep(5)
        #J'envoie la commande pour reseter le TMU
		self.TELNET.write("bexc freeze\n")
		time.sleep(5)
        #J'autorise l'OMU à fermer son interface tmu
		self.TELNET.write("Q\n")
		time.sleep(5)
		self.TELNET.write('exit\n')
		time.sleep(5)
        #Je mets cette varaible à true qui indique toutes les étapes se sont bien dérouler
		self.TMU_reset= True
		return tmu

    #Cette fonction récupère la liste des tmu actif dans l'OMC
	def get_list_tmu(self):
		patterns= r"tmu_[\w\.-]+[0-9]"

        #J'envoi la command pour récuperer qui affiche les infos concernant le tmu
		self.TELNET.write("ftViCpTable\n")
		time.sleep(5)
        #Je lis la sortie de la command précedente 
		txt= self.TELNET.read_very_eager()
		print("\n"*4)
		print(txt)
        #filter le contenu de la variable text à l'aide patterns qui me retourne la liste des liste de tmu
		self.List_tmu= re.findall(patterns, txt)
        #je mélange la liste de façon aléatoire
		random.shuffle(self.List_tmu, random.random)
		print(self.List_tmu)
        #je retourne la liste
		return self.List_tmu


