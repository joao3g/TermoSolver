# -*- coding: utf-8 -*-
from array import array
import re
import os

file = open(os.path.abspath("/home/joao/Desktop/TermoSolver/words_pt-br_five_letters.txt"), 'r')
words = file.readlines()

excluded = []
contains = {}
awnser = {0: '', 1: '', 2: '', 3: '', 4: ''}
exclusiveOne = []
TwoOrMore = []

def checkExcluded(word):
    for letter in excluded:
        result = word.find(letter)
        if (result > -1):
            return False
    return True

def checkContains(word):
    for letter in contains:
        if (word.find(letter) == -1):
            return False

        occurrences = [m.start() for m in re.finditer(letter, word)]

        for i in occurrences:
            for j in contains[letter]:
                if (j == i):
                    return False

    return True

def checkExact(word):
    for index in awnser:
        if (awnser[index] != ''):
            if (awnser[index] != word[index]):
                return False
    return True

def checkTwoMore(word):
    for letter in TwoOrMore:
        if (word.count(letter) < 2):
            return False
    return True

def checkExclusivelyOne(word):
    for letter in exclusiveOne:
        if (word.count(letter) != 1):
            return False
    return True

def InsertWord(letters: array, positions: array):
    # Letters is an array with the letters of word
    # Positions is an array with the position of this letters\

    word = {}

    for i in range(len(letters)):
        letter = letters[i]
        position = positions[i]

        word[position] = letter

        do = True

        # Impede de remover letra já inserida
        for index in awnser:
            if (awnser[index] == letter and position == 0):
                do = False
                exclusiveOne.append(letter)

        for index in contains:
            if (index == letter and position == 0):
                do = False

        if (do):
            if (position > 0):
                awnser[(position-1)] = letter

                if letter in excluded:
                    excluded.remove(letter)

            elif (position < 0):
                if (letter in contains):
                    contains[letter].append((abs(position)-1))
                else:
                    contains[letter] = [(abs(position)-1)]
            else:
                excluded.append(letter)

    for position in word:
        letter = word[position]
        if (position < 0):
            for i in word:
                if (letter == word[i] and i > 0):
                    TwoOrMore.append(letter)


def getInfo():
    word = {}

    data = input(
        "Insira os dados descobertos (Letra, Posicao) (0 para letra invalida): ")

    if data == 0:
        exit()
        
    dataArray = data.split(" ")

    for info in dataArray:
        infoArray = info.split(",")
        do = True

        letter = infoArray[0]
        position = int(infoArray[1])
        word[position] = letter

        # Impede de remover letra já inserida
        for index in awnser:
            if (awnser[index] == letter and position == 0):
                do = False
                exclusiveOne.append(letter)

        for index in contains:
            if (index == letter and position == 0):
                do = False

        if (do):
            if (position > 0):
                awnser[(position-1)] = letter

                if letter in excluded:
                    excluded.remove(letter)

            elif (position < 0):
                if (letter in contains):
                    contains[letter].append((abs(position)-1))
                else:
                    contains[letter] = [(abs(position)-1)]
            else:
                excluded.append(letter)

    for position in word:
        letter = word[position]
        if (position < 0):
            for i in word:
                if (letter == word[i] and i > 0):
                    TwoOrMore.append(letter)

def mainLoop():

    while True:
        response = open('res.txt', 'w')
        count = 0

        getInfo()

        for word in words:
            if (checkExcluded(word) and checkContains(word) and checkExact(word) and checkExclusivelyOne(word) and checkTwoMore(word)):
                response.write(word)
                count += 1

        print("Quantidade de possiveis respostas:", count)

        print(excluded)
        print(awnser)
        print(contains)
        print(exclusiveOne)
        print(TwoOrMore)

        response.close()


if (__name__ == "__main__"):
    mainLoop()
