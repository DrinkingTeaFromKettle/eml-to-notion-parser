##Pierwsze uruchamianie skryptu:
1. W serwisie Notion stworzyć bazę danych, do której następnie dodać dwie podrzędne bazy danych, jedną do której będą dodawane treści korespondencji, oraz drugą do której dodawane będą dane nadawców korespondencji. Domyślnymi nazwami w skrypcie są 'Emails' oraz 'Contacts', ale można nadać inne preferowane nazwy.
2. Wejść na stronę stworzonej bazy danych Notion skopiować jej ID, jest to część URL znajdująca się po 'https://www.notion.so/Database-'. 
3. Korzystając z instrukcji znajdujących się w rozdziale "Create your integration in notion" na stronie https://developers.notion.com/docs/create-a-notion-integration stworzyć integrację wewnętrzną oraz skopiować 'API Secret'.
4. W tej chwili można uruchomić program za pomocą komendy:
Dla Windows:
`.\start.ps1 -notion_token <API Secret> -page_id <ID bazy danych> -email_db <nazwa bazy danych korespondencji> -contact_db <nazwa bazy danych nadawców>` 
Dla Linux:
`./start.sh --notion_token <API Secret> --page_id <ID bazy danych> --email_db <nazwa bazy danych korespondencji> --contact_db <nazwa bazy danych nadawców>`
wykonanej z poziomu folderu zawierającego pliki programu. Jeżeli bazom danych nadano nazwy domyślne to można pominąć argumenty `email_db` i `contact_db`.

###Dodatkowe argumenty:
`ftp_pass` - hasło do serwera ftp.
`nextcloud_pass` - hasło do serwera nextcloud.

Domyślne login i hasło do serwera ftp : admin , pass#123
Domyślne login i hasło do serwera nextcloud : admin, admin