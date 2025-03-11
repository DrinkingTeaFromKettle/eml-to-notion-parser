import ftplib, os
from time import sleep
import schedule
from dotenv import load_dotenv
from eml_parser import parse_eml
from notion import write_email_to_notion, write_contact_to_notion,create_email_database,create_contacts_database

load_dotenv()

def job():
    create_email_database(os.environ["EMAIL_DB_NAME"])
    create_contacts_database(os.environ["CONTACT_DB_NAME"])
    retry = True
    while (retry):
        try:
            #Connection to ftp server 
            ftp = ftplib.FTP(os.environ["FTP_HOST"], os.environ["FTP_USER"], os.environ["FTP_SECRET"]) 
            #Move to foler with files 
            ftp.cwd(os.environ["FTP_FILE_FOLDER"])
            #Get list of files
            filenames = ftp.nlst()
            retry = False
            if len(filenames) > 0:
                for filename in filenames:
                    data=[]
                    file = []
                    #Get file data as binary
                    ftp.retrbinary('RETR '+ filename, file.append)
                    #Parse decoded data as bytes
                    data = parse_eml(b''.join(file).decode())
                    write_email_to_notion(data)
                    write_contact_to_notion(data)
                    #Move file to arhcive
                    ftp.rename(filename, os.environ["FTP_ARCHIVE_FOLDER_PATH"]+'/'+filename)
                    
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
            sleep(10)
            retry = True

if __name__ == "__main__":
        print("WORKING")
        schedule.every(30).seconds.do(job)
        while True:
            schedule.run_pending()
            sleep(1)
        