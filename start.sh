#!/bin/sh
FTP_PASS=""
NEXTCLOUD_PASS=""
NOTION_TOKEN=""
PAGE_ID=""
EMAIL_DB=""
CONTACT_DB=""

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --ftp_pass=*) FTP_PASS="${1#*=}" ;;
    --nextcloud_pass=*) NEXTCLOUD_PASS="${1#*=}" ;;
    --notion_token=*) NOTION_TOKEN="${1#*=}" ;;
    --page_id=*) PAGE_ID="${1#*=}" ;;
    --email_db=*) EMAIL_DB="${1#*=}" ;;
    --contact_db=*) CONTACT_DB="${1#*=}" ;;
    *) echo "Unknown parameter: $1"; exit 1 ;;
  esac
  shift
done

# Ensure required parameters are set
if [ -z "$NOTION_TOKEN" ] || [ -z "$PAGE_ID" ]; then
  echo "Error: --notion_token and --page_id are required parameters."
  exit 1
fi

python -m venv venv

venv/bin/activate

python set_env.py --ftp_pass="$FTP_PASS" --nextcloud_pass="$NEXTCLOUD_PASS" --notion_token="$NOTION_TOKEN" --page_id="$PAGE_ID" --email_db="$EMAIL_DB" --contact_db="$CONTACT_DB"

docker compose up -d

python main.py
