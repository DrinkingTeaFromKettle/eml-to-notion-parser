import os
from time import time
import requests
import nextcloud_client
import xmltodict
from helpers import randomword


def  add_file_to_nextcloud(data):
    attachment_links = []
    nc = nextcloud_client.Client(os.environ["NEXTCLOUD_HOSTNAME"])
    nc.login(os.environ["NEXTCLOUD_ADMIN_USER"], os.environ["NEXTCLOUD_ADMIN_PASSWORD"])
    file_list = nc.list(os.environ["REMOTE_FOLDER_NAME"]+'/')
    for attachment in data["attachments"]:
        f = open("output/"+attachment["filename"]+"."+attachment["filetype"], "wb")
        f.write(attachment["content"])
        f.close()
        remote_file_name = attachment["filename"]+"_"+ randomword(5)+"."+attachment["filetype"]
        while remote_file_name in file_list:
            remote_file_name = attachment["filename"]+"_"+ randomword(5)+"."+attachment["filetype"]       
        nc.put_file(os.environ["REMOTE_FOLDER_NAME"]+'/' + remote_file_name, "output/"+attachment["filename"]+"."+attachment["filetype"])
        
        propfind_optins="""<?xml version="1.0" encoding="UTF-8"?>
            <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
            <d:prop>
                <oc:id/>
            </d:prop>
            </d:propfind>"""
        
        r = requests.request(
            'PROPFIND',
            os.environ["REMOTE_FOLDER_URL"]+"/"+remote_file_name,
            auth=(os.environ["NEXTCLOUD_ADMIN_USER"], os.environ["NEXTCLOUD_ADMIN_PASSWORD"]),
            data=propfind_optins
        )
        
        start_time = time() * 1000
        xml_dict = xmltodict.parse(r.text, dict_constructor=dict)
        end_time = time() * 1000
        print("Time: " + str(end_time-start_time))
        id = xml_dict['d:multistatus']['d:response']['d:propstat']['d:prop']['oc:id']
        
        attachment_links.append( 
             {
               "name": remote_file_name,
               "type": "external",
               "external": {
                   "url": os.environ["NEXTCLOUD_HOSTNAME"]+'/f/'+id,
               }
             }
           )
        os.remove("output/"+attachment["filename"]+"."+attachment["filetype"])
        return attachment_links