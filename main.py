import ftplib, os
from time import sleep
import schedule
from dotenv import load_dotenv
from eml_parser import parse_eml
from notion import write_email_to_notion, write_client_to_notion

load_dotenv()

def job():
    
    retry = True
    while (retry):
        try:
            ftp = ftplib.FTP(os.environ["FTP_HOST"], os.environ["FTP_USER"], os.environ["FTP_SECRET"]) 
            ftp.cwd(os.environ["FTP_FILE_FOLDER"])
            filenames = ftp.nlst()
            retry = False
            if len(filenames) > 0:
                for filename in filenames:
                    data=[]
                    file = []
                    ftp.retrbinary('RETR '+ filename, file.append)
                    data = parse_eml(b''.join(file).decode())
                    write_email_to_notion(data)
                    write_client_to_notion(data)
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
            sleep(1)
            retry = True

if __name__ == "__main__":
        schedule.every(5).seconds.do(job)
        while True:
            schedule.run_pending()
            sleep(1)