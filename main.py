#!/usr/bin/env python2
# -*- coding:utf-8 -*-

# Arroyo Calle, Adrián
# Crespo Jiménez, Cristina Alejandra

# TODO: with open
# TODO: Mover con raton
# TODO: Elegir nivel
# TODO: Contar movimientos
# TODO: Asfalto -> marcas
# TODO: Pantalla de victoria

import coche
import gtk
import cairo
import math

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
					self.x_start = self.car.real_x - event.x
					self.y_start = self.car.real_y - event.y
					break
	def drag_end(self,widget,event):
		if self.car != None:
			self.car.x = round((self.car.real_x/128)+1)
			self.car.y = round((self.car.real_y/128)+1)
                        if self.car.x == 6 and self.car.y == 3:
                            self.win = True
                            print "Victoria"
			# TODO CONTAR MOVIMIENTOS 
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

class Ventana(gtk.Window):
	def __init__(self):
		super(Ventana,self).__init__()
		self.set_title("Anrokku")
		self.set_default_size(500,500)
		self.game = GameArea()
                self.game.set_level(niveles[0][:])
		self.add(self.game)
		self.connect("delete-event",self.confirmar)
		self.connect("destroy",gtk.main_quit)
		self.show_all()
	def confirmar(self,widget,event,data=None):
		dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_YES_NO,flags=gtk.DIALOG_MODAL)
		dialog.set_title("Anrokku")
		dialog.set_markup("¿Desea salir de Anrokku?")
		response = dialog.run()
		if response == gtk.RESPONSE_YES:
			return False
		else:
			dialog.destroy()
			return True

def in_game(n_nivel):
    j_nivel = niveles[n_nivel - 1][:]
    win = False
    movimientos = 0
    while not win:
        # MOSTRAR RECORD
        print "NIVEL",n_nivel, "- RECORD",( records[n_nivel - 1] if len(records) >= n_nivel else "SIN BATIR")
        pintar_nivel(j_nivel)
        entrada = raw_input("Introduzca los movimientos: ")
        try:
            for c in entrada:
                for car in j_nivel:
                    if car.name == c.upper():
                        direccion = 1 if c.lower() == c else -1
                        if car.casilla_libre(direccion,j_nivel):
                            car.mover(direccion)
                            movimientos += 1
                        else:
                            print "Movimiento",c,"bloqueado"
                            raise
                ## COMPROBAR CONDICIÓN DE VICTORIA
                if j_nivel[0].y == 3 and j_nivel[0].x == 6:
                    win = True
        except:
            pass
    ## GUARDAR RECORD
    print "Enhorabuena, has ganado"
    try:
        records[n_nivel - 1] = movimientos
    except:
        records.append(movimientos)
    write_records()
    
    if n_nivel != len(niveles):
        siguiente=raw_input("¿Desea jugar al siguiente nivel? [S/N]")
        if siguiente.upper() == "S":
            in_game(n_nivel+1)
        else:
            pass

def write_records():
    f_records = open("records.txt","w")
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

# START

ventana = Ventana()
gtk.main()
