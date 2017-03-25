#!/usr/bin/env python2
# -*- coding:utf-8 -*-

# Arroyo Calle, Adrián
# Crespo Jiménez, Cristina Alejandra

# TODO: Salirse si una mal
# TODO: pintar nivel - DONE
# TODO: Fix output
# TODO: Documentación? 


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

import coche

def pintar_nivel(nivel):
    print CES + (COES + COE*5)*6 + COES + CSO
    for y in range(1,7):
        for line in range(0,3):
            print CNS,
            for x in range(1,7):
                pintado = False
                for coche in nivel:
                    if coche.img(x,y) != None:
                        print coche.img(x,y)[line],
                        pintado = True
                        break
                if not pintado:
                    print " "*5,
            print CNS if y != 3 else CSOM
        if y != 6:
            print CNES + " "*37 + CONS
    print CNE + (CONE + COE*5)*6 + CONE + CON


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
        
    
        

def play_menu():
    """ Muestra el menú de selección de nivel """
    max_level = (len(records) + 1)
    n_nivel = -1
    while n_nivel < 1 or n_nivel > max_level:
        n_nivel = raw_input("Elige el nivel a jugar (1-%d)" % max_level)
        n_nivel = int(n_nivel)
    print "Jugando nivel", n_nivel
    in_game(n_nivel)
    return None

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

print "Anrokku"
print "="*80
print "Arroyo Calle, Adrián"
print "Crespo Jiménez, Cristina Alejandra"
print ""

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
play_menu()


print "Gracias por jugar"
