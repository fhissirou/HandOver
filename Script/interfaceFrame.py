# -*-coding:Latin-1 -*
"""
File InterfaceFrame.py
"""
import os
import sys
from Tkinter import *
import Tkconstants, tkFileDialog
import inspect
import ttk
import serial
from threading import Thread
import time

import handOver

global VALUE_BOX_COM1
global VALUE_BOX_COM2
global VALUE_SELECT_CALL_OPTION
global VALUE_SELECT_CALL_CONFIG
global VALUE_ENTRY_PHONE_NUMERO
global VALUE_ENTRY_ATCBST
global VALUE_ENTRY_GROUP_ID

global VALUE_ENTRY_OMC_IP
global VALUE_ENTRY_OMC_PASSWORD
global VALUE_ENTRY_OMC_USER

global VALUE_ENTRY_OMU1_IP
global VALUE_ENTRY_OMU1_PASSWORD
global VALUE_ENTRY_OMU1_USER

global VALUE_ENTRY_OMU2_IP
global VALUE_ENTRY_OMU2_PASSWORD
global VALUE_ENTRY_OMU2_USER

global VALUE_ENTRY_NB_RTMU

global val_line
global begin_time


begin_time= time.time()

val_line=0
VALUE_FILE_CONF=""
VALUE_FILE_CMD=""
VALUE_FILE_SAVE=""
VALUE_FILE_AUDIO=""


# cette frame controle tout les autres frames
# c'est elle qui initilisation les different type d'execution du programme
# avec la radiobutton chaque selection correspond une porgramme que l'utlisateur peut exécuter

def Frame_init_option(self, otherFrame2 ,otherFrame3):
	global VALUE_SELECT_CALL_OPTION
	global VALUE_SELECT_CALL_CONFIG
	VALUE_SELECT_CALL_OPTION={}
	VALUE_SELECT_CALL_CONFIG={}

	labelFrame= LabelFrame(self, text="CONFIG HandOver",borderwidth=10, relief=GROOVE)
	labelFrame.pack(side=TOP, padx=10, pady=5)

	labelFrame1= LabelFrame(labelFrame, text="HandOver Type",borderwidth=5, relief=GROOVE)
	labelFrame1.grid(column=0,row=0,padx=14, pady=2)

	labelFrame2= LabelFrame(labelFrame, text="Type of call",borderwidth=5, relief=GROOVE)
	labelFrame2.grid(column=1,row=0,padx=14, pady=2)

	call_config=["SIMPLE","RESET-TMU"]
	call_modes=["PTP","DATA","VGCS","REC","VBS"]

	j= 0

	for text in call_config:
		var_call_config = IntVar()
		var_call_config.set(1)
		VALUE_SELECT_CALL_CONFIG[text]= var_call_config
		bouton= ttk.Checkbutton(labelFrame1, text=text, variable=VALUE_SELECT_CALL_CONFIG[text])
		bouton.state(['!disabled','selected'])
		bouton.grid(row=j, padx= 35,sticky=W)
		j+=1
	j= 0
	for text in call_modes:
		var_select = IntVar()
		var_select.set(1)

		VALUE_SELECT_CALL_OPTION[text]= var_select
		bouton= ttk.Checkbutton(labelFrame2, text=text, variable=VALUE_SELECT_CALL_OPTION[text])
		bouton.state(['!disabled','selected'])
		bouton.grid(row=j, padx= 35,sticky=W)
		j+=1
"""
c'est la deuxieme frame de la frame principale,
elle change en fonction des differentss selection de l'utilisateur depuis de la frame_init_option
a chaque selection elle intialise le champs option necessaire pour l'excution du programme 

"""
# c'est la partie qui correspond au champ de selection des com des téléphone mobile
# elle permet également de saisir des information comme le numéro du mobile qui réçois l'appel ou le champ qui correpond au groupe ID
def Frame_select_com(self, val_type):
	global VALUE_BOX_COM1 
	global VALUE_BOX_COM2
	global VALUE_ENTRY_PHONE_NUMERO
	global VALUE_ENTRY_ATCBST
	global VALUE_ENTRY_GROUP_ID

	global VALUE_ENTRY_OMC_IP
	global VALUE_ENTRY_OMC_PASSWORD
	global VALUE_ENTRY_OMC_USER

	global VALUE_ENTRY_OMU1_IP
	global VALUE_ENTRY_OMU1_PASSWORD
	global VALUE_ENTRY_OMU1_USER

	global VALUE_ENTRY_OMU2_IP
	global VALUE_ENTRY_OMU2_PASSWORD
	global VALUE_ENTRY_OMU2_USER
	global VALUE_ENTRY_NB_RTMU
    # On initialise les variagle blogal
	VALUE_BOX_COM1= StringVar()
	VALUE_BOX_COM2= StringVar()

	VALUE_ENTRY_PHONE_NUMERO= StringVar()
	VALUE_ENTRY_ATCBST= StringVar()
	VALUE_ENTRY_GROUP_ID= StringVar()
	VALUE_ENTRY_NB_RTMU= StringVar()

	VALUE_ENTRY_OMC_IP= StringVar()
	VALUE_ENTRY_OMC_PASSWORD= StringVar()
	VALUE_ENTRY_OMC_USER= StringVar()


	VALUE_ENTRY_OMU1_IP= StringVar()
	VALUE_ENTRY_OMU1_PASSWORD= StringVar()
	VALUE_ENTRY_OMU1_USER= StringVar()

	VALUE_ENTRY_OMU2_IP= StringVar()
	VALUE_ENTRY_OMU2_PASSWORD= StringVar()
	VALUE_ENTRY_OMU2_USER= StringVar()
	# Je definie mes label des diffrent catégorie de qui sont:
    # Le choix des com mobiles pour selection les mobiles
    # La deuxième partie correspond au configuration de l'OMC
    # La dernire est ce lui de OMC (en tout on a deux OMC au total)
	labelFrame1= LabelFrame(self, text="Choisir un port COM",borderwidth=10, relief=GROOVE)
	labelFrame1.pack(padx=10, pady=5)


	labelFrame2= LabelFrame(self, text="Config OMC",borderwidth=10, relief=GROOVE)
	labelFrame2.pack(padx=10,pady=5)


	labelFrame3= LabelFrame(self, text="Config BSC1",borderwidth=10, relief=GROOVE)
	labelFrame3.pack(padx=10,pady=5)

	labelFrame4= LabelFrame(self, text="Config BSC2",borderwidth=10, relief=GROOVE)
	labelFrame4.pack(padx=10,pady=5)

    # j'inialise les paramètre de façon automatique
    # ce qui permet à l'utilisatueur d'aller beaucoup plus vite
    # néamoins l'utilisateur à toujours la possibilité de changer les paramètre s'il le souhaite 
	text_1= "COM mobile phone:"
	text_2= "COM Dispather:"
	text_3= "Num Dispatcher:"
	text_4= "Cmd AT+CBST:"
	text_5= "Goupe ID:"
	text_6=	"NB Reset TMU:"

	text_omc_ip= "Hostname"
	text_omc_user= "Username"
	text_omc_password= "Password"

	text_omu_ip= "Hostname"
	text_omu_user= "Username"
	text_omu_password= "Password"



#------------------------------------------------------------
    # je définie mes Les label 
    # ce sont des noms qui designent quel champ correspond à quelles informations
	label_1= Label(labelFrame1,width=20, text=text_1)
	label_2= Label(labelFrame1,width=20, text=text_2)
	label_3= Label(labelFrame1,width=20, text=text_3)
	label_4= Label(labelFrame1,borderwidth=5, width=21, text=text_4)
	label_5= Label(labelFrame1,borderwidth=5, width=21, text=text_5)
	label_6= Label(labelFrame1,borderwidth=5, width=21, text=text_6)

	label_omc_ip= Label(labelFrame2,width=10, text=text_omc_ip)
	label_omu1_ip= Label(labelFrame3,width=10, text=text_omu_ip)
	label_omu2_ip= Label(labelFrame4,width=10, text=text_omu_ip)

	label_omc_user= Label(labelFrame2,width=10, text=text_omc_user)
	label_omu1_user= Label(labelFrame3,width=10, text=text_omu_user)
	label_omu2_user= Label(labelFrame4,width=10, text=text_omu_user)

	label_omc_password= Label(labelFrame2,width=10, text=text_omc_password)
	label_omu1_password= Label(labelFrame3,width=10, text=text_omu_password)
	label_omu2_password= Label(labelFrame4,width=10, text=text_omu_password)




#------------------------------------------------------------------------------------------------
    # je definie les champs entry pour saisir les information
    # Le champ de type Combotox propose à l'utilisateur la liste des com disponible sur le PC

	box_com1= ttk.Combobox(labelFrame1, width=25, textvariable=VALUE_BOX_COM1, state= 'readonly')
	box_com2= ttk.Combobox(labelFrame1, width=25, textvariable=VALUE_BOX_COM2, state='readonly')

	entry_id= Entry(labelFrame1,borderwidth=5, textvariable=VALUE_ENTRY_GROUP_ID, width=28)
	entry_num= Entry(labelFrame1,borderwidth=5,textvariable=VALUE_ENTRY_PHONE_NUMERO, width=28)
	entry_atcbst= Entry(labelFrame1,borderwidth=5, textvariable=VALUE_ENTRY_ATCBST, width=28)
	entry_nb_rtmu= Entry(labelFrame1,borderwidth=5, textvariable=VALUE_ENTRY_NB_RTMU, width=28)

	omc_ip= Entry(labelFrame2, borderwidth=5, textvariable=VALUE_ENTRY_OMC_IP ,width=18)
	omc_user= Entry(labelFrame2, borderwidth=5,textvariable=VALUE_ENTRY_OMC_USER, width=16)
	omc_password= Entry(labelFrame2, borderwidth=5, textvariable=VALUE_ENTRY_OMC_PASSWORD, width=16)

	omu1_ip= Entry(labelFrame3, borderwidth=5, textvariable=VALUE_ENTRY_OMU1_IP ,width=18)
	omu1_user= Entry(labelFrame3,borderwidth=5, textvariable=VALUE_ENTRY_OMU1_USER, width=16)
	omu1_password= Entry(labelFrame3, borderwidth=5, textvariable=VALUE_ENTRY_OMU1_PASSWORD, width=16)

	omu2_ip= Entry(labelFrame4, borderwidth=5, textvariable=VALUE_ENTRY_OMU2_IP ,width=18)
	omu2_user= Entry(labelFrame4,borderwidth=5, textvariable=VALUE_ENTRY_OMU2_USER, width=16)
	omu2_password= Entry(labelFrame4, borderwidth=5, textvariable=VALUE_ENTRY_OMU2_PASSWORD, width=16)



#-------------------------------------------------------------------------------------
    # la fonction scan_com permet de sauvergarder la liste des com disponible
	box_com1['values']= Scan_com()
	box_com1.current(0)

	box_com2['values']= Scan_com()
	box_com2.current(0)

	VALUE_ENTRY_PHONE_NUMERO.set("555558000265")
	VALUE_ENTRY_ATCBST.set("70,0,0")
	VALUE_ENTRY_GROUP_ID.set("200")
	VALUE_ENTRY_NB_RTMU.set("2")

	VALUE_ENTRY_OMC_IP.set("172.21.155.71")
	VALUE_ENTRY_OMC_USER.set("omc")
	VALUE_ENTRY_OMC_PASSWORD.set("nortel")

	VALUE_ENTRY_OMU1_IP.set("47.164.27.128")
	VALUE_ENTRY_OMU1_USER.set("omu")
	VALUE_ENTRY_OMU1_PASSWORD.set("omu")

	VALUE_ENTRY_OMU2_IP.set("47.164.27.144")
	VALUE_ENTRY_OMU2_USER.set("omu")
	VALUE_ENTRY_OMU2_PASSWORD.set("omu")

#---------------------------------------------------------------------------------------------
    # je position chanque champs dans un grille pour avoir une interface jolie
	label_1.grid(column=0, row=0, sticky=E)
	label_2.grid(column=0, row=1, sticky=E)
	label_3.grid(column=0, row=2, sticky=E)
	label_4.grid(column=0, row=3, sticky=E)
	label_5.grid(column=0, row=4, sticky=E)
	label_6.grid(column=0, row=5, sticky=E)



#---------------------------------------------------------------
	box_com1.grid(column=1, row=0, padx=10, pady=10, sticky=W)
	box_com2.grid(column=1, row=1, padx=10, pady=10, sticky=W)
	entry_num.grid(column=1, row=2, padx=10, pady=10, sticky=W)
	entry_atcbst.grid(column=1, row=3, padx=10, pady=10, sticky=W)
	entry_id.grid(column=1, row=4, padx=10, pady=10, sticky=W)
	entry_nb_rtmu.grid(column=1, row=5, padx=10, pady=10, sticky=W)

#------------------------------------------------------------

	label_omc_ip.grid(column=0, row=0, sticky=N)
	label_omu1_ip.grid(column=0, row=0, sticky=N)
	label_omu2_ip.grid(column=0, row=0, sticky=N)

	label_omc_user.grid(column=1, row=0, sticky=N)
	label_omu1_user.grid(column=1, row=0, sticky=N)
	label_omu2_user.grid(column=1, row=0, sticky=N)

	label_omc_password.grid(column=2, row=0, sticky=N)
	label_omu1_password.grid(column=2, row=0, sticky=N)
	label_omu2_password.grid(column=2, row=0, sticky=N)

	omc_ip.grid(column=0, row=1,padx=5, sticky=W)
	omu1_ip.grid(column=0, row=1,padx=5, sticky=W)
	omu2_ip.grid(column=0, row=1,padx=5, sticky=W)

	omc_user.grid(column=1, row=1,padx=5, sticky=W)
	omu1_user.grid(column=1, row=1,padx=5, sticky=W)
	omu2_user.grid(column=1, row=1,padx=5, sticky=W)

	omc_password.grid(column=2, row=1,padx=5, sticky=W)
	omu1_password.grid(column=2, row=1,padx=5, sticky=W)
	omu2_password.grid(column=2, row=1,padx=5, sticky=W)




"""
ce bouton permet de lancer l'execution du programme 
"""
def Frame_btn_execution(self):
	self= Frame(self)
	self.pack(side=TOP, padx=5, pady=5)
	bouton_exec= Button(self,width=10, text="Exécute", command=lambda:verif_args())
	bouton_exec.grid(column=3, row=0,)


# elle scan la liste des comme disponible sur la machine
# neamoins cette fonction ne vous permet de savoir quelle COM correspond à quel mobile
# donc vous devez quand même savoir par d'autres les COM de vos mobiles
def Scan_com():
	available=[]
	try:
		for i in range(256):
			try:
				ser = serial.Serial(i)
				available.append(str(ser.portstr))
				ser.close
			except serial.SerialException:
				pass
		return available
	except Exception as e:
		print("In file Interface; ligne 247")
		print(e)

# cette Fonction verifie que tous les arguments
# elle verifie que tous les information nécessaire sont siasie 
# cela permet d'eviter des bugs ou errors
def verif_args():
	global VALUE_BOX_COM1 
	global VALUE_BOX_COM2
	
	global VALUE_SELECT_CALL_OPTION
	global VALUE_SELECT_CALL_CONFIG
	
	global VALUE_ENTRY_PHONE_NUMERO
	global VALUE_ENTRY_ATCBST

	global VALUE_ENTRY_OMC_IP
	global VALUE_ENTRY_OMC_PASSWORD
	global VALUE_ENTRY_OMC_USER

	global VALUE_ENTRY_OMU1_IP
	global VALUE_ENTRY_OMU1_PASSWORD
	global VALUE_ENTRY_OMU1_USER

	global VALUE_ENTRY_OMU2_IP
	global VALUE_ENTRY_OMU2_PASSWORD
	global VALUE_ENTRY_OMU2_USER

	msg_error= 1

	tmu_mode= False
	simple_mode= False
	ptp_mode= False
	data_mode= False
	vgcs_mode= False
	rec_mode= False
	vbs_mode= False

    # On veirifie que les entrés sont bien présent
    # On verifie l'existance des tous les chanmps obligatoire
    # ensuite on essaye de savoir les options utilisé par l'utilisateur
	if (len(VALUE_ENTRY_OMC_IP.get()) > 0) and (len(VALUE_ENTRY_OMC_USER.get()) > 0) and (len(VALUE_ENTRY_OMC_PASSWORD.get()) > 0) and\
	(len(VALUE_ENTRY_OMU1_IP.get()) > 0) and (len(VALUE_ENTRY_OMU1_USER.get()) > 0) and (len(VALUE_ENTRY_OMU1_PASSWORD.get()) > 0) and \
	(len(VALUE_ENTRY_OMU2_IP.get()) > 0) and (len(VALUE_ENTRY_OMU2_USER.get()) > 0) and (len(VALUE_ENTRY_OMU2_PASSWORD.get()) > 0) and \
	(len(VALUE_BOX_COM1.get()) > 0) and (VALUE_BOX_COM1.get()  != VALUE_BOX_COM2.get()) and (len(VALUE_ENTRY_PHONE_NUMERO.get()) > 0) and \
	(len(VALUE_ENTRY_GROUP_ID.get()) > 0) and (len(VALUE_ENTRY_ATCBST.get()) > 0) and (len(VALUE_ENTRY_NB_RTMU.get()) > 0):
		
        # lacette Boucle permet de savoir la configuration choisi par l'utilisateur
        # On  deux type de configuration SIMPLe pour un handOver simple ou RESET-TMU pour reseter le TMU
		for cle in VALUE_SELECT_CALL_CONFIG:
			if VALUE_SELECT_CALL_CONFIG[cle].get() == 1:
				if cle == "SIMPLE":
					simple_mode= True
					set_config= True
				elif cle == "RESET-TMU":
					tmu_mode= True
					set_config= True
				else:
					set_config= False
					print("Veuillez remplir tous les champs")

        # Ici chercher à savoir les types d'appel choisi par l'utilisateur
        # ce types peut PTP pour l'appel voix
        # DATA pour appel data
        # VGCS VBS et REC font parties de la famille de groupe call ensuite on fait appel a la classe handOver pour en lui donnant les paramètre
		for cle in VALUE_SELECT_CALL_OPTION:
			if VALUE_SELECT_CALL_OPTION[cle].get() == 1:
				if cle == "PTP":
					ptp_mode= True
					set_call_option= True
				elif cle == "DATA":
					data_mode = True
					set_call_option= True
				elif cle == "VGCS":
					vgcs_mode= True
					set_call_option= True
				elif cle == "REC":
					rec_mode= True
					set_call_option= True
				elif cle == "VBS":
					vbs_mode= True
					set_call_option= True
				else:
					set_call_option= False
					print("Veuillez remplir tous les champs")
		
		if (set_call_option== False) or (set_config== False):
			print("Veuillez remplir tous les champs")
		else:
            # On fait appel de la classe begin_handOver une fois que l'utilisateur clic sur le bouton d'exécuter
			handOver.begin_handOver(simple_mode, tmu_mode, ptp_mode, data_mode, vgcs_mode, rec_mode, vbs_mode)
	else:
		print("Veuillez remplir tous les champs")



# Cette fonction de supprimer des caractère speciaux lorqu'on fait un read du mobile
# Cela permet de mieux veirifier que les information retourner par le mobile
# Ca aide le programme à mieux prendre les decision 

def split_chaine(chaine, caractere):
	carac_chaine=["[","]", "\n", "\r"]
	new_chaine=""
	try:
		for line in chaine:
			i=0
			while i < len(line):
				if line[i] not in carac_chaine:
					new_chaine=new_chaine+line[i]
				i+=1
			"""
			adding character tosepare the elements of the character string
			"""
			new_chaine+=caractere

		return new_chaine
	except Exception as e:
		print("In file Interface; ligne 346")
		print(e)
		return None 
