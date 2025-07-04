import requests as rq
from bs4 import BeautifulSoup
import json
from notionInteg import create_page
from datetime import datetime, timezone


session = rq.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

homeUrl = "https://dlsudshs.edu20.org/log_in/form"
loginUrl = 'https://dlsudshs.edu20.org/log_in/submit_from_portal?original_host=dlsudshs.edu20.org'

databaseID = "20f0b4372f5080eb93fec3643d678318"

Subject = "poopy"
Task = "poop nugget"
Deadline = datetime.now().astimezone(timezone.utc).isoformat()

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
subjectList = soup.find_all('a',attrs={'class':'title_and_count'})
data = []
for subject in subjectList:
    subjectDataRaw = subject.find_all('span')
    assignUrl = "https://dlsudshs.edu20.org" + subject['href'] 

    subjectData = {"subjTitle": subjectDataRaw[0],
                   "assignCount": subjectDataRaw[1],
                   "url": assignUrl}

    # Getting individual Assignments from subjects listed
    subjectUrl = assignUrl.replace("?redirect_if_one=true", "")
    response = session.get(subjectUrl, headers=headers, cookies=session.cookies, allow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    assignmentTable = soup.find_all('table', attrs={'class':'assignmentsTable'})
    # Assignment Deets
    for n in assignmentTable:
        assignDetails = assignmentTable[0].find_all("tr")[1].find_all("td")
        assignName = assignDetails[1].text.replace("\n", "")

        # assignStart = " ".join(assignDetails[2].text.split())
        # if len(assignStart) <= 6:  
        #     assignStart = assignStart + " 11:59 PM"
        # assignStart = datetime.strptime(str(datetime.now().year) + assignStart, f"%Y%b %d %I:%M %p").isoformat()


        assignEnd = " ".join(assignDetails[3].text.split())
        if len(assignEnd) <= 6:    
            assignEnd = assignEnd + " 11:59 PM"
        assignEnd = datetime.strptime(str(datetime.now().year) + assignEnd, f"%Y%b %d %I:%M %p").isoformat()
        print(assignName + "  " + assignEnd)

# TO DO:
# NOTION INTEGRATION, CHECK FOR EXISTING TO STOP DUPLICATES
