import requests
import csv
import re
import random
import time
import pandas as pd
from sys import exit
from bs4 import BeautifulSoup

print("Initiating... please wait.\n")
search_from, URL_edit= "", ""

def wait():
	print("Waiting for a few secs...")
	time.sleep(random.randrange(1, 6))
	print("Waiting done. Continuing...\n")

def checkPage():
	global search_from
	if "pubmed" in URL_input:
		search_from = "Pubmed"
		print("Input is from: PubMed.\n")
	else:
		print("Page URL undefined.\n")


#Get URL
URL_input = input("Please paste search URL and press Enter:")
URL_ori = URL_input
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/15.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20210916 Firefox/95.0',
})
checkPage()


# Main
if search_from == "Pubmed":

	try:

		# CSV file
		outfile = open("scrapped_pubmed.csv","w",newline='',encoding='utf-8')
		writer = csv.writer(outfile)
		df = pd.DataFrame(columns=['Title','Links','References'])

		# Page number
		page_num = 1
		page_view = 100 # can be change to 10, 20, 50, 100 or 200
		URL_edit = URL_ori + "&page=" + str(page_num) + "&size=" + str(page_view)	
		print("URL : ", URL_edit)

		page = requests.get(URL_edit, headers=headers, timeout=None)
		soup = BeautifulSoup(page.content, "html.parser")
		wait()

		page_total = soup.find("label", class_="of-total-pages").text
		page_total_num = int(''.join(filter(str.isdigit, page_total)))
		print(f"Total page number: {page_total_num}")
		print(f"Results per page: {page_view}.\n")

	except AttributeError:

		print("Opss! ReCaptcha is probably preventing the code from running.")
		print("Please consider running in another time.\n")
		exit()

	wait()

	# Extract info
	for i in range(page_total_num):

		page_num_up = page_num + i
		URL_edit = URL_ori + "&page=" + str(page_num_up) + "&size=" + str(page_view)
		page = requests.get(URL_edit, headers=headers, timeout=None)	

		soup = BeautifulSoup(page.content, "html.parser")
		wait()
		results = soup.find("section", class_="search-results-list")

	try:

		# Extract info
		job_elements = results.find_all("article", class_="full-docsum")

		for job_element in job_elements:
			title_element = job_element.find("a", class_="docsum-title")
			cit_element = job_element.find("span", class_="docsum-journal-citation full-journal-citation").text.strip()

			links = job_element.find_all("a") 
			for link in links:
				link_url = link["href"]
		
			title_element_clean = title_element.text.strip()
			link_url_clean = "https://pubmed.ncbi.nlm.nih.gov"+link_url

			print(title_element_clean)
			print(link_url_clean)
			print(cit_element)
			print()

			df2 = pd.DataFrame([[title_element_clean, link_url_clean, cit_element]],columns=['Title','Links','References'])
			df = pd.concat([df, df2], ignore_index=True)

		wait()

	except AttributeError:

		print("Opss! ReCaptcha is probably preventing the code from running.")
		print("Please consider running in another time.\n")
		exit()

	df.index += 1
	df.to_csv('scrapped_pubmed.csv')
	outfile.close()

# End
print("Finished.")