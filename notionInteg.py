import requests
import json
import scraper

with open('credentials.json', 'r') as file:
    credentials = json.load(file)

from datetime import datetime, timezone


headers = {
    "Authorization": "Bearer " + credentials["apiKey"],
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_page(Subject, Task, Deadline, databaseID):
    data = {
    "Subject": {"title": [{"text": {"content": Subject}}]},
    "Task": {"rich_text": [{"text": {"content": Task}}]},
    "Deadline": {"date": {"start": Deadline, "end": None}}
}
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": databaseID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res




databaseID = credentials["databaseId"]

# print(create_page(data))

def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{databaseID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    results = data["results"]

    # while data["has_more"] and get_all:
    #     payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
    #     url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    #     response = requests.post(url, json=payload, headers=headers)
    #     data = response.json()
    #     results.extend(data["results"])

    return results



def refreshAssignments():
    pages = get_pages()
    assignments = scraper.findAssignments()
    print(assignments)
    # print(pages[0]["properties"]["Task"]["rich_text"][0]["text"]["content"])
    for subject in assignments:
        for task in subject["tasks"]:
            # checking for duplicate
            isDuplicate = False
            for page in pages:
                pageTitle = page["properties"]["Task"]["rich_text"][0]["text"]["content"]
                if pageTitle == task['task']:
                    isDuplicate = True
            if isDuplicate == False:
                create_page(subject['subject'], task['task'], task['deadline'], databaseID)

    


refreshAssignments()    
# print(create_page(data))
