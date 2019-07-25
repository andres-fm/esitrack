#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
import uuid
from random import randint

import cherrypy
class Soup:
    words = [word[:-1] for word in open("words.txt")]        
    def __init__(self, w, h, ltr, rtl, ttb, btt, d):
        self.w = w
        self.h = h
        self.ltr = ltr == 'True'
        self.rtl = rtl == 'True'
        self.ttb = ttb == 'True'
        self.btt = btt == 'True'
        self.d = d == 'True'
        self.id = str(uuid.uuid4())
        #TODO validar si el tama;o es correcto
        self.board = [[' ' for j in range(self.w)] for i in range(self.h)]
        self.empty_cell = [[True for j in range(self.w)] for i in range(self.h)]
        self.__used_words = [False for _ in range(len(Soup.words))]
        self.words = []
        self.__create_board()

    def __str__(self):
        return '\n'.join(['|'+'|'.join(row)+'|' for row in self.board])


    def __create_board(self):
        num_words = int(self.w * self.h * 0.02)#number of words to put in soup
        permissions = []
        if self.ltr:
            permissions.append(0)
        if self.rtl:
            permissions.append(1)
        if self.ttb:
            permissions.append(2)
        if self.btt:
            permissions.append(3)
        if self.d:
            permissions.append(4)
        if len(permissions) == 0:
            raise Exception("Seas mamon, da permisos")
        while num_words >= 0:
            #randomly selects direction
            direction = permissions[randint(0,len(permissions)-1)] 
            #randomly selects a word
            word_idx = randint(0, len(Soup.words)-1)
            while self.__used_words[word_idx]:
                word_idx = randint(0, len(Soup.words)-1)
            word = Soup.words[word_idx]
            self.__used_words[word_idx] = True
            #adds a word until it succeeds
            while not self.__add_word(direction, word): 
                pass
            num_words -= 1
        #fills the rest of cells
        for i in range(self.h):
            for j in range(self.w):
                if self.empty_cell[i][j]:
                    self.board[i][j] = chr(randint(ord('a'), ord('z')))

    def __empty_cell(self, i, j):
        if i < 0 or i >= self.h or j < 0 or j >= self.w:
            return False
        return self.empty_cell[i][j]

    def __add_word(self, direction, word):
        #randomly selects initial word position on board
        i, j = randint(0, self.h-1), randint(0, self.w-1)

        if direction == 0:
           return self.__add_word_aux(i, j, 0, 1, word)
        elif direction == 1:
           return self.__add_word_aux(i, j, 0, -1, word)
        elif direction == 2:
           return self.__add_word_aux(i, j, 1, 0, word)
        elif direction == 3:
           return self.__add_word_aux(i, j, -1, 0, word)
        elif direction == 4:
           return self.__add_word_aux(i, j, 1, 1, word)

    def __add_word_aux(self, i, j, ii, jj, word):
        current_i = i
        current_j = j
        for _ in range(len(word)):
            if not self.__empty_cell(current_i, current_j):
                return False
            current_i += ii
            current_j += jj
            
        current_i = i
        current_j = j
        for c in word:
            self.board[current_i][current_j] = c
            self.empty_cell[current_i][current_j] = False
            current_i += ii
            current_j += jj
        self.words.append((word, (i, j)))
        return True


        

class alphabetSoupService(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="generate">
              Ancho    <input type="w" value="15" name="w" />
              <br>
              Largo    <input type="h" value="15" name="h" />
              <br>
              izq->der <input type="ltr" value="True" name="ltr" />
              <br>
              der->izq <input type="rtl" value="False" name="rtl" />
              <br>
              arr->ab  <input type="ttb" value="False" name="ttb" />
              <br>
              ab->arr  <input type="btt" value="False" name="btt" />
              <br>
              diagona  <input type="d" value="False" name="d" />
              <br>
              <button type="submit">Give it now!</button>
              <br>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def alphabetSoup(self, w=15, h=15, ltr=True, rtl=False, ttb=False, btt=False, d=False):
        s = Soup(w,h,ltr,rtl,ttb,btt,d)
        return s.id
    #''.join(random.sample(string.hexdigits, int(length)))


if __name__ == '__main__':
    """
    #a = Soup(15, 15, 'True', 'False', 'False', 'False', 'False')
    a = Soup(15, 15, 'True', 'True', 'True', 'True', 'True')
    print(a)
    print(a.words)
    print(len(a.words))
    """
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }
    service = alphabetSoupService()
    #cherrypy.tree.mount(index.stream(), '/input/stream', {})
    cherrypy.quickstart(service, '/', conf)
