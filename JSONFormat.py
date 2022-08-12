from seleniumwire import webdriver
import random
import time
##################################################################
##################################################################
##################################################################
# Your Keyword List
kws = ["webscraping", "bitcoin", "chicken"]

# Limit scraped Questions ||| 0 == All Possible
limit = 15

##################################################################
##################################################################
##################################################################
##### FUNCTIONS
def clickyThingyXpath(xpath, wait, timeout, desc):
    startTime = time.time()
    time.sleep(wait)
    while True:
        checkTime = time.time() - timeout

        if startTime < checkTime:
            return(False)
        try:
            driver.find_element("xpath", xpath).click()
            return(True)
        except:
            time.sleep(1)
            pass

def findTexts(xpath, sleep):
    time.sleep(sleep)
    texts = list()
    _texts = driver.find_elements("xpath",xpath)
    for t in _texts:
        if len(t.text) > 5:
            texts.append(t.text)
    return(texts)

def findQuesionID(questions):
    _id = driver.find_element("xpath", '//*[text() = "'+questions+'"]/parent::*/parent::*/parent::*/parent::*/parent::*').get_attribute("id")
    return(_id)   

def XPathByQuestionID(_id):
    xpath = '//*[@id="'+_id+'"]/div/div/div[1]/div[4]'
    return(xpath)

def XPathByAnswerID(_id):
    clicky = '//*[@id="'+_id+'"]//*[@data-attrid="wa:/description"]'
    return(clicky)

def handleAnswerList(_id):
    _dict = dict()

    _dict["heading"] = findTexts('//*[@id="'+_id+'"]//*[@role="heading"]',0)
    findList = findTexts('//*[@id="'+_id+'"]//li',0)
    if len(findList) > 0:
        _dict["list"] = findList
        _dict["anwerType"] = "list"
        return(_dict)
    else:
        return(None)

def doWhateverYouWandwithThe(results):
    import json
    with open("results.json", "w") as jsonFile:
        json.dump(results, jsonFile, indent=4)

##################################################################
##################################################################
##################################################################
##### Script

results = dict()
for kw in kws:
    results[kw] = dict()
    ### Setting Up Webdriver
    ua = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"]
    options = webdriver.ChromeOptions()
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-application-cache")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--user-agent='+random.choice(ua))
    driver = webdriver.Chrome(executable_path=r"C:\Selenium\chromedriver.exe", chrome_options=options)

    ### Request
    url = 'https://www.google.com/search?q='+kw+'&start=0'
    driver.get(url)

    ### Click on Privacy Stuff - Optional
    # clickyThingyXpath("/html/body/div[3]/div[3]/span/div/div/div/div[3]/div[1]/button[1]/div", 1, 60, "Handling Privacy Popup")

    ### Scraping
    seen = list()
    questions = findTexts("//*[@data-q]//div[@role='button']//div/span", 0)
    i = 0
    while True:
        for q in questions:
            try:
                # Preparing result dict
                results[kw][str(i)] = {"question":{}, "answer":{}}
                # check if question done allready, since in loop
                if q in seen:
                    continue
                # Get the question ID for further xpath usage
                qid = findQuesionID(q)
                print(kw+" ||| "+q)
                 # Open question
                clickyThingyXpath(XPathByQuestionID(qid), 0, 10, 'Clicking Question: "'+q+'"')
                # Scrape answer
                answer = findTexts(XPathByAnswerID(qid), 2)
                # check if answer is text only
                if len(answer) == 1:
                    anwerType = "Text"
                    while answer[0] == "":
                        answer = findTexts(XPathByAnswerID(qid), 2)
                    # Add to result dict
                    results[kw][str(i)]["question"] = q
                    results[kw][str(i)]["answer"]["answerType"] = "text"
                    results[kw][str(i)]["answer"]["answer"] = answer
                else:
                    # Not Text, so handle as list
                    answer = handleAnswerList(qid)
                    # Ignore if it's not a List as well
                    if answer == None:
                        seen.append(q)
                        continue
                    # Add to result dict
                    results[kw][str(i)]["question"] = q
                    results[kw][str(i)]["answer"] = answer
                seen.append(q)
                i+=1
                if i == limit:
                    break
            except:
                seen.append(q)
                continue
        if i == limit:
            break
        ### Did more questions pop up?
        _questions = findTexts("//*[@data-q]//div[@role='button']//div/span", 0)
        if len(questions) == len(_questions):
            break
        questions = _questions

    driver.close()

doWhateverYouWandwithThe(results)