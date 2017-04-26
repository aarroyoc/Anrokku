# -*- coding:utf-8 -*-

import gtk
import random

IMG_SIZE2 = ["data/car1.png","data/car2.png","data/car3.png","data/car4.png"]
IMG_SIZE3 = ["data/limo.png","data/truck.png"]

class Coche:
    def __init__(self,load_data,first=False):
        """ Parsea los datos de cada coche según el formato del fichero e inicializa sus variables internas """
        self.orientation = load_data[0]
        self.x = int(load_data[1])
        self.y = int(load_data[2])
        self.size = int(load_data[3])
	if first:
		path = IMG_SIZE2[3]
	elif self.size == 2:
		path = IMG_SIZE2[random.randint(0,2)]
	else:
		path = IMG_SIZE3[random.randint(0,1)]
	self.img = gtk.gdk.pixbuf_new_from_file(path)
		
    def libre(self,x,y):
        if self.orientation == "H":
            if x >= self.x and x < self.x + self.size:
                if y == self.y:
                    return False
        else:
            if y >= self.y and y < self.y + self.size:
                if x == self.x:
                    return False
        return True
    def casilla_libre(self,direction,nivel):
        x = self.x
        y = self.y
        if self.orientation == "H":
            x += self.size if direction > 0 else direction
        else:
            y += self.size if direction > 0 else direction
        libre = True
        for car in nivel:
            if car.name != self.name:
                libre = libre and car.libre(x,y)
        if x < 1 or x > 6:
            libre = False
            if x == 7 and y == 3:
                libre = True
        if y < 1 or y > 6:
            libre = False
        return libre

    def mover(self,direction):
        if self.orientation == "H":
            self.x = self.x + direction
        else:
            self.y = self.y + direction
