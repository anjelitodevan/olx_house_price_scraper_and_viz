import csv
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
import time

# use edge
options= EdgeOptions()
options.use_chromium= True
driver= Edge(options= options, executable_path= "C:\Additional Packages\edgedriver_win64\msedgedriver.exe")

# create url builder function
def get_url(loc_term, search_term):
    """Generate URL from search term"""
    template= "https://www.olx.co.id/{}/properti_c88/q-{}"
    search_term= search_term.replace(" ", "-")
    return template.format(loc_term, search_term)

# create record extractor
def extract_record(item):
    """Extract and return data from a single record"""
    try:
        product= item.find("span", {"data-aut-id": "itemTitle"}).text
        price= item.find("span", {"data-aut-id": "itemPrice"}).text
        location= item.find("span", {"data-aut-id": "item-location"}).text
        spec= item.find("span", {"data-aut-id": "itemDetails"}).text
        result= (product, price, location, spec)
        return(result)
    except:
        pass    

# create function to click next page
def click_next_page(n):
    """Click next page n number of times"""
    list= range(n)
    for i in list:
        try:
            next_button = driver.find_element(By.CLASS_NAME, "JbJAl")
            next_button.click()
            time.sleep(3)
        except:
            pass


list_place_to_crawl= [
    # "jakarta-dki_g2000007",
    # "bandung-kota_g4000018",
    # "yogyakarta-kota_g4000072",
    # "medan-kota_g4000131",
    # "surabaya-kota_g4000216", 
    # "bekasi-kota_g4000020", 
    # "tangerang-kota_g4000079", 
    # "palembang-kota_g4000368",
    # "semarang-kota_g4000065",
    # "makassar-kota_g4000307",
    # "depok-kota_g4000024", 
    # "batam-kota_g4000406",
    # "temanggung-kab_g4000059",
    "demak-kab_g4000040",
    "boyolali-kab_g4000037",
    "kudus-kab_g4000047",
    # "magelang-kota_g4000062",
    "klaten-kab_g4000046",
    "purworejo-kab_g4000053",
    "balikpapan-kota_g4000250",
    "sragen-kab_g4000056"
]

for city in list_place_to_crawl:
    
    # open url in browser and grab
    url= get_url(city, "rumah")
    driver.get(url)

    # load next page
    click_next_page(250)

    soup= BeautifulSoup(driver.page_source, "html.parser")

    records= []
    results= soup.find_all("div", {"class": "IKo3_"})

    for item in results:
        record= extract_record(item)
        if record:  
            records.append(extract_record(item))

    # append result to csv
    with open("result.csv", "a", newline= "", encoding= "utf-8") as f:
        writer= csv.writer(f)
        writer.writerows(records)

driver.close()

print("Task finished.")