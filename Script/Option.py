# -*-coding:Latin-1 -*

from Tkinter import *
import tkMessageBox
import ttk
import serial
import interfaceFrame
import time
import threading 

global RUNNING
global toplevel 
global signal_limit_waiting
global val_continue
global val_stage
global phone_com1
"""
Cette fonction permet de creer une alerte, pour que l'utisateur confirmer son choix
"""
def callback_quit():
	global RUNNING
	if tkMessageBox.askokcancel("Quitter", "êtes-vous sûr de vouloir quitter?"):
		toplevel.destroy()
		RUNNING= False

"""
Comme son indique progress_Bar est une barre de progression en mode de dure indertiminé. 
Elle s'execute au premier plan et masqué la fenetre principale pour empêcher toute motidification possible
"""
def progress_Bar():
	global RUNNING
	global toplevel
	try:
		RUNNING= True
		toplevel= Toplevel()
		toplevel.progress = ttk.Progressbar(toplevel, orient="horizontal",length=380, mode="indeterminate")
		toplevel.progress.pack()
		thread = threading.Thread()
		thread.__init__(target=toplevel.progress.start(), args=())
		thread.start
		toplevel.grab_set()
		toplevel.focus_set()
		toplevel.focus_force

		"""
		On detecte si l'utisateur clic sur le bouton fermer,
		alors on appelle la fonction callback_quit pour confirmer le choix 
		"""
		toplevel.protocol("WM_DELETE_WINDOW", lambda:callback_quit())
	except Exception as e:
		print("in file Option, progressbar")
		print(e)
		RUNNING = False
	


"""
La fonction permet d'enregistre les donneés dans le fichier de rapport choisi par l'utilisateur 
elle est utilisé dans le cas si l'utilisateur choisi l'option NR_DATA
"""
def save_Data(my_object):
	with open(interfaceFrame.VALUE_FILE_SAVE, "a") as fichier:	
		fichier.write(my_object)
		fichier.closed

"""
elle convertit la liste chaine en string et ajoute caractere a chaque tour de la boucle
"""
def split_chaine(chaine, caractere):
	carac_chaine=["[","]", "\n", "\r"]
	new_chaine=""
	for line in chaine:
		i=0
		while i < len(line):
			if line[i] not in carac_chaine:
				new_chaine=new_chaine+line[i]
			i+=1
		new_chaine+=caractere

	return new_chaine


def limit_waiting():
	global RUNNING
	global signal_limit_waiting
	global val_continue
	global phone_com1
	global val_stage

	signal_limit_waiting= False
	val_stage= 0

	while RUNNING == True:
		if signal_limit_waiting == True:
			stage= val_stage
			val_continue= True
			time.sleep(90)
			if val_continue == True and stage== val_stage:
				hang_up_call(phone_com1)



"""
hang_up_call est la fonction qui permet de racrocher un appel DATA
"""
def hang_up_call(phone):
	#phone.write("\r")
	time.sleep(1)
	phone.write(b"+")
	phone.write(b"+")
	phone.write(b"+")
	time.sleep(2)
	phone.write("\r")
	time.sleep(2)
	phone.write(b"ath\r")
	time.sleep(3)
	print("++ath")
	phone.readlines()
