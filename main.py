#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import coche

def play_menu():
    """ Muestra el menú de selección de nivel """

    return None

def see_records():
    """ Muestra los récords actualmente guardados y ofrece una opción para resetearlos"""

    return None





print "Anrokku"
print "="*80
print "Arroyo Calle, Adrián"
print "Crespo Jiménez, Cristina Alejandra"
print ""

exit = False

while not exit:
    print "MENÚ PRINCIPAL"
    print "1. Jugar"
    print "2. Ver récords"
    print "0. Salir"
    
    option = -1
    while option < 0 or option > 2:
        option = raw_input("Selecciona la opción: ")
        try:
            option = int(option)
        except:
            pass
    if option == 1:
        play_menu()
    elif option == 2:
        see_records()
    else:
        exit = True

print "Gracias por jugar"
