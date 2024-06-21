import re
from email import message_from_string
from email.header import decode_header
from datetime import datetime
from email import policy
from helpers import chunkstring


def extract(msg):
    output_count = 0
    attachments = []
    try:
        for attachment in msg.iter_attachments():
                    try:
                        attachments.append({"content": attachment.get_payload(decode = True), "filename": attachment.get_filename().split(".")[0], "filetype": attachment.get_filename().split(".")[1]})
                        output_count += 1
                    except TypeError:
                        print("Couldn't get payload for" )
    except IOError:
        print("Problem with file or one of its attachments!")
    return attachments


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
            "body": body,
            "name" : msg["from"][0:(len(msg["from"]))-(len(m[-1])+2)]
        }
    else:
        multi_body=chunkstring(body, 2000)
        return {
            "subject": subject_decoded,
            "date": date,
            "from": m[-1],
            "attachments": attachments,
            "body": multi_body,
            "name" : msg["from"][0:(len(msg["from"]))-(len(m[-1])+2)]
        }