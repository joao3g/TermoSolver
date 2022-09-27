# -*- coding: utf-8 -*-
import re

file = open('words_pt-br_five_letters.txt', 'r')
words = file.readlines()

excluded = []
contains = {}
awnser = {0: '', 1: '', 2: '', 3: '', 4: ''}
exclusiveOne = []

def checkExcluded(word):
     for letter in excluded:
          result = word.find(letter)
          if(result > -1):
               return False
     return True

def checkContains(word):
     for letter in contains:
          if(word.find(letter) == -1):
               return False
               
          occurrences = [m.start() for m in re.finditer(letter, word)]
          for i in occurrences:
               for j in contains[letter]:
                    if(j == i):
                         return False
          
     return True

def checkExact(word):
     for index in awnser:
          if(awnser[index] != ''):
               if(awnser[index] != word[index]):
                    return False
     return True

def checkExclusivelyOne(word):
     for letter in exclusiveOne:
          if(word.count(letter) != 1):
               return False
     return True

def getInfo():
     data = input("Insira os dados descobertos (Letra, Posicao) (0 para letra invalida): ")
     if data==0:
          exit()
     dataArray = data.split(" ")

     for info in dataArray:
          infoArray = info.split(",")
          do = True
          
          letter = infoArray[0]
          position = int(infoArray[1])

          # Impede de remover letra já inserida
          for index in awnser:
               if(awnser[index]==letter and position==0):
                    do = False
                    exclusiveOne.append(letter)
          
          if(do):
               if(position > 0):
                    awnser[(position-1)] = letter
               elif(position < 0):
                    if(letter in contains):
                         contains[letter].append((abs(position)-1))
                    else:
                         contains[letter] = [(abs(position)-1)]
               else:
                    excluded.append(letter)

def mainLoop():

     while True:
          getInfo()

          for word in words:
               if(checkExcluded(word) and checkContains(word) and checkExact(word) and checkExclusivelyOne(word)):
                    print(word)

mainLoop()