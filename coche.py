# -*- coding:utf-8 -*-

COE = u'\u2500' # ─
CNS = u'\u2502' # │
CES = u'\u250C' # ┌
CSO = u'\u2510' # ┐
CNE = u'\u2514' # └
CON = u'\u2518' # ┘
COES = u'\u252C' # ┬
CNES = u'\u251C' # ├
CONS = u'\u2524' # ┤
CONE = u'\u2534' # ┴
CSOM = u'\u2593' # ▒ 


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
    def img(self, x, y):
        if x == self.x and y == self.y:
            if self.orientation == "H":
                return [CES+COE*4,CNS+self.name+" "*3,CNE+COE*4]
            else:
                return [CES+COE*3+CSO,CNS+" "+self.name+" "+CNS,CNS+" "*3+CNS]
        if x == self.x + self.size -1 and y == self.y and self.orientation == "H":
            return [COE*4+CSO," "*3+self.name.lower()+CNS,COE*4+CON]
        if x == self.x and y == self.y + self.size -1 and self.orientation == "V":
            return [CNS+" "*3+CNS,CNS+" "+self.name.lower()+" "+CNS,CNE+COE*3+CON]
        if self.x < x < self.x + self.size and self.y == y and self.orientation == "H":
            return [COE*5," "*5,COE*5]
        if self.y < y < self.y + self.size and self.x == x and self.orientation == "V":
            return [CNS+" "*3+CNS,CNS+" "*3+CNS,CNS+" "*3+CNS]

        return None
    def mover(self,direction):
        if self.orientation == "H":
            self.x = self.x + direction
        else:
            self.y = self.y + direction
