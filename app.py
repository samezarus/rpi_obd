# -*- coding: utf8 -*-

from tkinter import *
from tkinter.font import Font

import os

import math

import time

import threading

import obd

#######################################################################################################

width, height = 500, 500         # frame canvas dimensions
len1, len2    = 0.85, 0.3        # needle dimensions, relative to meter ray
ray           = int(0.9*width/2) # meter circle
x0, y0        = width/2, width/2 # position of circle center inside canvas
    
form1 = Tk()
form1.attributes("-fullscreen", True)
form1.configure(bg="black")

frame_font = Font(family="Arial", size=40, weight='bold')

txt = StringVar()

#######################################################################################################
		
def Button1Click(event):
	# Закрываем программу
    event.destroy()		

def Button2Click():
	# Сбрасываем ошибки
	import obd
	connection = obd.OBD(portstr="/dev/ttyUSB0", baudrate=38400, fast=False)
	cmd        = obd.commands.CLEAR_DTC
	response   = connection.query(cmd)
	#globals()[speed.set("111")]	

def Test():
	# Тестовый поток
	#global speed
	while True:
		for i in range(0, 180):
			speed.draw_needle (i)
			#txt.set(i)
			time.sleep(0.03)
		
		for i in range(0, 7000):
			rpm.draw_needle (i)
			#txt.set(i)
			time.sleep(0.001)	
	
def GetInf():
	# Поток внутри которого идёт опрос датчиков
	while True:
		#connection = obd.OBD(portstr="/dev/ttyUSB0", baudrate=38400, fast=True) 
		
		cmd        = obd.commands.SPEED # select an OBD command (sensor)
		response   = connection.query(cmd) # send the command, and parse the response
		#txt.set(response.value.magnitude)
		speed.draw_needle(response.value.magnitude)
	
		cmd        = obd.commands.RPM # select an OBD command (sensor)
		response   = connection.query(cmd) # send the command, and parse the response
		#txt.set(response.value.magnitude)
		rpm.draw_needle(response.value.magnitude)

class Speed(Canvas):
	digitals_color = "#FFFFFF"    # Цвет цифр
	arrow_color    = "#ff0000"    # Цвет стрелки
	alert1_color   = "#339966"    # Цвет круга предупреждения (нормально)
	alert2_color   = "#ffcc00"    # Цвет круга предупреждения (допустимо)
	alert3_color   = "#ff3300"    # Цвет круга предупреждения (критично)
	ring_color     = alert1_color # Цвет кольца спидометра (начальный цвет)
	meter_color    = "#000000"    # Цвет циферблата

	def draw(self, vmin, vmax, step):
		self.vmin = vmin
		self.vmax = vmax
		self.step = step
		x0        = width/2
		y0        = width/2
		ray       = int(0.85*width/2)
		
		self.metr = self.create_oval(x0-ray*1.1, y0-ray*1.1, x0+ray*1.1, y0+ray*1.1, fill=self.meter_color, outline=self.ring_color, width=30) # Параметры спидометра
		coef = 0.1
		self.create_oval(x0-ray*coef, y0-ray*coef, x0+ray*coef, y0+ray*coef, fill="#2C2C25")
		for i in range(1+int((vmax-vmin)/step)):
			v     = vmin + step*i
			angle = (5+6*((v-vmin)/(vmax-vmin)))*math.pi/4
			self.create_line(x0+ray*math.sin(angle)*0.9, y0 - ray*math.cos(angle)*0.9, x0+ray*math.sin(angle)*0.98, y0 - ray*math.cos(angle)*0.98, fill="#fff", width=2)
			self.create_text(x0+ray*math.sin(angle)*0.75, y0 - ray*math.cos(angle)*0.75, text=v,fill=self.digitals_color,font=frame_font)
			if i==int(vmax-vmin)/step:
				continue
			for dv in range(1, 5):
				angle = (5+6*((v+dv*(step/5)-vmin)/(vmax-vmin)))*math.pi/4
				self.create_line(x0+ray*math.sin(angle)*0.94, y0 - ray*math.cos(angle)*0.94, x0+ray*math.sin(angle)*0.98, y0 - ray*math.cos(angle)*0.98,fill="#FFF")
		
		self.needle = self.create_line(x0-ray*math.sin(5*math.pi/4)*len2, y0+ray*math.cos(5*math.pi/4)*len2, x0+ray*math.sin(5*math.pi/4)*len1, y0-ray*math.cos(5*math.pi/4)*len1, width=7, fill=self.arrow_color) # Стрелка
		
		#self.create_oval(x0-ray*coef-40, y0-ray*coef+110, x0+ray*coef+40, y0+ray*coef+190, fill=self.alert1_color) # Круг предупреждения

	def draw_needle(self, v):
			
		if (v < 61) & (v > 0):
			if self.ring_color != self.alert1_color:
				self.ring_color = self.alert1_color
				self.itemconfig(self.metr, outline=self.ring_color)
				
		if (v < 91) & (v > 61):
			if self.ring_color != self.alert2_color:
				self.ring_color = self.alert2_color
				self.itemconfig(self.metr, outline=self.ring_color)
				
		if (v < 180) & (v > 91):
			if self.ring_color != self.alert3_color:
				self.ring_color = self.alert3_color
				self.itemconfig(self.metr, outline=self.ring_color)	
	
		v = max(v,self.vmin)
		v = min(v,self.vmax)
		angle = (5+6*((v-self.vmin)/(self.vmax-self.vmin)))*math.pi/4
		self.coords(self.needle, x0-ray*math.sin(angle)*len2, y0+ray*math.cos(angle)*len2, x0+ray*math.sin(angle)*len1, y0-ray*math.cos(angle)*len1)
		

class Rpm(Canvas):
	digitals_color = "#FFFFFF"    # Цвет цифр
	arrow_color    = "#ff0000"    # Цвет стрелки
	alert1_color   = "#339966"    # Цвет круга предупреждения (нормально)
	alert2_color   = "#ffcc00"    # Цвет круга предупреждения (допустимо)
	alert3_color   = "#ff3300"    # Цвет круга предупреждения (критично)
	ring_color     = alert1_color # Цвет кольца спидометра (начальный цвет)
	meter_color    = "#000000"    # Цвет циферблата

	def draw(self, vmin, vmax, step):
		self.vmin = vmin
		self.vmax = vmax
		self.step = step
		x0        = width/2
		y0        = width/2
		ray       = int(0.85*width/2)
		
		self.metr = self.create_oval(x0-ray*1.1, y0-ray*1.1, x0+ray*1.1, y0+ray*1.1, fill=self.meter_color, outline=self.ring_color, width=30) # Параметры спидометра
		coef = 0.1
		self.create_oval(x0-ray*coef, y0-ray*coef, x0+ray*coef, y0+ray*coef, fill="#2C2C25")
		for i in range(1+int((vmax-vmin)/step)):
			v     = vmin + step*i
			angle = (5+6*((v-vmin)/(vmax-vmin)))*math.pi/4
			self.create_line(x0+ray*math.sin(angle)*0.9, y0 - ray*math.cos(angle)*0.9, x0+ray*math.sin(angle)*0.98, y0 - ray*math.cos(angle)*0.98, fill="#fff", width=2)
			self.create_text(x0+ray*math.sin(angle)*0.75, y0 - ray*math.cos(angle)*0.75, text=v,fill=self.digitals_color,font=frame_font)
			if i==int(vmax-vmin)/step:
				continue
			for dv in range(1, 5):
				angle = (5+6*((v+dv*(step/5)-vmin)/(vmax-vmin)))*math.pi/4
				self.create_line(x0+ray*math.sin(angle)*0.94, y0 - ray*math.cos(angle)*0.94, x0+ray*math.sin(angle)*0.98, y0 - ray*math.cos(angle)*0.98,fill="#FFF")
		
		self.needle = self.create_line(x0-ray*math.sin(5*math.pi/4)*len2, y0+ray*math.cos(5*math.pi/4)*len2, x0+ray*math.sin(5*math.pi/4)*len1, y0-ray*math.cos(5*math.pi/4)*len1, width=7, fill=self.arrow_color) # Стрелка
		
		#self.create_oval(x0-ray*coef-40, y0-ray*coef+110, x0+ray*coef+40, y0+ray*coef+190, fill=self.alert1_color) # Круг предупреждения

	def draw_needle(self, v):
		v = v / 1000
		
		#if v == 3.6:
		#	self.metr_color = self.alert3_color
		#	self.draw(self.vmin, self.vmax, self.step)
			
		if (v < 2.5) & (v > 0):
			if self.ring_color != self.alert1_color:
				self.ring_color = self.alert1_color
				self.itemconfig(self.metr, outline=self.ring_color)
				
		if (v < 3.6) & (v > 2.5):
			if self.ring_color != self.alert2_color:
				self.ring_color = self.alert2_color
				self.itemconfig(self.metr, outline=self.ring_color)
				
		if (v < 7) & (v > 3.6):
			if self.ring_color != self.alert3_color:
				self.ring_color = self.alert3_color
				self.itemconfig(self.metr, outline=self.ring_color)	
		
	
		v = max(v,self.vmin)
		v = min(v,self.vmax)
		angle = (5+6*((v-self.vmin)/(self.vmax-self.vmin)))*math.pi/4
		self.coords(self.needle, x0-ray*math.sin(angle)*len2, y0+ray*math.cos(angle)*len2, x0+ray*math.sin(angle)*len1, y0-ray*math.cos(angle)*len1)

#######################################################################################################

# Фрэйм с датчиками
f = Frame(form1, bg="black")

#	Датчик скорости
speed = Speed(f, width=width, height=height, bg="black", bd = 0, highlightthickness=0, relief="ridge")
speed.draw(0, 180, 20)
speed.pack(side=LEFT)
#speed.draw_needle (50)

#	Датчик оборотов в минуту
rpm = Rpm(f, width=width, height=height, bg="black", bd = 0, highlightthickness=0, relief="ridge")
rpm.draw(0, 7, 1)
rpm.pack(side=LEFT)
#rpm.draw_needle (6.2)

f.pack()

# Кнопка закрытия приложения
Button1 = Button(form1, text = 'X', command=lambda:Button1Click(form1)).place(x=10, y=500, width=90, height=90)

# Кнопка сброса ошибок
Button2 = Button(form1, text = 'ХХХ', command=Button2Click).place(x=915, y=500, width=100, height=90)

# Надпись в низу экрана
label1 = Label(form1, textvariable=txt, fg="#eee", bg="#000000", font=("Helvetica", 40))
label1.pack()
label1.place(x=150, y=500)

txt.set("0000")

# Соединяемся с ECU
connection = obd.OBD(portstr="/dev/ttyUSB0", baudrate=38400, fast=True) 

# Поток для получения информации с ECU
ttt = threading.Thread(target=GetInf, args=())
ttt.daemon = True
ttt.start()


# Поток для тестов датчиков
#t1 = threading.Thread(target=Test, args=())
#t1.daemon = True
#t1.start()
	
form1.mainloop()