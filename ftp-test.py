import ftplib, os, re, email
from time import sleep
import schedule
from dotenv import load_dotenv
from email import message_from_string
from email.header import decode_header
from datetime import datetime
from notion_client import Client
from email import policy
import json


load_dotenv()

def extract(msg):
    output_count = 0
    attachments = []
    try:
        for attachment in msg.iter_attachments():
                    try:
                        attachments.append(attachment.get_payload(decode=True))
                        output_count += 1
                    except TypeError:
                        print("Couldn't get payload for %s" % attachment.get_filename())
        if output_count == 0:
            print("No attachment found for file!")
    except IOError:
        print("Problem with file or one of its attachments!")
    return attachments

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def parse_eml(file):
    msg = message_from_string(file, policy=policy.default)
    m = re.findall(r'[\w.!#$%&\'*+-/=?^_`{|}~]+@[\w-]+\.[\w.-]+',msg["from"])
    date = datetime.strptime(msg["Date"], "%a, %d %b %Y %X %z")
    date = date.strftime("%Y-%m-%d")
    decoded_subject_header = decode_header(msg["Subject"])
    subject = decoded_subject_header[0]
    attachments = extract(msg)
    subject_decoded = subject[0]
    if subject[1] != None:
        subject_decoded = subject[0].decode(subject[1])
    b = msg 
    body = ""
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == 'text/plain' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = b.get_payload(decode=True)
    body = body.decode()
    if len(body) < 2000:
        return {
            "subject": subject_decoded,
            "date": date,
            "from": m[-1],
            "attachments": attachments,
            "body": body
        }
    else:
        multi_body=chunkstring(body, 2000)
        return {
            "subject": subject_decoded,
            "date": date,
            "from": m[-1],
            "attachments": attachments,
            "body": multi_body
        }
    
    
    
def job():
    retry = True
    while (retry):
        try:
            ftp = ftplib.FTP(os.environ["FTP_HOST"], os.environ["FTP_USER"], os.environ["FTP_SECRET"]) 
            ftp.cwd('test')
            filenames = ftp.nlst()
            print(filenames)
            retry = False
            if len(filenames) > 0:
                for filename in filenames:
                    data=[]
                    file = []
                    ftp.retrbinary('RETR '+ filename, file.append)
                    data = parse_eml(b''.join(file).decode())
                    write_to_notion(data)
                    ftp.rename(filename, '../archive/'+filename)
            else:
                print("No files to download.")
            ftp.quit()
        except ftplib.error_perm as e:
            print("An error occured: %s", e)
            print("Quitting")
            retry=False
        except ftplib.all_errors as e:
            print("An error occured: %s", e)
            print("Retrying...")
            sleep(1)
            retry = True

            
def write_to_notion(data):
    notion = Client(auth=os.environ["NOTION_TOKEN"])
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


if __name__ == "__main__":
        schedule.every(5).seconds.do(job)
        while True:
            schedule.run_pending()
            sleep(1)
            
            