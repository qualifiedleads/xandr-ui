#!/bin/sh
#### Backup of whole PostgreSQL db using pg_dump in custom format (allows restore of single table). And upload it on AWS S3 ####
#### BEGIN CONFIGURATION ####
  export AWS_ACCESS_KEY_ID=""
  export AWS_SECRET_ACCESS_KEY=""
  export PASSPHRASE=""
# set dates for backup rotation
NOWDATE=`date +%Y-%m-%d`
LASTDATE=$(date +%Y-%m-%d --date='1 week ago')

# set backup directory variables
SRCDIR='/tmp/s3backups'
DESTDIR='database'
BUCKET='<bucket>'

# database access details
PG_BIN='/usr/local/pgsql/bin'
HOST='localhost'
PORT='5432'
USER='postgres'

#### END CONFIGURATION ####

# make the temp directory if it doesn't exist
mkdir -p $SRCDIR

# dump each database to its own sql file
DBLIST=`$PG_BIN/psql -l -h$HOST -p$PORT -U$USER \
| awk '{print $1}' | grep -v "+" | grep -v "Name" | \
grep -v "List" | grep -v "(" | grep -v "template" | \
grep -v "postgres" | grep -v "root" | grep -v "|" | grep -v "|"`

# get list of databases
for DB in ${DBLIST}
do
$PG_BIN/pg_dump --host $HOST --port $PORT --username $USER --no-password  --format custom --blobs --file $SRCDIR/$NOWDATE-$DB.dump $DB
done

# tar all the databases into $NOWDATE-backups.tar.gz
cd $SRCDIR
tar -czPf $NOWDATE-backup.tar.gz *.dump

# upload backup to s3
/usr/bin/s3cmd put $SRCDIR/$NOWDATE-backup.tar.gz s3://$BUCKET/$DESTDIR/ > /dev/null

# delete old backups from s3
#/usr/bin/s3cmd del --recursive s3://$BUCKET/$DESTDIR/$LASTDATE-backup.tar.gz

# remove all files in our source directory
#cd
rm -f $SRCDIR/*.dump
