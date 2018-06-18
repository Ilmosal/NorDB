cd nordb/sql

echo "Give your postgres password to create the database"

echo "1salis7" | createdb nordb
echo "1salis7" | psql nordb -f make_tables.sql 2>1

echo "Database nordb created to your system!"

cd ../..
