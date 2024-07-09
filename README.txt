1. docker compose up -d
2. WAIT
3. docker exec -u www-data -it python-nextcloud  sh -c 'export OC_PASS="passw!2345^"; php occ user:add --password-from-env --display-name="user" --group="users" --group="admin" user'