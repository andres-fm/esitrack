#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

s = requests.Session()

def generate_alphabet_soup(w, h , ltr, rtl, ttb, btt, d):
    """
    Makes POST request with given alphabet soup constructor parameters to create soup and returns its id
    """
    r = s.post('http://127.0.0.1:8080/alphabetSoup/', data = {'w':w, 'h':h, 'ltr':ltr, 'rtl':rtl, 'ttb':ttb, 'btt':btt, 'd':d})
    if r.status_code != 200:
        raise Exception('Error. Remember 15 <= w,h <= 80 and the rest are True or False')
    return r.text

def view_list_of_words(uuid):
    """
    Makes GET request with given alphabet soup id to see its word list
    """
    r = s.get('http://127.0.0.1:8080/alphabetSoup/list/'+uuid)
    if r.status_code != 200:
        raise Exception('Error. Verify given id actually exists')
    return r.text

def view_board(uuid):
    """
    Makes GET request with given alphabet soup id to see its board
    """
    r = s.get('http://127.0.0.1:8080/alphabetSoup/view/'+uuid)
    if r.status_code != 200:
        raise Exception('Error. Verify given id actually exists')
    return r.text

def find_word(uuid, sr, er, sc, ec):
    """
    Makes PUT request with given alphabet soup id to see if in the given location there is a soup word
    """
    r = s.put('http://127.0.0.1:8080/alphabetSoup/'+uuid, params={'sr':sr, 'er':er, 'sc':sc, 'ec':ec})
    return r.text

def interact_create_soup():
    """
    Interacts with user to obtain soup parameters for creation, and then generates it with them
    """
    params = raw_input("Desea ingresar parametros al juego? y/n ")
    params = params == 'y'
    w, h , ltr, rtl, ttb, btt, d = 15, 15, 'True', 'False', 'False', 'False', 'False'
    if params:
        w = int(raw_input('Ancho: entero entre 15 y 80 = '))
        while not w >= 15 and w <=80:
            w = int(raw_input('Ancho: entero entre 15 y 80 = '))
        h = int(raw_input('Alto: entero entre 15 y 80 = '))
        while not h >= 15 and h <=80:
            h = int(raw_input('Alto: entero entre 15 y 80 = '))
        ltr = raw_input("Permitir paralabras de izquierda a derecha? y/n ")
        ltr = ltr == 'y'
        rtl = raw_input("Permitir paralabras de derecha a izquierda? y/n ")
        rtl = rtl == 'y'
        ttb = raw_input("Permitir paralabras de arriba hacia abajo? y/n ")
        ttb = ttb == 'y'
        btt = raw_input("Permitir paralabras de abajo hacia arriba? y/n ")
        btt = btt == 'y'
        d = raw_input("Permitir paralabras en diagonal? y/n ")
        d = d == 'y'
    return generate_alphabet_soup(w, h, ltr, rtl, ttb, btt, d)

def interact_see_list():
    """
    Interacts with user to obtain soup id, and then requests the web service to see the soup's word list
    """
    uuid = raw_input("Ingrese el identificador de la sopa de letras: ")
    return view_list_of_words(uuid)

def interact_see_soup():
    """
    Interacts with user to obtain soup id, and then requests the web service to see the soup's board
    """
    uuid = raw_input("Ingrese el identificador de la sopa de letras: ")
    return view_board(uuid)

def interact_encuentra_palabra():
    """
    Interacts with user to obtain where he thinks there is a word, and then requests the PUT web service to verify it
    """
    uuid = raw_input("Ingrese el identificador de la sopa de letras: ")
    print("Ingrese la ubicación de la palabra (indexando la sopa desde 0)")
    while True:
        try:
            sr = int(raw_input('Renglón inicial: '))
        except ValueError:
            print("Debe ingresar un entero")
        else:
            break

    while True:
        try:
            er = int(raw_input('Renglón final: '))
        except ValueError:
            print("Debe ingresar un entero")
        else:
            break

    while True:
        try:
            sc = int(raw_input('Columna inicial: '))
        except ValueError:
            print("Debe ingresar un entero")
        else:
            break

    while True:
        try:
            ec = int(raw_input('Columna final: '))
        except ValueError:
            print("Debe ingresar un entero")
        else:
            break

    return find_word(uuid, sr, er, sc, ec)



if __name__ == '__main__':
    print("bienvenido al demo del juego de sopa de letras")
    while True:
        try:
            accion = int(raw_input("Indique el número de lo que desea hacer\n1.Crear sopa de letras\n2.Ver lista de palabras en sopa de letras\n3.Ver sopa de letras\n4.Encontrar palabra en sopa de letras\n5.Salir"))
        except ValueError:
            print("Debe ingresar un entero")
            continue
        if accion == 1:
            print(interact_create_soup() + ' es el id de la sopa generada')
        elif accion == 2:
            print('las palabras en la sopa de letras don ' + str(interact_see_list()))
        elif accion == 3:
            print(interact_see_soup())
        elif accion == 4:
            print(interact_encuentra_palabra())
        elif accion == 5:
            exit(0)
        else:
            print('Opción no reconocida')
    
