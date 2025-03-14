from datetime import datetime
import ftplib, os
from time import sleep
import schedule
from dotenv import load_dotenv
from eml_parser import parse_eml
from notion import write_email_to_notion, write_contact_to_notion,create_email_database,create_contacts_database
from helpers import move_to_dated_folder

load_dotenv()

def job():
    create_email_database(os.environ["EMAIL_DB_NAME"])
    create_contacts_database(os.environ["CONTACT_DB_NAME"])
    try:
        #Connection to ftp server 
        ftp = ftplib.FTP(os.environ["FTP_HOST"], os.environ["FTP_USER"], os.environ["FTP_SECRET"]) 
        #Move to foler with files 
        ftp.cwd(os.environ["FTP_FILE_FOLDER"])
        #Get list of files
        filenames = ftp.nlst()
        if len(filenames) > 0:
            for filename in filenames:
                data=[]
                file = []
                retry = 0
                #Get file data as binary
                ftp.retrbinary('RETR '+ filename, file.append)
                #Parse decoded data as bytes
                dir = "archive"
                while retry < 3:
                    try:
                        data = parse_eml(b''.join(file).decode())
                        write_email_to_notion(data)
                        write_contact_to_notion(data)
                        #Move file to arhcive
                        retry = 4
                    except Exception as e:
                        retry += 1
                        if retry == 3:
                            print("Couldn't upload email file "+ filename)
                            dir = "skipped"
                        print("An error occured: %s", e)
                        print("Retrying...")
                        sleep(3)
                move_to_dated_folder(ftp, filename, dir)

        else:
            print("No files to download.")
        ftp.quit()
    except ftplib.error_perm as e:
        print("An error occured: %s", e)
        print("Quitting")
        exit(1)

if __name__ == "__main__":
        print("WORKING")
        schedule.every(5).seconds.do(job)
        while True:
            schedule.run_pending()
            sleep(1)
        