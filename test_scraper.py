import csv
from selenium import webdriver
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_driver(url):
    options = webdriver.ChromeOptions() 
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.set_window_position(-10000,0)
    driver.get(url)
    time.sleep(5)
    return driver

driver = get_driver('https://www.tokopedia.com/p/handphone-tablet')
max = 100
while 1:
    elements = driver.find_elements_by_xpath("//div[contains(@class, 'pcv3__container')]")
    for e in elements:
        driver.execute_script("arguments[0].scrollIntoView();", e)
    n = len(elements)
    if n >= max*2:
        break

result = []
count = 0
for e in elements:
    complete_info = {}
    product_content = e.find_element_by_xpath(".//a[contains(@class, 'pcv3__info-content')]")
    
    if product_content:
        product_content = str(product_content.text).splitlines()
        if len(product_content) == 7:
            complete_info.update({
                    "name":product_content[0],
                    "rating":product_content[5]
                })
        elif len(product_content) == 8:
            complete_info.update({
                    "name":product_content[1],
                    "rating":product_content[6]
                })
        else:
            continue
    
    price = e.find_element_by_xpath(".//div[contains(@data-testid, 'linkProductPrice')]")
    if price:
        complete_info.update({"price":price.text})
    
    img = e.find_element_by_xpath(".//img[contains(@class, 'success fade')]")
    if img:
        complete_info.update({"img":img.get_attribute("src")})
    url = e.find_element_by_tag_name('a')
    if url:
        complete_info.update({"url":url.get_attribute("href")})
        driver2 = get_driver(complete_info["url"])
        edesc = driver2.find_element_by_xpath("//div[contains(@data-testid, 'lblPDPDescriptionProduk')]")
        emerchant = driver2.find_element_by_xpath("//a[contains(@data-testid, 'llbPDPFooterShopName')]")
        if edesc:
            complete_info.update({"desc":edesc.text.replace('\n',' ')})
        if emerchant:
            emerchant = emerchant.find_element_by_tag_name('h2')
            if emerchant:
                complete_info.update({"merchant":emerchant.text})
        driver2.close()
        driver2.quit()

    if complete_info:        
        result.append(complete_info)
    
    count += 1
    if count >= max:
        break

driver.close()
driver.quit()

delimiter=';'
with open('result.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Name of Product','Description','Image Link','Price','Rating (out of 5 stars)','Name of store or merchant'])
    for r in result:
        writer.writerow([r.get('name'),r.get('desc'),r.get('img'),r.get('price'),r.get('rating'),r.get('merchant')])
            

