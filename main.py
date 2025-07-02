import requests as rq
from bs4 import BeautifulSoup
import json

session = rq.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

homeUrl = "https://dlsudshs.edu20.org/log_in/form"
loginUrl = 'https://dlsudshs.edu20.org/log_in/submit_from_portal?original_host=dlsudshs.edu20.org'

# Getting creds
with open('credentials.json', 'r') as file:
    data = json.load(file)

# Finding Auth Token
response = session.get(homeUrl)
soup = BeautifulSoup(response.text, 'html.parser')
tokenElements = soup.find_all("input", attrs={"name": "authenticity_token"})
token = tokenElements[0].get('value')

# Logging in
payload = {
    'userid': data['User'],
    'password': data["Pass"],
    'authenticity_token': token
}
response = session.post(loginUrl, headers=headers, params=payload)

# Cookies
# for cookie in session.cookies:
#     print(f"{cookie.name} = {cookie.value}")

# Getting Assignments
check_url = 'https://dlsudshs.edu20.org/user_to_do_widget/tasks'
response = session.get(check_url, headers=headers, cookies=session.cookies, allow_redirects=True)

# Parsing Assignments
soup = BeautifulSoup(response.text, 'html.parser')
assignmentList = soup.find_all('a',attrs={'class':'title_and_count'})
for assignment in assignmentList:
    assignmentData = assignment.find_all('span')
    for datum in assignmentData:
        print(datum)
    



# Write to HTML
outputFile = open("output.html", 'w')
outputFile.write(response.text)
