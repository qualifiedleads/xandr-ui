#! /bin/bash
#### Upload to AWS S3 ####
  #set -x

#  PATH=$PATH:"/usr/bin/aws"

  if [ $# -lt 2 ];
    then echo "Usage $0 <local base folder> <s3 bucket folder>"; exit;
  fi

  if [ ! -d /var/log/backup ];then
      mkdir -p /var/log/backup
  fi

  export AWS_ACCESS_KEY_ID=""
  export AWS_SECRET_ACCESS_KEY=""
  export PASSPHRASE=""

  # base dir - directory for backups
  BASE_DIR=$1

  # bucket folder - remote bucket where we want to upload to
  BUCKET_FOLDER=$2

  #loogs paths
  LOGFILE="/var/log/backup/s3.upload.log"
  DAILYLOGFILE="/var/log/backup/s3.upload.daily.log"

  #other variables
  HOST=`hostname`
  DATE=`date +%Y-%m-%d`
  MAILADDR="sunnystas@gmail.com"
  TODAY=$(date +%d%m%Y)

  # The S3 destination followed by bucket name
  BASE_BUCKET="s3://softproekt.gamaun.us"



  # Clear the old daily log file
  cat /dev/null > ${DAILYLOGFILE}

  # Trace function for logging, don't change this
  trace () {
    stamp=`date +%Y-%m-%d_%H:%M:%S`
    echo "$stamp: $*" >> ${DAILYLOGFILE}
  }

  trace "Uploading to S3...."

  ls $BASE_DIR -1r | while read LINE
  do
    trace "Upload $BASE_DIR/$LINE"
    aws s3 mv $BASE_DIR/$LINE ${BASE_BUCKET}${BUCKET_FOLDER}/ >> ${DAILYLOGFILE} 2>&1
    ERR_CODE=$?
  done

  trace "Finished uploading to S3."


  unset AWS_ACCESS_KEY_ID
  unset AWS_SECRET_ACCESS_KEY
  unset PASSPHRASE

  # Append the daily log file to the main log file
  cat "$DAILYLOGFILE" >> $LOGFILE

  exit $ERR_CODE
