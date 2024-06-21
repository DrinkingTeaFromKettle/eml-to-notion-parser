import os
from notion_client import Client
from nextcloud import add_file_to_nextcloud

notion = Client(auth=os.environ["NOTION_TOKEN"])

def write_email_to_notion(data):
    
    if len(data["attachments"]) > 0:  
        attachment_links = add_file_to_nextcloud(data)        
    
    new_page = {
        "e-mail wysyłającego": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": data["from"]},
                    },
                ],
            },
        "Data otrzymania korespondencji": {"date": {
                "start": data["date"]
            }},
        "Tytuł e-mail ": {"title": [{"text": {"content":data["subject"]}}]},  
        "Załącznik":{
            "type": "files",
            "files": attachment_links,
        },
        }
    if not isinstance(data["body"], str):
        new_page["Treść otrzymanej korespondencji"] = {
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
        new_page["Treść otrzymanej korespondencji"]["rich_text"] = array
        
    else:
        new_page["Treść otrzymanej korespondencji"] = {
            "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": data["body"]},
                    }
                ],
            }
        
    notion.pages.create(parent={"database_id": os.environ["DB_ID"]}, properties=new_page)


def write_client_to_notion(data):
    email_exists = notion.databases.query(
        **{
        "database_id": os.environ['CLIENT_DB'],
        "filter": {
            "property": "Adres mailowy",
            "multi_select":{
            "contains": data["from"],
            },
        },
    })
    if email_exists["results"]:
        print("Dane klienta znajdują się już w bazie.")
    else:
        client_exists = notion.databases.query(
        **{
        "database_id": os.environ['CLIENT_DB'],
        "filter": {
            "property": "slug",
            "rich_text":{
            "contains": "".join(data["name"].upper().split()),
            },
        },
        })
        if client_exists["results"]:
            multi_select = []
            for email in client_exists["results"][0]["properties"]["Adres mailowy"]["multi_select"]:
                multi_select.append({"name": email['name']})
            multi_select.append({"name": data["from"]})
            notion.pages.update(
                **{
                    "page_id": client_exists["results"][0]["id"],
                    "properties":{
                        "Adres mailowy": {
                            "multi_select": multi_select
                        }
                    }
            })
        else:    
            new_page = {
            "Osoba kontaktowa":{
            "title":[{
                "text":{"content":data["name"]}
            } ] 
            },
            "Adres mailowy": {
                    "multi_select": [
                        {"name": data["from"]}
                    ]
                },
            "Dodane automatycznie": {
                "checkbox": True
            }
            }
            notion.pages.create(parent={"database_id": os.environ["CLIENT_DB"]}, properties=new_page)
  