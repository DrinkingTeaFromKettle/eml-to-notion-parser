import os
from notion_client import Client
from nextcloud import add_file_to_nextcloud
from time import sleep



def write_email_to_notion(data):
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    attachment_links = ""
    if len(data["attachments"]) > 0:  
        attachment_links = add_file_to_nextcloud(data)
        new_page = {
            "Sender E-mail": {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": data["from"]},
                        },
                    ],
                },
            "Date": {"date": {
                    "start": data["date"]
                }},
            "E-mail Title": {"title": [{"text": {"content":data["subject"]}}]},  
            "Attachments":{
                "type": "rich_text",
                "rich_text": [{
                    "type" : "text",
                    "text" : {"content" : attachment_links } 
                }
                    ]
                },
            
            }
    else:
        new_page = {
            "Sender E-mail": {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": data["from"]},
                        },
                    ],
                },
            "Date": {"date": {
                    "start": data["date"]
                }},
            "E-mail Title": {"title": [{"text": {"content":data["subject"]}}]},  
            }
    if not isinstance(data["body"], str):
        new_page["Content"] = {
            "type": "rich_text",
                "rich_text": [
                    {
                    }
                ],
            }
        array = []
        for d in data["body"]:
            array.append({
                       "type":"text",
                        "text":{"content": d},
            })
        new_page["Content"]["rich_text"] = array
        
    else:
        new_page["Content"] = {
            "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": data["body"]},
                    }
                ],
            }
        
    notion.pages.create(parent={"database_id": os.environ["EMAIL_DB_ID"]}, properties=new_page)


def write_contact_to_notion(data):
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    email_exists = notion.databases.query(
        **{
        "database_id": os.environ['CONTACT_DB_ID'],
        "filter": {
            "property": "E-mail Address",
                "email":{
                    "contains": data["from"],
                },
        },
    })
    if email_exists["results"]:
        print("Dane klienta znajdują się już w bazie.")
    else:    
        new_page = {
        "Contact Name":{
            "title":[{
                "text":{"content": data["name"]}
            }] 
        },
        "E-mail Address": {
                "email":  data["from"]
            },
        "Added automatically": {
            "checkbox": True
        }
        }
        notion.pages.create(parent={"database_id": os.environ["CONTACT_DB_ID"]}, properties=new_page)
  

def create_email_database(dbname):
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    db = notion.search(**{
        "query": dbname,
        "filter": {
        "value": 'database',
        "property": 'object'
        },
    })
    if len(db["results"]) == 0:
        print("Creating database "+dbname+"...")
        db = notion.databases.create(
        **{
        "parent": {
            "type": "page_id",
            "page_id": os.environ["NOTION_PAGE_ID"],
        },
        "title": [
            {
            "type": "text",
            "text": {
                "content": dbname,
                "link": None,
            },
            },
        ],
        "properties": {
            "Sender E-mail": {
                    "rich_text":{},
            },
            "Date": {
                "date": {},
            },
            "E-mail Title": {
                "title": {},
            },
            "Content":{
                "rich_text":{},
            },
            "Attachments":{
                "rich_text":{}
            }
        },
        })
        #Time needed for database creation and api info update
        sleep(20)
        os.environ["EMAIL_DB_ID"] = db["id"]

    else:
        print("Database " +dbname+" already exists. Skipping creation...")
        try:
            os.environ["EMAIL_DB_ID"] = db["results"][0]["id"]
        except:
            print("Couldn't get "+dbname+" database id.")
        
def create_contacts_database(dbname):
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    db = notion.search(**{
        "query": dbname,
        "filter": {
        "value": 'database',
        "property": 'object'
    },})
    if len(db["results"]) == 0:
        print("Creating database "+dbname+"...")
        db = notion.databases.create(
        **{
        "parent": {
            "type": "page_id",
            "page_id": os.environ["NOTION_PAGE_ID"],
        },
        "title": [
            {
            "type": "text",
            "text": {
                "content": dbname,
                "link": None,
            },
            },
        ],
        "properties": {
            "Contact Name": {
                    "title":{},
            },
            "Added automatically":{
                "checkbox":{},
            },
            "E-mail Address": {
                "email": {}
            },
        },
        })
        #Time needed for database creation and api info update
        sleep(20)
        os.environ["CONTACT_DB_ID"] = db["id"]

    else:
        print("Database " +dbname+" already exists. Skipping creation...")
        try:
            os.environ["CONTACT_DB_ID"] = db["results"][0]["id"]
        except:
            print("Couldn't get "+dbname+" database id.")