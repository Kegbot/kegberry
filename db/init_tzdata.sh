#!/bin/sh
# Wait to be sure that MySql is up
while ! /usr/bin/mysql -u root -e "use mysql;"
do
    sleep 2
done

echo "APPLY SYSTEM TIMEZONES START"

query="select count(*) from time_zone"

count=`/usr/bin/mysql -u root --skip-column-names mysql << eof
$query
eof`

if [ $count -eq 0 ]
then
    sh -c "mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql"
    echo "APPLY SYSTEM TIMEZONES COMPLETE"
else
    echo "SYSTEM TIMEZONES ALREAY POPULATED"
fi
