#!/usr/bin/env python2
# -*- coding:utf-8 -*-

# Arroyo Calle, Adrián
# Crespo Jiménez, Cristina Alejandra

import coche
import gtk
import cairo
import math

class GameArea(gtk.DrawingArea):
	def __init__(self):
		super(GameArea,self).__init__()
		self.connect("expose-event",self.expose)
		self.car = gtk.gdk.pixbuf_new_from_file("data/car2.png")
                self.limo = gtk.gdk.pixbuf_new_from_file("data/limo.png")
	def expose(self,widget,context):
		cr = widget.window.cairo_create()
		width, height = widget.window.get_size()
		cr.rectangle(0,0,width,height)
		cr.set_source_rgb(1,1,1)
		cr.fill()
		#cr.set_source_rgb(1,0,0)
		#cr.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
		#cr.set_font_size(20)
		#cr.move_to(20,20)
		#cr.show_text("Anrokku")
		cr.save()
		#cr.scale()
		#cr.set_source_pixbuf(self.car,0,0)
		#cr.rectangle(100,100,100,100) y cr.clip() si quieres recortar
		cr.paint()
		cr.restore()

                ## PAINT CARS
                for car in self.level:
                    cr.save()
                    img = self.car if car.size == 2 else self.limo
                    img_width = 256
                    img_height = 128
                    x_scale = float(width) / float(img_width)
                    y_scale = float(height) / float(img_height)
                    cr.scale(x_scale/3,y_scale/6)
                    if car.orientation == "V":
                        cr.translate((car.x)*128,(car.y)*128)
                        cr.rotate(math.pi/2)
                        cr.translate(-(car.x)*128,-(car.y-1)*128)
                    cr.set_source_pixbuf(img,(car.x -1)*128,(car.y - 1)*128)
                    cr.paint()
                    cr.restore()
        def set_level(self,level):
            self.level = level

class Ventana(gtk.Window):
	def __init__(self):
		super(Ventana,self).__init__()
		self.set_title("Anrokku")
		self.set_default_size(640,480)
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
names = "ABCDEFGHIJQLMNOPQRSTUVWXYZ"

for i in range(0,n_niveles):
    n_coches = int(f_niveles.readline())
    coches = []
    for j in range(0,n_coches):
        coches.append(coche.Coche(f_niveles.readline(),names[j]))
    niveles.append(coches[:])

# START

ventana = Ventana()
gtk.main()
