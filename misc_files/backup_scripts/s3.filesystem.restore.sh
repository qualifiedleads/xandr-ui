#! /bin/bash
#### Restore directories of local file system from AWS S3 ####
# test user read only policy here


export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export PASSPHRASE=""

#export AWS_ACCESS_KEY_ID="AKIAI5VWTERJIAIBSSUA"
#export AWS_SECRET_ACCESS_KEY="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"

BASE_BUCKET="s3://s3.amazonaws.com/softproekt.gamaun.us"

if [ $# -lt 2 ];
  then
    echo "Usage $0 <remote-file-path-with-folder> <restore-to-path>"; exit;
fi

duplicity \
    ${BASE_BUCKET}$1 $2

unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset PASSPHRASE
