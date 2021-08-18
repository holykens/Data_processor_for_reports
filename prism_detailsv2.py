from selenium import webdriver
from time import sleep
from scrapy.selector import Selector
import Input
import csv
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas

with open("urls.txt", "r") as myfile:           #Open urls.txt
    lines = myfile.readlines()                  #Assign lines as list of content in urls.txt    

strip_lines=[]                                  #Assign strip_lines as an empty list    
for line in lines:                              #loop for processing lines
    line=line.strip()                           #strip off \n
    line_list=line.split(",")                   #Assign line_list as placeholder after split
    strip_lines.append(line_list)               #append line_list to strip_lines

Site_url = strip_lines[0][1]                    #Assign Site_url as the first url in urls.txt
url_regex = re.compile(r'(.com/){1}')           #Assign url_regex as an object with ".com/" regular expression
match = url_regex.search(Site_url)              #Assign match as an object with search method of url_regex applied to Site_url
Domain = Site_url[:match.span(0)[1]]            #Assign Domain as the domain url - Site_url[:match.span(0)[1]] returns the domain url

driver = webdriver.Chrome("D:\Softwares\chromedriver_win32\chromedriver.exe")           #Assign driver as the initiation for webdriver.Chrome 
driver.maximize_window()                                            #Maximize window            
driver.get(Domain)                        #open the url for logging in
                                             #Wait

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'f_user'))).send_keys(Input.username)      #Wait until the username login visible then enter the username
password_input = driver.find_element_by_id('f_pass')        #Assign element with password entry for password_input variable
password_input.send_keys(Input.password)                    #input the password
sleep(0.5)                                                  #wait

driver.find_element_by_xpath('//button[text()="Login"]').click()        #Click the login button
sleep(8)                            

for line in strip_lines:

    myfile = open(line[0]+".txt", "w")                               #Create an object to open result_file in writing mode
    writer = csv.writer(myfile, lineterminator = '\n')                  #Create writer object with argument lineterminator = '\n' to avoid skipping lines when writing
    writer.writerow(['#', 'Header name', 'Alias name', "Variable ID"])      #Write the header row

    driver.get(line[1])                      #open the url to scrape prisms details
    sleep(8)                                        #wait
    
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody")))
    
    sel = Selector(text=driver.page_source)         #Create a Selector object
    table=sel.xpath('//tbody')                      #Assign table variable with the corresponding xpath
    trs=table.xpath('.//tr')                        #Assign trs as the xpaths of table rows    

    for tr in trs:                                  #loop for each table row to scrape data    
        print(tr)
        ID_number = tr.xpath('.//td[1]/text()').extract_first()         #Assign ID_number variable for extracting # in table
        Header_name = tr.xpath('.//td[2]/text()').extract_first()       #Assign Header_name variable for extracting Header name in table
        Alias_name = tr.xpath('.//td/p/text()').extract_first()         #Assign Alias_name variable for extracting Alias name in table
        Variable_ID = "$" + tr.xpath('.//td/p/following-sibling::input[@type="hidden"]/@value').extract_first() + "$"       #Assign Variable_ID for extracting Variable ID with leading and trailing $

        writer.writerow([ID_number, Header_name, Alias_name, Variable_ID])      #write the output to csv file after scraping

    myfile.close()                              #Close the output file

    df=pandas.read_csv(line[0]+".txt")                  #read file in panda mode
    df1 = df[df["Header name"].apply(lambda x : ("MPO" in x) and ("relatif" in x))]             #Filter variables with zRelatif
    df1["Modified_prism_name"]=df1["Header name"].str.extract(r"([XYZ]+)") + df1["Header name"].str.extract(r"MPO(\d\d\d)")     #Create a new column with [XYZ](/d/d/d)
    df1.to_csv(f'sorted {line[0]}.csv', index = False)                   #Write the dataframe to csv file