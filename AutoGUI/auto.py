#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from unidecode import unidecode

from datetime import datetime

from time import sleep
from time import time

import random

import sys
import os

sys.path.append(os.path.abspath("/home/joao/Desktop/TermoSolver"))

import main

class element_has_no_empty_class(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        # Finding the referenced element
        element = self.locator
        if "empty" in element.get_attribute("class"):
            return False
        else:
            return element

for i in range(int(sys.argv[1])):
    t0 = time()
    try:

        driver = webdriver.Firefox()
        driver.get("https://term.ooo/")

        WebDriverWait(driver, 10).until(
            EC.title_is("Termo")
        )

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        main.excluded = []
        main.contains = {}
        main.awnser = {0: '', 1: '', 2: '', 3: '', 4: ''}
        main.exclusiveOne = []
        main.TwoOrMore = []

        row = 0
        choice = 'vasco'

        print(choice)

        while (row < 6):
            letters = []
            positions = []

            position = 0

            webdriver.ActionChains(driver).send_keys(choice).perform()
            webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()

            while (position < 5):

                line = driver.execute_script("""return document.querySelector('wc-board').shadowRoot.querySelector("wc-row[termo-row='{}']").
                                        shadowRoot.querySelector("div[termo-pos='{}']")""".format(row, position))

                WebDriverWait(driver, 10).until(
                    element_has_no_empty_class(line)
                )

                position += 1

                if ("wrong" in line.get_attribute("class")):
                    color = 'black'
                elif ("right" in line.get_attribute("class")):
                    color = 'green'
                else:
                    color = 'yellow'

                if (color == 'green'):
                    letters.append(unidecode((line.text)).lower())
                    positions.append(position)
                elif (color == 'yellow'):
                    letters.append(unidecode((line.text)).lower())
                    positions.append(-abs(position))
                else:
                    letters.append(unidecode((line.text)).lower())
                    positions.append(0)

            # Check if the awnser is correctly
            positives = 0

            for i in positions:
                if(i>0): positives += 1
            
            if(positives == len(positions)): break
                
            # Starts to use the 'main code'

            main.InsertWord(letters, positions)

            solution = []

            for word in main.words:
                if (main.checkExcluded(word) and main.checkContains(word) and main.checkExact(word) and main.checkExclusivelyOne(word) and main.checkTwoMore(word)):
                    solution.append(unidecode(word[0:5]))

            print("Quantidade de possiveis respostas: {}\n".format(len(solution)))
            choice = random.choice(solution)
            print(choice)

            row += 1

            sleep(1)

        #sleep(2)

        now = datetime.now()

        current_time = now.strftime("%H-%M-%S")
        folder_name = now.strftime("%d-%m")

        
        if(row == 6): 
            try:
                os.mkdir("Screenshots/Error/{}".format(folder_name))
            finally:
                driver.save_screenshot('Screenshots/Error/{}/{}.png'.format(folder_name, current_time))

        else: 
            try:
                os.mkdir("Screenshots/Success/{}".format(folder_name))
            finally:
                driver.save_screenshot('Screenshots/Success/{}/{}.png'.format(folder_name, current_time))

        driver.close()

        print(time()-t0)


    except:
        now = datetime.now()

        current_time = now.strftime("%H-%M-%S")
        folder_name = now.strftime("%d-%m")

        try:
            os.mkdir("Screenshots/Failure/{}".format(folder_name))
        finally:
            driver.save_screenshot('Screenshots/Failure/{}/{}.png'.format(folder_name, current_time))

        driver.close()

        print(time()-t0)
        

