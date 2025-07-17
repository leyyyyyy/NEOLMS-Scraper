import requests as rq
from bs4 import BeautifulSoup
import json
# from notionInteg import create_page
from datetime import datetime, timezone


def findAssignments():
    session = rq.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    homeUrl = "https://dlsudshs.edu20.org/log_in/form"
    loginUrl = 'https://dlsudshs.edu20.org/log_in/submit_from_portal?original_host=dlsudshs.edu20.org'


    # Getting creds
    with open('credentials.json', 'r') as file:
        creds = json.load(file)

    # Finding Auth Token
    response = session.get(homeUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    tokenElements = soup.find_all("input", attrs={"name": "authenticity_token"})
    token = tokenElements[0].get('value')

    # Logging in
    payload = {
        'userid': creds['User'],
        'password': creds["Pass"],
        'authenticity_token': token
    }
    response = session.post(loginUrl, headers=headers, params=payload)

    aliases = creds['aliases']


    # Cookies
    # for cookie in session.cookies:
    #     print(f"{cookie.name} = {cookie.value}")
    data = []

    # Getting Assignments
    check_url = 'https://dlsudshs.edu20.org/user_to_do_widget/tasks'
    response = session.get(check_url, headers=headers, cookies=session.cookies, allow_redirects=True)
    output = open("output.html", "w")
    output.write(response.text)
    # Parsing Assignments
    soup = BeautifulSoup(response.text, 'html.parser')
    subjectList = soup.find_all('a',attrs={'class':'title_and_count'})


    tasksUl = soup.find('ul')
    tasksLi = tasksUl.find_all("li", id=lambda value: value and value.startswith("todo"))
    print("tasksLi")
    print(tasksLi)
    if tasksLi:
        selfData = []
        for task in tasksLi:
            selfData.append({"task": task.find('span').text})

            print(task.find('span').text)
            print('\n\n\n\n poopy')
        
        data.append({
                    "subject": "Self",
                    "count": len(tasksLi),
                    "tasks": selfData
                        })

    for subject in subjectList:
        subjectDataRaw = subject.find_all('span')
        assignUrl = "https://dlsudshs.edu20.org" + subject['href'] 

        subjectData = {"subject": subjectDataRaw[0].text,
                    "count": subjectDataRaw[1].text,
                    "url": assignUrl}
        
        # Changing subj name to alias
        if subjectData["subject"] in aliases:
            subjectData["subject"] = aliases[subjectData["subject"]]

        # Getting individual Assignments from subjects listed
        subjectUrl = assignUrl.replace("?redirect_if_one=true", "")
        response = session.get(subjectUrl, headers=headers, cookies=session.cookies, allow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        assignmentTable = soup.find('table', attrs={'class':'assignmentsTable'})
        assignmentTr = assignmentTable.find_all("tr")

        # Assignment Deets
        assignmentList = []
        i = 0
        
        for assignDetails in assignmentTr:
            if i == 0:
                i = i + 1
                continue
            i = i + 1

            assignDetails = assignDetails.find_all("td")
            
            # Name
            assignmentName = assignDetails[1]
            assignmentName = assignmentName.text.replace("\n", " ")
            assignmentName = " ".join(assignmentName.split())

            # Deadline
            assignEnd = " ".join(assignDetails[3].text.split())
            if len(assignEnd) <= 6:  
                assignEnd = assignEnd + " 11:59 PM"
            assignEnd = datetime.strptime(str(datetime.now().year) + assignEnd, f"%Y%b %d %I:%M %p").isoformat()
         
            assignmentList.append({
                "task": assignmentName,
                "deadline": assignEnd
            })
            subjectData["tasks"] = assignmentList
        data.append(subjectData)


    return data

findAssignments()
def addAssignment(name):

    session = rq.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    homeUrl = "https://dlsudshs.edu20.org/log_in/form"
    loginUrl = 'https://dlsudshs.edu20.org/log_in/submit_from_portal?original_host=dlsudshs.edu20.org'


    # Getting creds
    with open('credentials.json', 'r') as file:
        creds = json.load(file)

    # Finding Auth Token
    response = session.get(homeUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    tokenElements = soup.find_all("input", attrs={"name": "authenticity_token"})
    token = tokenElements[0].get('value')

    # Logging in
    payload = {
        'userid': creds['User'],
        'password': creds["Pass"],
        'authenticity_token': token
    }
    response = session.post(loginUrl, headers=headers, params=payload)
    createUrl = "https://dlsudshs.edu20.org/task/create"
    response = session.post(createUrl, headers=headers, cookies=session.cookies, allow_redirects=True, data = {"task[description]": name, "authenticity_token": token})
    print(response)



