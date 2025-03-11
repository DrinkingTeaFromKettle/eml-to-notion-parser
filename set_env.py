import os
import argparse
from dotenv import load_dotenv,set_key,find_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("--ftp_pass", help="Password for ftp server")
parser.add_argument("--nextcloud_pass", help="Password for nextcloud admin")
parser.add_argument("--notion_token", help="Notion token")
parser.add_argument("--page_id", help="Id of notion page containing databases")
parser.add_argument("--email_db", help="Name of email database in notion")
parser.add_argument("--contact_db", help="Name of contacts database in notion")

args = parser.parse_args()

dotenv_file = find_dotenv()
load_dotenv()

if args.ftp_pass:
    set_key(dotenv_file, "FTP_SECRET", args.ftp_pass)
if args.nextcloud_pass:
    set_key(dotenv_file, "NEXTCLOUD_ADMIN_PASSWORD", args.nextcloud_pass)
if args.notion_token:
    set_key(dotenv_file, "NOTION_TOKEN", args.notion_token)
if args.page_id:
    set_key(dotenv_file, "NOTION_PAGE_ID", args.page_id)
if args.email_db:
    set_key(dotenv_file, "EMAIL_DB_NAME", args.email_db)
if args.contact_db:
    set_key(dotenv_file, "CONTACT_DB_NAME", args.contact_db)