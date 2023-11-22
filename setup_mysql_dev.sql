#!/bin/bash

# MySQL server configuration
MYSQL_ROOT_USER="root"
MYSQL_ROOT_PASSWORD="your_root_password"

# Database and user configuration
DB_NAME="hbnb_dev_db"
DB_USER="hbnb_dev"
DB_PASSWORD="hbnb_dev_pwd"

# Check if the database and user already exist
DB_EXISTS=$(mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES LIKE '$DB_NAME';" | grep "$DB_NAME")
USER_EXISTS=$(mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "SELECT user FROM mysql.user WHERE user='$DB_USER';" | grep "$DB_USER")

# Create the database if it doesn't exist
if [ -z "$DB_EXISTS" ]; then
    mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE $DB_NAME;"
    echo "Database $DB_NAME created."
else
    echo "Database $DB_NAME already exists."
fi

# Create the user if it doesn't exist
if [ -z "$USER_EXISTS" ]; then
    mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
    echo "User $DB_USER created."
else
    echo "User $DB_USER already exists."
fi

# Grant privileges to the user
mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"
mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "GRANT SELECT ON performance_schema.* TO '$DB_USER'@'localhost';"

# Flush privileges
mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "FLUSH PRIVILEGES;"

echo "Script executed successfully."

