from selenium import webdriver
from time import sleep
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import Input

class vdvScraping:

    def __init__(self,ChromeDriver_filepath):
        self.driver = webdriver.Chrome(ChromeDriver_filepath)    #Assign driver as an object for initiation of Webdriver.Chrome
        self.driver.maximize_window()                   #maximise Chrome browser window

    def log_in(self,domain,username,password):
        self.driver.get(domain)                  #Go to the login url
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, 'f_user'))).send_keys(username)     #Wait until the element of username entry visible then enter the username

        sleep(0.5)  # wait
        password_input = self.driver.find_element_by_id('f_pass')  # Assign element with password entry for password_input variable
        password_input.send_keys(password)  # input the password
        sleep(0.5)  # wait

        self.driver.find_element_by_xpath('//button[text()="Login"]').click()  # Click the login button
        sleep(5)  # wait

    def go_to_url(self,url):
        self.driver.get(url)         #Go to the url
        sleep(20)  # Wait

    def choosing_dates(self,day_type_from,date_from,day_type_to,date_to):
        self.driver.switch_to.frame("IDContentFrame")            #Switch to iFrame with id as "IDContentFrame"
        self.driver.find_element_by_xpath('//button[@class="btn btn-default scrollDate optionButton"]').click()  # click the calendar button

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//span[@class="input-group-addon  date_picker date_button"]'))).click()  # click the calendar button at the from section
        current_month_year = self.driver.find_element_by_xpath('//div[@class="datepicker datepicker-dropdown dropdown-menu"]//th[@class="switch"]')  # Get the element showing current month-year of the datepicker
        # current_month_year.text
        if date_from[3:] == current_month_year.text:  # Condition if the current month-year is the same as Input.Input_month_year variable
            pass  # Do nothing
        else:  # Condition if the current month-year is not the same as Input.Input_month_year
            self.driver.find_element_by_xpath('//div[@class="datepicker datepicker-dropdown dropdown-menu"]//th[@class="switch"]').click()  # Click the month-year button of calendar-from section

        month_elements = self.driver.find_elements_by_xpath('//div[@class="datepicker-months"]//span[@class="month"]')  # Get element containing months assigning it to month_elements
        for month_element in month_elements:  # loop for each month_element
            if date_from[3:6] == month_element.text:  # Conditional for checking suitable month
                month_element.click()  # Click the valid month
                break

        list_of_days_from = self.driver.find_elements_by_xpath('//div[@class="datepicker-days"]//tr/td[@class=%s]' % day_type_from)  # Assign list_of_days_from as an identifier for list of xpath with days in the chosen month based on the from calendar
        for day in list_of_days_from:  # loop for checking suitable day in "from" calendar
            if date_from[0] == "0" and day.text == date_from[1]:        #Conditional for 1 digit day number
                day.click()  # Click the suitable day Index
                break  # break the loop
            elif date_from[0] != "0" and day.text == date_from[:2]:  # Conditional for choosing day index in "to" calendar and 2 digits day number
                day.click()  # Click the suitable day Index
                break  # break the loop

        self.driver.find_element_by_id('stop_button').click()  # click the calendar button at the to section
        current_month_year = self.driver.find_element_by_xpath('//div[@class="datepicker datepicker-dropdown dropdown-menu"]//th[@class="switch"]')  # Get the element showing current month-year of the datepicker
        # current_month_year.text
        if date_to[3:] == current_month_year.text:  # Condition if the current month-year is the same as Input.Input_month_year variable
            pass  # Do nothing
        else:  # Condition if the current month-year is not the same as Input.Input_month_year
            self.driver.find_element_by_xpath('//div[@class="datepicker datepicker-dropdown dropdown-menu"]//th[@class="switch"]').click()  # Click the month-year button of calendar-to section

            month_elements = self.driver.find_elements_by_xpath('//div[@class="datepicker-months"]//span[@class="month"]')  # Get element containing months assigning it to month_elements
            for month_element in month_elements:  # loop for each month_element
                if date_to[3:6] == month_element.text:  # Conditional for checking suitable month
                    month_element.click()  # Click the valid month
                    break                   #break the loop

        list_of_days_to = self.driver.find_elements_by_xpath('//div[@class="datepicker-days"]//tr/td[@class=%s]' % day_type_to)  # Assign list_of_days_to as the identifier for list of xpath with days in the chosen month based on the to calendar
        for day in list_of_days_to:  # loop for checking suitable day in "to" calendar
            if date_to[0] == "0" and day.text == date_to[1]:            #Conditional for 1 digit day number
                day.click()  # Click the suitable day Index
                break  # break the loop
            elif date_to[0] != "0" and day.text == date_to[:2]:  # Conditional for choosing day index in "to" calendar and 2 digits day number
                day.click()  # Click the suitable day Index
                break       #break the loop

        self.driver.find_element_by_xpath('//button[@class="btn btn-default getHistoricalDataByDate"]').click()  # CLick the Get Data button
        sleep(10)  # Wait

    def taking_screenshot(self,image_name):
        self.driver.save_screenshot('images_before_cropping\\%s.png' % image_name)

    #def 


web_scraping = vdvScraping(Input.WebDriver_filepath)
web_scraping.log_in(Input.Domain,Input.username,Input.password)

with open(Input.parameters_for_cropping_filepath) as myfile:         #open parameters for cropping.txt
    csv_reader=csv.reader(myfile,delimiter=",")             #Assign csv_reader as an object of csv.reader
    lines=myfile.readlines()                                #Assign lines as list of content in parameters for cropping

strip_lines=[]                                              #Assign strip_lines as a blank list
for line in lines:                                          #loop for processing lines identifier
    line=line.strip()                                       #Strip off \n in line
    strip_lines.append(line)                                #Append line to strip_lines

for line in strip_lines:                                    #loop for getting images
    line_list = line.split(",")                             #Assign line_list as a list after splitting "," in line
    web_scraping.go_to_url(line_list[0])
    web_scraping.choosing_dates(Input.day_type_from,Input.date_from,Input.day_type_to,Input.date_to)
    web_scraping.taking_screenshot(line_list[2])

