Param($ftp_pass, $nextcloud_pass, $notion_token, $page_id, $email_db, $contact_db)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python .\set_env.py --ftp_pass=$ftp_pass --nextcloud_pass=$nextcloud_pass --notion_token=$notion_token --page_id=$page_id --email_db=$email_db --contact_db=$contact_db
docker compose up -d
python .\main.py