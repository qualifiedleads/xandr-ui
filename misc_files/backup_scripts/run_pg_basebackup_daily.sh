#!/bin/bash
#### Copy PostgresSQL backups created using pg_basebackup ####
#### see more at https://www.postgresql.org/docs/current/static/app-pgbasebackup.html ####
#### https://www.postgresql.org/docs/current/static/continuous-archiving.html ####
#### https://www.postgresql.org/docs/current/static/warm-standby.html ####
clear

echo "Start pg_basebackup..."

BBFOLDER_NAME=`date +%Y-%m-%d-%H-%M-%S`
FILE_NAME=$BBFOLDER_NAME".tar.gz"
BASE_FOLDER="/mnt/base_backups"

PGPASSWORD="<password>" pg_basebackup -h localhost -U "postgres" -D $BASE_FOLDER/$BBFOLDER_NAME/
cd $BASE_FOLDER
tar -zcvf $FILE_NAME $BBFOLDER_NAME
RES=$?
if test $RES -eq 0
  then
    rm -rf $BBFOLDER_NAME
fi

echo "pg_basebackup backed up database cluster folder into "$BASE_FOLDER"/"$FILE_NAME

lftp -c "open ftp://<user>:<password>@<ftp.url>; cd postgresql_base_backups; mput /mnt/base_backups/"$FILE_NAME"; quit"

echo "DB backup uploaded to FTP!"
