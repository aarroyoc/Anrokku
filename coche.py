# -*- coding:utf-8 -*-

class Coche:
    def __init__(self,load_data,name):
        """ Parsea los datos de cada coche según el formato del fichero e inicializa sus variables internas """
        self.name = name
        self.orientation = load_data[0]
        self.x = int(load_data[1])
        self.y = int(load_data[2])
        self.size = int(load_data[3])
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
        if y < 1 or y > 6:
            libre = False
            if y == 7 and x == 3:
                libre = True
        return libre
    def mover(self,direction):
        if self.orientation == "H":
            self.x = self.x + direction
        else:
            self.y = self.y + direction
