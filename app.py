__author__ = "Sonic"
from selenium import webdriver
import time
import urllib.request
import os
import cv2
import random
import numpy



browser = webdriver.Chrome()

def LoginTraffiset():
    browser.get('http://www.traffiset.ir/user/?appdata=login')
    username = browser.find_element_by_name('username')
    password = browser.find_element_by_name('password')
    username.send_keys("soroush.nasiri3@yahoo.com")
    password.send_keys("soroush39")

    browser.find_element_by_id("submitBtnmapploginform").click()



def Chooser():
    browser.get('http://traffiset.ir/websites')
    time.sleep(5)
    while(True):
        try:
            browser.find_element_by_tag_name("strong").click()
            time.sleep(7)
            checkState = browser.find_elements_by_id("checkifhumancountdown")
            if(len(checkState) == 0):
                Chooser()
            waiter = int(str(checkState[0].text).split(":")[1])
            time.sleep(waiter+3)
            CheckIfHuman()
            browser.get('http://traffiset.ir/websites')
        except:
            browser.get('http://traffiset.ir/websites')
            continue
            
            #browser.find_element_by_id("checkifhumanquiz").click()
           
def CheckIfHuman():
    divParent = browser.find_element_by_id("checkifhumanquiz") 
    img = divParent.find_element_by_tag_name("img")   
    imgSrc = img.get_attribute('src') 
    if(not os.path.exists("Images")):
        os.mkdir("Images")
    urllib.request.urlretrieve(imgSrc, "Images/temp.png")
    files = [f for f in os.listdir('Images') if ".png"  in f and "temp" not in f ]
    stream1 = open("Images/temp.png", "rb")
    bytes1 = bytearray(stream1.read())
    numpyarray1 = numpy.asarray(bytes1, dtype=numpy.uint8)
    dlImage = cv2.imdecode(numpyarray1, cv2.IMREAD_UNCHANGED)
    stream1.close()
    hasSame = ""
    if(len(files) > 0):
        for f in range(len(files) - 1):
            path = "Images/{}".format(str(files[f]))
            stream2 = open(path, "rb")
            bytes2 = bytearray(stream2.read())
            numpyarray2 = numpy.asarray(bytes2, dtype=numpy.uint8)
            srcImage = cv2.imdecode(numpyarray2, cv2.IMREAD_UNCHANGED)
            stream2.close()
            if(srcImage is not None):
                value = (dlImage == srcImage)
                if(not False in value):
                    hasSame = path
                    break

    if(hasSame != "" and not "temp" in hasSame):
        fileName = hasSame.replace(".png","").replace("Images/","")
        anchor = divParent.find_element_by_xpath("//a[contains(text(), '{}')]".format(fileName))
        anchor.click()
    else:
        os.rename("Images/temp.png","Images/temp{}.png".format(str(random.randrange(20, 50, 3))))
        anchor = divParent.find_element_by_tag_name("a")
        anchor.click()

while(True):
    try:
        LoginTraffiset()
        Chooser()
    except:
        continue
