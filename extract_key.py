import RAKE
import requests
import csv
from bs4 import BeautifulSoup

# Specify the URL of the text
url = "https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=1428003&casa_token=m2n_9keUwHwAAAAA:_Ih5SZLc-Y1CZfcF3Pq8rg4pJ_UexERwqHML0Obt6uy_P-yKjrcMZ6aey4uGpM8j-ZH_4ZUqnwMG"

# Define a custom stop word list
stop_words = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with']

# Download the text from the URL
response = requests.get(url)
html = response.text

# Extract the text from the HTML
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text()

# Initialize the RAKE keyword extractor
rake = RAKE.Rake(stop_words)

# Extract the keywords from the text
n = 10
keywords = rake.run(text)
top_keywords = sorted(keywords, key=lambda x: x[1], reverse=True)[:n]

with open('output.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  for keyword, score in top_keywords:
    writer.writerow([keyword, score])


print(top_keywords)
