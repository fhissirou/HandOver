#!/usr/bin/env python
# Tkinter (Tk/Ttk) Progressbar widget example





import Tkinter as tk
import ttk
import datetime
import calendar
import math 

#Cette classe permet de creer une barre de progression
# une fois que l'utilisateur clic sur le bouton la barre de progression se lance automatique
# elle a pour intérer d'enpêcher l'utilisateur à modifier le contenu des champs pendant l'exécution du programme
class SampleApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.button = ttk.Button(text="start", command=self.start)
		self.button.pack()
		self.progress = ttk.Progressbar(self, orient="horizontal",length=200, mode="determinate")
		self.progress.pack()

		self.bytes = 0
		self.maxbytes = 0
		date_text = "2016-07-11 15:26"
		date = datetime.datetime.strptime(date_text, "%Y-%m-%d %H:%M")
		print(date)
		self.begin_time =calendar.timegm(datetime.datetime.now().utctimetuple())
		self.end_time= int(calendar.timegm(date.utctimetuple()) - self.begin_time)
		self.last_time=self.begin_time

		print(self.end_time)
		self.pas=0


    # On lance la barre de progression en definissant la taille et la vitesse de progression
	def start(self):
		self.progress["value"] = 0
		self.maxbytes = self.end_time
		self.progress["maximum"] = self.end_time
		self.read_bytes()

	def read_bytes(self):

		self.diff_time= calendar.timegm(datetime.datetime.now().utctimetuple())
		self.bytes += int(self.diff_time - self.last_time)
		self.last_time= self.diff_time
		self.progress["value"] = self.bytes

		self.pas= int(self.diff_time - self.begin_time)
		print(self.pas)
		pourcentage= round((self.pas*100) / self.end_time)
		print(str(pourcentage));

		
		if self.bytes < self.maxbytes:
			self.after(100, self.read_bytes)


app = SampleApp()
app.mainloop()