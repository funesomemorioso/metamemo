#!/bin/bash

# This script:
# - Downloads $filename from storage.metamemo.info
# - Uploads file to local MinIO

filename="$1"

defaultfoldername="media"
foldername="${2:-$defaultfoldername}"

if [[ -z $filename ]]; then
 echo "ERROR - Usage: $0 <filename> <foldername>"
 exit 1
fi

bucket=$AWS_STORAGE_BUCKET_NAME
endpoint=$(echo $AWS_S3_ENDPOINT_URL | sed 's/\/$//')
host=$(echo $AWS_S3_ENDPOINT_URL | sed 's/https\?:\/\///; s/\/.*//')
s3_key=$AWS_S3_ACCESS_KEY_ID
s3_secret=$AWS_S3_SECRET_ACCESS_KEY

mkdir -p $foldername
rm -rf "${foldername}/${filename}"
curl --output "${foldername}/${filename}" https://storage.metamemo.info/${bucket}/${foldername}/${filename}

resource="/${bucket}/${foldername}/${filename}"
content_type="application/octet-stream"
date=`date -R`
_signature="PUT\n\n${content_type}\n${date}\n${resource}"
signature=`echo -en ${_signature} | openssl sha1 -hmac ${s3_secret} -binary | base64`

curl -X PUT -T "${foldername}/${filename}" \
          -H "Host: ${host}" \
          -H "Date: ${date}" \
          -H "Content-Type: ${content_type}" \
          -H "Authorization: AWS ${s3_key}:${signature}" \
          "${endpoint}${resource}"
