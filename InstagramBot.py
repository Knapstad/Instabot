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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import random
import pickle



def getLoginUser():
    userName = input("Type Username:")
    return userName
def getLoginPassword():
    password = input("Type Password:")
    return password
def loadCookies():
    """loads saved Cookies from file"""
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("cookies loaded")
    except FileNotFoundError:
        print("no cookies found")
    
        
def saveCookies():
    """Saves cookies to file"""
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    
def importLogFiles(fileName):
    """ Takes one argument 'filename' and loads that file"""
    return json.load(open(fileName+".txt","r"))

userName = getLoginUser()
password = getLoginPassword()
    


tags=["brød","surdeig","baking", "sourdough", "realbread","artisanbread","matprat","nrkmat","bread"]
tag=tags[random.randrange(0,len(tags)-1)]
##def openBrowser(webDriver):
#    """takes one arg.
#    determins what webdriver to use
#    eg. Chrome, PhantomJS ... Chrome is default
#    """
#    #return exec("webdriver." + webDriver + "()")

#driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(chrome_options=options)
       

#driver.set_window_size(1024,700)
driver.get(url)
loadCookies()
driver.refresh()




    
    
runs= 0
total = 0
if importLogFiles("total") > 0:
    total = importLogFiles("total")

nxtPress= 0
if importLogFiles("nxtpress") > 0:
    nxtPress= importLogFiles("nxtpress")


likeNames={}
if len(importLogFiles("likeNames")) > 0:
    likeNames = importLogFiles("likeNames")

tagLikes={}
if len(importLogFiles("tagLikes")) > 0:
    tagLikes = json.load(open("tagLikes.txt","r"))
    







def login():
    element= driver.find_element_by_class_name("_b93kq")
    #print(driver.page_source)
    
    
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
    while len(driver.find_elements_by_id("slfErrorAlert")) > 0:
        driver.refresh()






def openTag(tag = tag):
    """Opens the tag page and finds the first window
    """
    
#    from selenium.webdriver.common.by import By
#    from selenium.webdriver.support.ui import WebDriverWait
#    from selenium.webdriver.support import expected_conditions as EC  
    print("opening tag:", tag)
    driver.get(url+"/explore/tags/"+tag)
    time.sleep(3)
    print("opened", driver.current_url)
    time.sleep(3)
   # driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[1]')
    pic= driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[1]')
    plocX=pic.location_once_scrolled_into_view['x'] 
    plocY=pic.location_once_scrolled_into_view['y']
    script= "window.scrollTo("+str(plocX)+","+str(plocY)+");"
    driver.execute_script(script)
    pic.click()
#    driver.find_element_by_id("react-root").click()
#    driver.find_element_by_class_name("_e3il2").click()
    
#    
def liker( runs = runs, thisrunlikes = 0, numberofruns = 3, tag=tag):
    global total
    global nxtPress
    thisrunlikes=thisrunlikes
    runs=runs
    tottemp= total
    nxtpresstemp = nxtPress
    while tottemp - total < random.randrange(20, 60):
        driver.implicitly_wait(2)
        name = driver.find_element_by_class_name("_eeohz").text
        print(name)
        print("likes:", tottemp - total)
        print("next press:", nxtpresstemp - nxtPress)
        
        #driver.find_element_by_class_name("_si7dy").click()
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@class,'coreSpriteHeart')]")))
        like=driver.find_element_by_xpath("//span[contains(@class,'coreSpriteHeart')]").text
               
        heart = driver.find_element_by_xpath("//span[contains(@class, 'coreSpriteHeart')]")
        nxt = driver.find_element_by_link_text("Next")
        if (nxtpresstemp-nxtPress)- (tottemp - total) > 150:
            break
        elif name.lower() != userName and like.lower() == "like":
            heart.click()
            likeNames.setdefault(name,0)
            likeNames[name] += 1
            tagLikes.setdefault(tag,0)
            tagLikes[tag]+=1
            tottemp += 1
            thisrunlikes+=1
            nxt.click()
            nxtpresstemp += 1
            time.sleep(random.randrange(2, 8))
        
        else:
            time.sleep(0.5)
            nxt.click()    
            nxtpresstemp += 1
            
    
    total = tottemp
    nxtPress = nxtpresstemp
    print("Total likes:" , total,"\n","Total next", nxtPress, "\n" , "runs: ", runs, "\n", "likes this run:", thisrunlikes )
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
    while runs < numberofruns +1 :
#        print("check while", runs , "< 4")
        if runs == numberofruns:
#            print("runs == 3", runs)
            run= input("do you want to continue? Y/N/T")
            if run.lower() == "n":
                return("Aborted")
            elif run.lower()== "t":
                ntag=tags[random.randrange(0,len(tags)-1)]
                while ntag == tag:
                   ntag=tags[random.randrange(0,len(tags)-1)]
                tag=ntag       
                openTag(tag)
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_eeohz")))
                                
            else:
               runs=0
        elif runs == 4:
            ntag=tags[random.randrange(0,len(tags)-1)]
            while ntag == tag:
                   ntag=tags[random.randrange(0,len(tags)-1)]
            tag=ntag       
            openTag(tag)
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_eeohz")))
            
        print("resuming")
        liker(runs, thisrunlikes, numberofruns, tag)







#    json.dump(likeNames, open("likeNames.txt",'w'))
#    json.dump(tagLikes, open("tagLikes.txt",'w'))
#    json.dump(total, open("total.txt",'w'))
#    json.dump(nxtPress, open("nxtpress.txt",'w'))
#
#

#
#test = json.load(open("tagLikes.txt","r"))
#
#
#


