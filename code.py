from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
import csv


code="" #put your password
user="" # put your username

query='site:linkedin.com/in/ AND "python developer" AND "London"'
number_of_page_of_search_result=int(input()) #type how much search result page you want

options = Options()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"# it locates chrome app
driver=webdriver.Chrome(options=options,executable_path='C:\\Users\\<username_of_pc>\\Downloads\\chromedriver_win32\\chromedriver') #it locates chromedriver app

driver.get('https://www.linkedin.com')

username = driver.find_element_by_id('session_key')
username.send_keys(user)
sleep(0.5)

password = driver.find_element_by_id('session_password')
password.send_keys(code)
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click() #login to LinkedIn
sleep(0.5)

driver.get('https:www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q') #finding searchbox
search_query.send_keys(query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

all_linkedin_urls=[] #getting all the python developers link of uk from google after search.
for i in range(number_of_page_of_search_result):
	try:
		next_button=driver.find_element_by_xpath('//*[@id="pnnext"]')
		linkedin_urls = driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div/a')
		linkedin_urls = [url.get_attribute("href") for url in linkedin_urls]
		all_linkedin_urls.extend(linkedin_urls)
		next_button.click()
		sleep(0.5)

	except exceptions.NoSuchElementException:
		break

#xpath of these data which will be extracted
xpath_of_work='/html/body/div[8]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[2]/ul/li[1]/a/span'
xpath_of_educaion='/html/body/div[8]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[2]/ul/li[2]/a/span'
xpath_of_name='//*[@id="ember59"]/div[2]/div[2]/div[1]/ul[1]/li[1]'
xpath_of_profession= '//*[@id="ember59"]/div[2]/div[2]/div[1]/h2' 
xpath_of_location= '//*[@id="ember59"]/div[2]/div[2]/div[1]/ul[2]/li[1]'

#print(all_linkedin_urls)
with open("LinkedIn_Users.csv","w",newline="",encoding="utf-8") as file:
	writer=csv.DictWriter(file,fieldnames=["Name","Job Title","Address","Education","Company","URL"])
	writer.writeheader()

	for i in all_linkedin_urls:
		driver.get(i)
		sleep(1.2)
	
		try:
			name=driver.find_element_by_xpath(xpath_of_name).text
		except exceptions.NoSuchElementException:
			pass
		try:
			edu=driver.find_element_by_xpath(xpath_of_educaion).text
		except exceptions.NoSuchElementException:
			edu="Not Existed"
		try:
			company=driver.find_element_by_xpath(xpath_of_work).text
		except exceptions.NoSuchElementException:
			company="Not Existed"
		try:
			profession=driver.find_element_by_xpath(xpath_of_profession).text
		except exceptions.NoSuchElementException:
			profession="Not Existed"
		try:
			address=driver.find_element_by_xpath(xpath_of_location).text
		except exceptions.NoSuchElementException:
			address="Not Existed"
		writer.writerow({"Name":name,"Job Title":profession,"Address":address,"Education":edu,"Company":company,"URL":i})


driver.quit() #Done. Your file is ready.
