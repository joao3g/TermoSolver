# -*- coding: utf-8 -*-

file = open('words_pt-br_five_letters.txt', 'r')
words = file.readlines()

excluded = []
contains = {}
awnser = {0: '', 1: '', 2: '', 3: '', 4: ''}


def checkExcluded(word):
     for letter in excluded:
          result = word.find(letter)
          if(result > -1):
               return False
     return True

def checkContains(word):
     for letter in contains:
          result = word.find(letter)
          if(result == -1):
               return False
          for i in contains[letter]:
               if(result == i):
                    return False
     return True

def checkExact(word):
     for index in awnser:
          if(awnser[index] != ''):
               if(awnser[index] != word[index]):
                    return False
     return True

def getInfo():
     data = raw_input("Insira os dados descobertos (Letra, Posicao) (0 para letra invalida): ")
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
               if(awnser[index]==letter or letter in contains):
                    do = False
          
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
               if(checkExcluded(word)):
                    if(checkContains(word)):
                         if(checkExact(word)):
                              print(word)

mainLoop()