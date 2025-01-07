# local database

## psql

Install posrgresql

```sh
sudo dnf install postgresql
yay -Syyu postgresql
```

```sh
psql postgresql://admin:superadmin@localhost:5432/our_db
```

