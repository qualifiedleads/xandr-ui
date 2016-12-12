#! /bin/bash
#### Download from AWS S3 ####

  #set -x

#  PATH=$PATH:"/usr/local/bin/aws"

  if [ $# -lt 2 ];
    then echo "Usage $0 <s3 remote file path with folder> <local file path>"; exit;
  fi

  if [ ! -d /var/log/backup ];then
      mkdir -p /var/log/backup
  fi

  export AWS_ACCESS_KEY_ID=""
  export AWS_SECRET_ACCESS_KEY=""
  export PASSPHRASE=""

  # base dir - directory for backups
  REMOTE_FILE_PATH=$1

  # bucket folder - remote bucket where we want to upload to
  LOCAL_FILE_PATH=$2

  #loogs paths
  LOGFILE="/var/log/backup/s3.download.log"

  #other variables
  HOST=`hostname`
  DATE=`date +%Y-%m-%d`
  MAILADDR="sunnystas@gmail.com"
  TODAY=$(date +%d%m%Y)

  # The S3 destination followed by bucket name
  BASE_BUCKET="s3://softproekt.gamaun.us"

  # Trace function for logging, don't change this
  trace () {
    stamp=`date +%Y-%m-%d_%H:%M:%S`
    echo "$stamp: $*" >> ${LOGFILE}
  }

  trace "Uploading to S3...."

  trace "Download ${BASE_BUCKET}${REMOTE_FILE_PATH}"
  aws s3 cp ${BASE_BUCKET}${REMOTE_FILE_PATH} ${LOCAL_FILE_PATH} >> ${LOGFILE} 2>&1
  ERR_CODE=$?

  trace "Finished downloading from S3."

  unset AWS_ACCESS_KEY_ID
  unset AWS_SECRET_ACCESS_KEY
  unset PASSPHRASE

  exit $ERR_CODE
