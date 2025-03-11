Powyższy projekt służy do automatycznego synchronizowania korespondencji e-mail zapisanej na lokalnym serwerze ftp z bazą danych w serwisie Notion z integracją z serwerem NextCloud. Treść korespondencji oraz kontakt nadawcy zapisywany jest w bazie danych Notion, załączniki dołączone do wiadomości e-mail zapisywane są w serwerze NextCloud. 


## Pierwsze uruchamianie skryptu:
1. W serwisie Notion stworzyć bazę danych, do której następnie dodać dwie podrzędne bazy danych, jedną do której będą dodawane treści korespondencji, oraz drugą do której dodawane będą dane nadawców korespondencji. Domyślnymi nazwami w skrypcie są 'Emails' oraz 'Contacts', ale można nadać inne preferowane nazwy.
2. Wejść na stronę stworzonej bazy danych Notion skopiować jej ID, jest to część URL znajdująca się po 'https://www.notion.so/Database-'. 
3. Korzystając z instrukcji znajdujących się w rozdziale "Create your integration in notion" na stronie https://developers.notion.com/docs/create-a-notion-integration stworzyć integrację wewnętrzną oraz skopiować 'API Secret'.
4. Dodać integrację jako 'connections' do bazy danych (trzy kropki w prawym górnym rogu).
5. W tej chwili można uruchomić program za pomocą komendy:

Dla Windows:

`.\start.ps1 -notion_token <API Secret> -page_id <ID bazy danych>` 

Dla Linux:

`./start.sh --notion_token <API Secret> --page_id <ID bazy danych> `

wykonanej z poziomu folderu zawierającego pliki programu. 

### Dodatkowe argumenty:

`ftp_pass` - hasło do serwera ftp.

`nextcloud_pass` - hasło do serwera nextcloud.

`email_db` - nazwa dla bazy danych korespondencji

`contact_db` - nazwa dla bazy danych nadawców


Domyślne login i hasło do serwera ftp : admin , pass#123
Domyślne login i hasło do serwera nextcloud : admin, admin

## English

The above project is used to automatically synchronize email correspondence stored on a local ftp server with a database in Notion with integration with NextCloud server. The content of the correspondence and the sender's contact are saved in the Notion database, the attachments included in the email are saved in the NextCloud server. 


## Initial activation of the script:
1. In Notion, create a page with any name.
2. Copy the ID of the created page, it's the part of the URL located after 'https://www.notion.so/NazwaStrony-'. 
3. Using instructions found in 'Create your integration in notion' at https://developers.notion.com/docs/create-a-notion-integration, create an internal integration and copy the 'API Secret'.
4. Add the integration as 'connections' to the database (three dots in the upper right corner).
5. At this point, you can run the program with the command:

For Windows:

`.\start.ps1 -notion_token <API Secret> -page_id <database ID>`. 

For Linux:

`./start.sh --notion_token <API Secret> --page_id <databaseID>`.

executed from the folder containing the program files. 

### Additional arguments:

`ftp_pass` - the password for the ftp server.

`nextcloud_pass` - password for nextcloud server.

`email_db` -  name for database containing correspondence

`contact_db` - name for database containing senders

Default login and password for ftp server : admin , pass#123
Default login and password for nextcloud server : admin, admin
