#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import coche

def play_menu():
    """ Muestra el menú de selección de nivel """

    return None

def write_records():
	f_records = open("records.txt","w")
	for record in records:
		f_records.write(str(record))
		f_records.write("\n")
def read_records():
	f_records = open("records.txt","r")
	for line in f_records:
		records.append(int(line))
	print records		
		

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

for i in range(0,n_niveles):
	n_coches = int(f_niveles.readline())
	coches = []
	for j in range(0,n_coches):
		coches.append(coche.Coche(f_niveles.readline()))
	niveles.append(coches[:])

play_menu()

print "Gracias por jugar"
