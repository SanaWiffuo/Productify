import requests 
from classes import Product,Lazada
from bs4 import BeautifulSoup as soup
import json
import pandas as pd
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import queue
from threading import Thread
#lazada
def func1(results,queue):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('start-maximized') 
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    browser = webdriver.Chrome(options=options)
    aList = []


    for i in range(0,5):
        browser.get("{}".format(results[i].url))
        ratings = browser.find_elements_by_class_name('score-average')
        ratings_count = browser.find_elements_by_class_name('count')
        num_of_ratings = [i for i in ratings_count[0].text if i.isdigit()==True]
        results[i].ratings = ratings[0].text+"("+"".join(num_of_ratings)+")"
        print("l-func1 " + results[i].ratings)
        aList.append(results[i])

        
    browser.quit()
    queue.put(aList)
    return results

def func2(results,queue):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('start-maximized') 
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    browser = webdriver.Chrome(options=options)
    aList = []
    

        
    for i in range(5,10):
        browser.get("{}".format(results[i].url))
        ratings = browser.find_elements_by_class_name('score-average')
        ratings_count = browser.find_elements_by_class_name('count')
        num_of_ratings = [i for i in ratings_count[0].text if i.isdigit()==True]
        results[i].ratings = ratings[0].text+"("+"".join(num_of_ratings)+")"
        print("l-func2 " + results[i].ratings)
        aList.append(results[i])
       
        
    browser.quit()
    queue.put(aList)
    return results


def scrape(search_item,total_of_result):
    my_url = "https://www.lazada.sg/catalog/?q={}".format(search_item)

    ua = UserAgent()
    userAgent = ua.random
    headers = {
        'User-Agent': userAgent,
        'Referer': "https://www.lazada.sg"
        }

    ret = requests.get(my_url,headers=headers)
    page_soup = soup(ret.text, 'lxml')
    data = page_soup.select("[type='application/ld+json']")[1]
    oJson = json.loads(data.text)["itemListElement"]
    results = []

    for product in oJson:
        results.append(Lazada(product['name'],"$"+product['offers']['price'],"",product['url'], product['image']))
        if len(results)==total_of_result:
            break
    df = pd.DataFrame([t.__dict__ for t in results])
    print(df)
    return results


# def scrap_lazada(search_item, total_of_result,queue):
#     lst = scrape(search_item, total_of_result)

#     l1 = Thread(target=func1 ,args=(lst,queue))
#     l1.start()
#     l2 = Thread(target=func2,args=(lst,queue))
#     l2.start()
#     # l3 = Thread(target=func3 ,args=(lst,queue))
#     # l3.start()
#     # l4 = Thread(target=func4,args=(lst,queue))
#     # l4.start()
    
#     result = queue.get()
#     l1.join()
#     l2.join()
#     result += queue.get()
#     # l3.join()
#     # result += queue.get()
#     # l4.join()
#     # result += queue.get()
#     # over.put(result)
#     return result

if __name__ == "__main__":
    lst = scrape("monitor",20)
    df = pd.DataFrame([t.__dict__ for t in lst])
    print(df)
