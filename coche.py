# -*- coding:utf-8 -*-

class Coche:
    def __init__(self,load_data):
        """ Parsea los datos de cada coche según el formato del fichero e inicializa sus variables internas """
        self.orientation = load_data[0]
        self.x = load_data[1]
        self.y = load_data[2]
        self.size = load_data[3]
    def mover(self,direction):
        if self.orientation == "H":
            self.x = self.x + direction
        else:
            self.y = self.y + direction
