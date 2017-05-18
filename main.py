#!/usr/bin/env python2
# -*- coding:utf-8 -*-

# Arroyo Calle, Adrián
# Crespo Jiménez, Cristina Alejandra

import gtk
import coche
import cairo
import math
import sys

class GameArea(gtk.DrawingArea):
	def __init__(self):
		super(GameArea,self).__init__()
		self.set_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK)
		self.connect("expose-event",self.expose)
		self.connect("button-press-event",self.drag_start)
		self.connect("button-release-event",self.drag_end)
		self.connect("motion-notify-event",self.drag)
		self.car = None
		self.x_start = 0
		self.y_start = 0
                self.win = False
                self.movements = 0
                self.n_nivel = 0
                self.level = niveles[0][:]
                self.set_level(self.level)
                self.asphalt = gtk.gdk.pixbuf_new_from_file("data/asphalt.png")
	def expose(self,widget,context):
		cr = widget.window.cairo_create()
		width, height = widget.window.get_size()
                if not self.win:
                    cr.rectangle(0,0,width,height)
                    cr.set_source_rgb(1,1,1)
                    cr.fill()
                    cr.save()
                    cr.scale(float(width)/float(512),float(height)/float(512))
                    cr.set_source_pixbuf(self.asphalt,0,0)
                    cr.paint()
                    cr.restore()

                    ## PAINT CARS
                    for car in self.level:
                        cr.save()
                        img_width = 256
                        img_height = 128
                        x_scale = float(width) / float(img_width)
                        y_scale = float(height) / float(img_height)
                        cr.scale(x_scale/3,y_scale/6)
                        if car.orientation == "V":
                            cr.translate(car.real_x + 128,car.real_y + 128)
                            cr.rotate(math.pi/2)
                            cr.translate(-car.real_x - 128,-car.real_y)
                        cr.set_source_pixbuf(car.img,car.real_x,car.real_y)
                        cr.paint()
                        cr.restore()
                    cr.set_source_rgb(0,0,0)
                    cr.select_font_face("Monospace",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                    cr.set_font_size(16)
                    cr.move_to(10,round(height/8)*7.75)
                    try:
                        cr.show_text("NIVEL "+str(self.n_nivel + 1)+"  RECORD: "+str(records[self.n_nivel])+"  MOVIMIENTOS: "+str(int(self.movements)))
                    except:
                        cr.show_text("NIVEL "+str(self.n_nivel +1) +"  RECORD: No establecido  MOVIMIENTOS: "+str(int(self.movements)))
                else:
                    cr.rectangle(0,0,width,height)
                    cr.set_source_rgb(0,0,1)
                    cr.fill()
                    cr.set_source_rgb(1,1,1)
                    cr.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                    cr.set_font_size(round(width/8))
                    cr.move_to(round(width/8),round(height/2))
                    cr.show_text("¡Victoria!")
	def drag_start(self,widget,event):
            if not self.win:
		width, height = widget.window.get_size()
		u_width = width / 6
		u_height = height / 6
		for car in self.level:
			if u_width*(car.x -1) < event.x < u_width*(car.x + ( (car.size -1) if car.orientation == "H" else 0)):
				if u_height*(car.y -1) < event.y < u_height*(car.y+(( car.size -1) if car.orientation == "V" else 0)):
					self.car = car
                                        self.x_init = car.x
                                        self.y_init = car.y
					self.x_start = self.car.real_x - event.x
					self.y_start = self.car.real_y - event.y
					break
            else:
                selector = Selector()
                n_nivel = selector.run()
                selector.destroy()
                self.load_level(n_nivel)
	def drag_end(self,widget,event):
		if self.car != None:
			self.car.x = round((self.car.real_x/128)+1)
			self.car.y = round((self.car.real_y/128)+1)

                        self.movements += abs(self.x_init - self.car.x) + abs(self.y_init - self.car.y)
                        
                        if self.level[0].x == 6 and self.level[0].y == 3:
                            self.win = True
                            try:
                                if self.movements < records[self.n_nivel]:
                                    records[self.n_nivel] = int(self.movements)
                                    write_records()
                            except:
                                records.append(int(self.movements))
                                write_records()


			self.car = None
			self.set_level(self.level)
			self.queue_draw()
	def drag(self,widget,event):
		if self.car != None:
			if self.car.orientation == "H":
				self.car.real_x += (event.x - self.car.real_x) + self.x_start
				if self.car.real_x > (self.car.x-1)*128:
					if not self.car.casilla_libre(1,self.level):
						self.car.real_x = (self.car.x-1)*128
					else:
						self.car.x += 1
				if self.car.real_x < (self.car.x-1)*128:
					if not self.car.casilla_libre(-1,self.level):
						self.car.real_x = (self.car.x-1)*128
					else:
						self.car.x -= 1
			else:
				self.car.real_y += (event.y - self.car.real_y) + self.y_start
				if self.car.real_y > (self.car.y-1)*128:
					if not self.car.casilla_libre(1,self.level):
						self.car.real_y = (self.car.y-1)*128
					else:
						self.car.y += 1
				if self.car.real_y < (self.car.y-1)*128:
					if not self.car.casilla_libre(-1,self.level):
						self.car.real_y = (self.car.y-1)*128
					else:
						self.car.y -= 1
			self.queue_draw()
			
        def set_level(self,level):
            self.level = level
            for car in self.level:
		car.real_x = (car.x -1)*128
		car.real_y = (car.y -1)*128
        def load_level(self,n_nivel):
            self.level = niveles[n_nivel][:]
            self.set_level(self.level)
            self.n_nivel = n_nivel
            self.movements = 0
            self.win = False
            self.queue_draw()

class Ventana(gtk.Window):
	def __init__(self):
		super(Ventana,self).__init__()
		self.set_title("Anrokku")
		self.set_default_size(500,500)
		self.game = GameArea()
		self.add(self.game)
		self.connect("delete-event",self.menu)
                self.connect("destroy",lambda x: sys.exit(0))
		self.show_all()
                self.menu(self)
	def menu(self,widget,data=None):
            selector = Selector()
            n_level = selector.run()
            if n_level == -1:
                self.destroy()
            selector.destroy()
            if n_level == -2:
                self.menu(self)
            else:
                self.game.load_level(n_level)
            return True

class Selector(gtk.Dialog):
    def __init__(self):
        super(Selector,self).__init__(flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT)
        self.set_title("Anrokku - Main Menu")
        self.set_default_size(200,400)
        img = gtk.Image()
        img.set_from_file("data/Anrokku.png")
        self.vbox.pack_start(img)
        label = gtk.Label("Selecciona el nivel")
        self.vbox.pack_start(label)
        combo = gtk.combo_box_new_text()
        for i in range(len(records)+1):
            combo.append_text("NIVEL "+str(i+1))
        self.vbox.pack_start(combo)
        combo.connect("changed",self.set)
        salir = gtk.Button("Salir de Anrokku")
        self.vbox.pack_start(salir)
        salir.connect("clicked",self.confirmar)
        self.connect("delete-event",self.confirmar)
        self.show_all()
    def set(self,widget):
        i = widget.get_active()
        n_level = i
        self.response(n_level)
    def confirmar(self,widget,data=None):
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_YES_NO,flags=gtk.DIALOG_MODAL)
        dialog.set_title("Anrokku")
        dialog.set_markup("¿Desea salir de Anrokku?")
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            self.response(-1)
        else:
            self.response(-2)
        return True

def write_records():
    with open("records.txt","w") as f_records:
        for record in records:
            f_records.write(str(record))
            f_records.write("\n")
def read_records():
    try:
        f_records = open("records.txt","r")
        for line in f_records:
            records.append(int(line))
    except:
        pass

records = []
read_records()


niveles = []
def read_levels():
    f_niveles = open("niveles.txt","r")
    n_niveles = f_niveles.readline()
    n_niveles = int(n_niveles)
    names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(0,n_niveles):
        n_coches = int(f_niveles.readline())
        coches = []
        for j in range(0,n_coches):
            coches.append(coche.Coche(f_niveles.readline(),names[j], True if j == 0 else False))
        niveles.append(coches[:])
read_levels()
# START
Ventana()
gtk.main()
