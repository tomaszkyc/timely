#!/bin/bash

# Wait until MySQL is ready
while ! mysql -u root -ppassword -h db  -e "SELECT CURRENT_TIMESTAMP();" 2>/dev/null; do
    echo "Waiting for MySQL to be up..."
    sleep 1
done

# Create a test db to be able to run tests inside or outside the app countainer
test_db_name=db_test

echo "Trying to create $test_db_name for tests purposes."
mysql -u root -ppassword -h db -e "CREATE DATABASE $test_db_name;COMMIT;" 2>/dev/null
echo "Test db $test_db_name created successfully."

# here MySQL db is okey
echo "MySQL db is up and running"