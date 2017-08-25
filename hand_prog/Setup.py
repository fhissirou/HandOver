# -*-coding:Latin-1 -*
"""
File interface.py
"""
import os
import sys
from Tkinter import *
import Tkconstants, tkFileDialog
import inspect
import ttk
import serial
from Script import interfaceFrame
import threading 

"""
le frame principale qui englobe l'ensemble du programme
"""
class MainInterface(Frame):
	def __init__(self, parent, **kwargs):

		self.root = parent
		self.root.title("Main frame")
		self.root.geometry=("320x240")
		Frame.__init__(self, parent, width=320, height=240, **kwargs)
		self.pack(fill=BOTH)

		self.select= IntVar()
		self.Init_all_frame()
		#self.poll()
		thread = threading.Thread(target=self.poll)
		thread.daemon= True
		thread.start()
	
	def Init_all_frame(self):
		self.Frame1= Frame(self, width = self.winfo_width())
		self.Frame1.grid(column=0,row=0)
		#self.Frame1.pack(side=TOP, padx=5, pady=5)

		self.Frame2= Frame(self, width = self.winfo_width())
		#self.Frame2.pack(side=TOP, padx=5, pady=5)
		self.Frame2.grid(column=0,row=1)
		
		self.Frame3= Frame(self, width = self.winfo_width())
		#self.Frame3.pack(side=TOP, padx=5, pady=5)
		self.Frame3.grid(column=0,row=2)
		
		self.Frame4= Frame(self, width = self.winfo_width())
		#self.Frame4.pack(side=TOP, padx=5, pady=5)
		self.Frame4.grid(column=0,row=3)
		#self.Frame5= Frame(self)
		#self.Frame5.pack(side=TOP, padx=5, pady=5)

		interfaceFrame.Frame_init_option(self.Frame1, self.Frame2, self.Frame3)
		interfaceFrame.Frame_select_com(self.Frame2, "PTP")
		#interfaceFrame.Frame_select_file(self.Frame3, 1)
		interfaceFrame.Frame_btn_execution(self.Frame4)

		#interfaceFrame.Frame_resultat(self.Frame5)

	def poll(self):
		self.root.after(100,self.poll)


fenetre = Tk()
fenetre.resizable(width= False, height= False)
interface = MainInterface(fenetre)

try:
	interface.mainloop()
except Exception as e:
	print("Error ", e)
	sys.exit(1)
