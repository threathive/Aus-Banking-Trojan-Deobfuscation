# Author: Terry Skliros

__version__ 	= "1.0"

import requests
import datetime
import jsbeautifier
import os
import time
from selenium import webdriver

# Define the target and malware URLs
def define_URLs():
	# Targeted URLs - URLs that the malware is targetting
	targeted_urls = {
	"nab_ib": "https://ib.nab.com.au/nabib/index.jsp",
	"nab_connect": "https://nabconnect2.nab.com.au/auth/nabc-login/login?TAM_OP=login",
	"westpac": "https://banking.westpac.com.au/wbc/banking/handler?TAM_OP=login&logout=false#/login",
	"commbank": "https://www.my.commbank.com.au/netbank/Logon/Logon.aspx",
	"anz": "https://www.anz.com/inetbank/login.asp",
	"st_george": "https://ibanking.stgeorge.com.au/ibank/loginPage.action",
	"bank_sa": "https://ibanking.banksa.com.au/ibank/loginPage.action",
	"bank_of_melb": "https://ibanking.bankofmelbourne.com.au/ibank/loginPage.action"
	}
	# Malware URLs - URLs that the malware web injects are being hosted at
	malware_urls = {
	"danabot": "DANABOT INJECT URL GOES HERE",
	"gozi": "GOZI INJECT URL GOES HERE"
	}

	return targeted_urls, malware_urls

# Handles the calling of functions and passing along of values
def handler(targeted_urls, malware_urls):
	current_date = datetime.date.today() # Retrieve current date for labelling and storage organisation
	current_date = str(current_date) # Change current date to a string
	os.system("mkdir " + current_date) # Create a new directory with the name being the current date in YYYY-MM-DD

	for targets in targeted_urls.values():
		for malware in malware_urls.values():
			storage_name = inject_retrieval_and_storage(targets, malware, targeted_urls, malware_urls, current_date)
			inject_beautified = beautify_injects(storage_name)
			THE_WEB_INJECT = deobfuscation(inject_beautified, current_date)
			deobd_inject_storage(THE_WEB_INJECT, storage_name)

# Handles the retrieval of the malware web inject
def inject_retrieval_and_storage(target_url, malware_url, targeted_urls, malware_urls, date):

	os.system("clear") # Refreshes the screen to only display the current inject that is being retrieved
	reversed_targeted_urls = dict(map(reversed, targeted_urls.items())) # Reverses the list targeted_urls dictionary
	reversed_malware_urls = dict(map(reversed, malware_urls.items())) # Reverses the list malware_urls dictionary
	target_url_key = reversed_targeted_urls[target_url] # Return the key of the target_url from the targeted_urls dictionary
	malware_url_key = reversed_malware_urls[malware_url] # Return the key of the malware_url from the malware_urls dictionary

	print("Retrieving : " + malware_url_key + " on " + target_url_key) # Displays in terminal the inject that is being retrieved
	print("Target  URL: " + target_url) # Displays the current target url
	print("Malware URL: " + malware_url) # Displays the current malware url
	print("\n")

	# Sends a get request to the malware url with the referer header being the target url - This will return the web inject for the specific target url
	inject = requests.get(
		malware_url,
		headers={"Referer": target_url}
		)

	inject_storage = [] # List to store each line of the inject
	inject_storage.append(inject.text) # Appending inject to the list
	storage_name = date + "/" + target_url_key + "_" + malware_url_key + ".js" # String that will be used to specify where to store file
	with open(storage_name, "w") as storage_file:
		for line in inject_storage: # For each line in the inject_storage list:
			storage_file.write(line) # Write the line to the open storage file
	return storage_name # Return the storage_name 

# Handles the beautification of the javascript inject files - This is to help define values by the line that they appear on
def beautify_injects(storage_name):
	inject_beautified = jsbeautifier.beautify_file(storage_name) # Beautifies the js inject file and stores it
	inject_beautified_list = [] # List to store each beautified line of the inject

	# Writing to and reading from files to get inject into a workable format
	with open(storage_name, "w+") as raw_inject:
		for line in inject_beautified:
			raw_inject.write(line)
	with open(storage_name, 'r') as raw_inject:
		for line in raw_inject:
			inject_beautified_list.append(line)
	return inject_beautified_list # Return the inject_beautified_list

# Handles the deobfuscation of the beuatified inject
def deobfuscation(inject_beautified, date):
	driver = webdriver.Firefox(executable_path="./geckodriver") # Starts a webdriver instance to run the obfuscated inject through the doebfuscation function

	# Define js values to be run - Note that as the malware changes these values will need to change
	obf_inject_string = inject_beautified[1]
	deobf_function_call = inject_beautified[20]
	deob_function = ''
	
	#Create the deob function in a string
	start_line = 3 # Index of the line in the beautified inject list that is the first line of the deobfuscation function
	end_line = 19 # Index of the line in the beautified inject list that is the last line of the deobfuscation function

	i = start_line # Set i equal to the start_line - This is probably unnecessary but to have meaningful variable names is important
	while i <= end_line: # While i is less then or equal to the end_line variable
		deob_function = deob_function + inject_beautified[i] # 
		i += 1 # Increment i by 1

	#Create the JS to be executed
	not_needed_js, underscore, call = deobf_function_call.partition('_') # not_needed_js is some excess js that will interfere with our deobfuscation, underscore is literally just an underscore and call is part of what will make up the doebfuscation function call
	deobf_function_call = underscore + call # _LIJEy(_FNZACrxnaG))(); - need to remove the annoying brackets and symbols at the end
	name_of_deob_f, close_bracket, brackets = deobf_function_call.partition(')')# _LIJEy(_FNZACrxnaG - need to add close bracket
	deobf_function_call = name_of_deob_f + close_bracket # _LIJEy(_FNZACrxnaG) - ready to go
	full_deobfuscation_call = obf_inject_string + '\n' + deob_function + '\n' + "THE_WEB_INJECT = " + deobf_function_call + "\n" + "return THE_WEB_INJECT"

	# Execute the JS and get the deobfuscated JS
	deobd_inject = driver.execute_script(full_deobfuscation_call)
	driver.quit()
	return deobd_inject

# Handles the storage of the deobfuscated malware
def deobd_inject_storage(THE_WEB_INJECT, storage_name):
	with open(storage_name + "CAUTION", "w") as web_inject_file: # The inject file will have CAUTION appended to the end of the file extension
		web_inject_file.write(THE_WEB_INJECT) # Stores the deobfuscated malware

def main():
	urls = define_URLs()
	handler(urls[0], urls[1])

main()
