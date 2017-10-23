# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 10:04:32 2017

@author: BLK
"""
url="https://instagram.com"
#from bs4 import BeautifulSoup
#import requests
#from robobrowser import RoboBrowser'
from selenium import webdriver
import time
import json
import random
def getLoginUser():
    userName = input("Type Username:")
    return userName
def getLoginPassword():
    password = input("Type Password:")
    return password
userName = getLoginUser()
password = getLoginPassword()
    


tags=["brød","surdeig","baking", "sourdough"]
tag=tags[-1]
##def openBrowser(webDriver):
#    """takes one arg.
#    determins what webdriver to use
#    eg. Chrome, PhantomJS ... Chrome is default
#    """
#    #return exec("webdriver." + webDriver + "()")

driver = webdriver.Chrome()
#driver.set_window_size(1024,700)
driver.get(url)

def importLogFiles(fileName):
    return json.load(open(fileName+".txt","r"))
    
    
    
total = 0
nxtPress= 0
if sum(importLogFiles("likeNames").values()) > 0:
    likeNames = importLogFiles("likeNames")
likeNames={}
if len(importLogFiles("likeNames")) > 0:
    likeNames = importLogFiles("likeNames")
tagLikes={}
if len(importLogFiles("tagLikes")) > 0:
    tagLikes = json.load(open("tagLikes.txt","r"))
    

total = sum(likeNames.values())



def login():
    element= driver.find_element_by_class_name("_b93kq")
    eloc= element.location_once_scrolled_into_view
    xval= eloc['x']
    yval= eloc['y']
    script= "window.scrollTo("+str(xval)+","+str(yval)+");"
    driver.execute_script(script)
    
    
    element.click()
    user=driver.find_element_by_name("username")
    
    user.send_keys(userName)
    passW=driver.find_element_by_name("password")
    passW.send_keys(password)
    loginbutton=driver.find_element_by_css_selector("button")
    loginbutton.click()
    time.sleep(3)
    while len(driver.find_elements_by_name("verificationCode")) > 0:
        sec = driver.find_element_by_name("verificationCode")
        sec.click()
        keys = input("tast inn kode")
        sec.send_keys(keys)    
        sec.submit()
        time.sleep(3)


def openTag(tag =tag):
    tag=tag
#    from selenium.webdriver.common.by import By
#    from selenium.webdriver.support.ui import WebDriverWait
#    from selenium.webdriver.support import expected_conditions as EC  
    
    driver.get(url+"/explore/tags/"+tag)
    time.sleep(3)
    
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[1]')
    pic= driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[1]')
    plocX=pic.location_once_scrolled_into_view['x'] 
    plocY=pic.location_once_scrolled_into_view['y']
    script= "window.scrollTo("+str(plocX)+","+str(plocY)+");"
    driver.execute_script(script)
    pic.click()
#    driver.find_element_by_id("react-root").click()
#    driver.find_element_by_class_name("_e3il2").click()
    
#    
def liker(total = total, nxtPress = nxtPress):

    tottemp= total
    nxtpresstemp = nxtPress
    runs= 0
    while tottemp - total < random.randrange(20, 30):
        name = driver.find_element_by_class_name("_eeohz").text
        print(name)
        print("likes:", tottemp - total)
        print("next press:", nxtpresstemp - nxtPress)
        
        #driver.find_element_by_class_name("_si7dy").click()
        like=driver.find_element_by_xpath("//span[contains(@class,'coreSpriteHeart')]").text
        heart = driver.find_element_by_xpath("//span[contains(@class, 'coreSpriteHeart')]")
        nxt = driver.find_element_by_link_text("Next")
        if nxtpresstemp - tottemp > 150:
            break
        elif name.lower() != userName and like.lower() == "like":
            heart.click()
            likeNames.setdefault(name,0)
            likeNames[name] += 1
            tagLikes.setdefault(tag,0)
            tagLikes[tag]+=1
            tottemp += 1
            nxt.click()
            nxtpresstemp += 1
            time.sleep(random.randrange(2, 8))
        
        else:
            nxt.click()    
            nxtpresstemp += 1
            time.sleep(random.randrange(2, 8))
    
    total = tottemp
    nxtPress = nxtpresstemp
    print("Total likes:" , total,"\n","Total next", nxtPress)
    json.dump(likeNames, open("likeNames.txt",'w'))
    json.dump(tagLikes, open("tagLikes.txt",'w'))
    json.dump(total, open("total.txt",'w'))
    json.dump(nxtPress, open("nxtpress.txt",'w'))
#    for i in likeNames:
#        print(i,":", likeNames[i])
    runs += 1
    tSleep = random.randrange(600, 950)
    print("sleeping for", round(tSleep/60 ,1),"min")
    
    for i in range(tSleep):
        time.sleep(1)
    while runs < 4:
        if runs == 3:
            run= input("do you want to continue? Y/N")
            if run.lower() == "n":
                break
                
            else:
               print("resuming")
               run=0
        print("resuming")
        liker(total, nxtPress)
    



#    json.dump(likeNames, open("likeNames.txt",'w'))
#    json.dump(tagLikes, open("tagLikes.txt",'w'))
#    json.dump(total, open("total.txt",'w'))
#    json.dump(nxtPress, open("nxtpress.txt",'w'))
#
#
#
#
#test = json.load(open("tagLikes.txt","r"))
#
#
#


