#!/bin/bash
#### Backup directories of local file system to AWS S3 ####
#set -x

# Export some ENV variables so you don't have to type anything
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export PASSPHRASE=""

# Your GPG key
#GPG_KEY=

# The S3 destination followed by bucket name
BASE_BUCKET="s3://s3.amazonaws.com/softproekt.gamaun.us"


# Set up some variables for logging
#LOGFILE="/var/log/duplicity/backup.log"
DAILYLOGFILE="/var/log/duplicity/backup.daily.log"
FULLBACKLOGFILE="/var/log/duplicity/backup.full.log"
HOST=`hostname`
DATE=`date +%Y-%m-%d`
MAILADDR="sunnystas@gmail.com"
TODAY=$(date +%d%m%Y)
OLDER_THAN="3M"
VOLSIZE="256"
FULL=

SRC_SRV="/srv"
SRC_SQL="/mnt/sql"
SRC_UPLOADS="/srv/gam/uploads"
SRC_ETC_POSTGRES="/etc/postgresql"
SRC_CRONTABS="/var/spool/cron/crontabs"
SRC_USR_SHARE_POSTGRES="/usr/share/postgresql"

DEST_SRV=${BASE_BUCKET}/filesystem_bkp/srv/
DEST_SQL=${BASE_BUCKET}/filesystem_bkp/sql/
DEST_UPLOADS=${BASE_BUCKET}/filesystem_bkp/srv_gam_uploads/
DEST_ETC_POSTGRES=${BASE_BUCKET}/filesystem_bkp/etc_postgresql/
DEST_CRONTABS=${BASE_BUCKET}/filesystem_bkp/var_spool_cron_crontabs/
DEST_USR_SHARE_POSTGRES=${BASE_BUCKET}/filesystem_bkp/usr_share_postgresql/


is_running=$(ps -ef | grep duplicity  | grep python | wc -l)

if [ ! -d /var/log/duplicity ];then
    mkdir -p /var/log/duplicity
fi

if [ ! -f $FULLBACKLOGFILE ]; then
    touch $FULLBACKLOGFILE
fi

if [ $is_running -eq 0 ]; then
    # Clear the old daily log file
    cat /dev/null > ${DAILYLOGFILE}

    # Trace function for logging, don't change this
    trace () {
            stamp=`date +%Y-%m-%d_%H:%M:%S`
            echo "$stamp: $*" >> ${DAILYLOGFILE}
    }

#    tail -1 ${FULLBACKLOGFILE} | grep ${TODAY} > /dev/null
#    if [ $? -ne 0 -a $(date +%d) -eq 1 ]; then
    if [ "`date +%d`" -eq '1' ] && [ "`date +%H`" -eq '0' ]; then
        FULL=full
    fi;

    trace "Backup for local filesystem started"

    trace "... removing old backups"

    duplicity remove-older-than ${OLDER_THAN} ${DEST_SRV} >> ${DAILYLOGFILE} 2>&1
    duplicity remove-older-than ${OLDER_THAN} ${DEST_SQL} >> ${DAILYLOGFILE} 2>&1
    duplicity remove-older-than ${OLDER_THAN} ${DEST_UPLOADS} >> ${DAILYLOGFILE} 2>&1
    duplicity remove-older-than ${OLDER_THAN} ${DEST_ETC_POSTGRES} >> ${DAILYLOGFILE} 2>&1
    duplicity remove-older-than ${OLDER_THAN} ${DEST_CRONTABS} >> ${DAILYLOGFILE} 2>&1
    duplicity remove-older-than ${OLDER_THAN} ${DEST_USR_SHARE_POSTGRES} >> ${DAILYLOGFILE} 2>&1

    trace "... backing up filesystem"

    duplicity \
        ${FULL} \
	--volsize ${VOLSIZE} \
	--exclude=${SRC_UPLOADS} \
        ${SRC_SRV} ${DEST_SRV} >> ${DAILYLOGFILE} 2>&1

    duplicity \
        ${FULL} \
        --volsize ${VOLSIZE} \
        ${SRC_SQL} ${DEST_SQL} >> ${DAILYLOGFILE} 2>&1

    duplicity \
        ${FULL} \
	--volsize ${VOLSIZE} \
        ${SRC_UPLOADS} ${DEST_UPLOADS} >> ${DAILYLOGFILE} 2>&1

    duplicity \
        ${FULL} \
	--volsize ${VOLSIZE} \
        ${SRC_ETC_POSTGRES} ${DEST_ETC_POSTGRES} >> ${DAILYLOGFILE} 2>&1

    duplicity \
        ${FULL} \
	--volsize ${VOLSIZE} \
        ${SRC_CRONTABS} ${DEST_CRONTABS} >> ${DAILYLOGFILE} 2>&1

    duplicity \
        ${FULL} \
	--volsize ${VOLSIZE} \
        ${SRC_USR_SHARE_POSTGRES} ${DEST_USR_SHARE_POSTGRES} >> ${DAILYLOGFILE} 2>&1

    trace "Backup for local filesystem complete"
    trace "------------------------------------"

    # Send the daily log file by email
    #cat "$DAILYLOGFILE" | mail -s "Duplicity Backup Log for $HOST - $DATE" $MAILADDR
    BACKUPSTATUS=`cat "$DAILYLOGFILE" | grep Errors | awk '{ print $2 }'`
    if [ "$BACKUPSTATUS" != "0" ]; then
	   cat "$DAILYLOGFILE" | mail -s "Duplicity Backup Log for $HOST - $DATE" $MAILADDR
    elif [ "$FULL" = "full" ]; then
        echo "$(date +%d%m%Y_%T) Full Back Done" >> $FULLBACKLOGFILE
    fi

    # Append the daily log file to the main log file
    cat "$DAILYLOGFILE" >> $FULLBACKLOGFILE

    # Reset the ENV variables. Don't need them sitting around
    unset AWS_ACCESS_KEY_ID
    unset AWS_SECRET_ACCESS_KEY
    unset PASSPHRASE
fi
