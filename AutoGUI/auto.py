from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep


import sys
import os

sys.path.append(os.path.abspath("/home/joao/Desktop/TermoSolver"))

from main import getInfo

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


driver = webdriver.Firefox()
driver.get("https://term.ooo/")

WebDriverWait(driver, 10).until(
    EC.title_is("Termo")
)

webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

row = 0
word = 'odeia'

while (row < 6):
    response = []
    position = 0

    webdriver.ActionChains(driver).send_keys(word).perform()
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
            response.append("{},{}".format((line.text).lower(), position))
        elif (color == 'yellow'):
            response.append("{},{}".format(
                (line.text).lower(), -abs(position)))
        else:
            response.append("{},{}".format((line.text).lower(), 0))

    print(*response)
    row += 1

    sleep(1)

driver.close()
