import random, string
import time
import ftplib

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def move_to_dated_folder(ftp:ftplib.FTP, filename, dir):
   folder_name = time.strftime('%Y%m%d%H%M%S')
   path = ftp.mkd("../" + dir + "/" + folder_name)
   ftp.rename(filename, "/" + path + "/" + filename)