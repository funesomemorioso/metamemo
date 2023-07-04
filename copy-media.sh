#!/bin/bash

# This script:
# - Downloads $filename from storage.metamemo.org.br
# - Uploads file to local MinIO

filename="$1"

if [[ -z $filename ]]; then
 echo "ERROR - Usage: $0 <filename>"
 exit 1
fi

bucket=$AWS_STORAGE_BUCKET_NAME
endpoint=$(echo $AWS_S3_ENDPOINT_URL | sed 's/\/$//')
host=$(echo $AWS_S3_ENDPOINT_URL | sed 's/https\?:\/\///; s/\/.*//')
s3_key=$AWS_S3_ACCESS_KEY_ID
s3_secret=$AWS_S3_SECRET_ACCESS_KEY

full_filename="/tmp/mtm-tmp/${filename}"
mkdir -p $(dirname $full_filename)
rm -rf "$full_filename"
curl --output "$full_filename" https://storage.metamemo.org.br/${bucket}/${filename}

resource="/${bucket}/${filename}"
content_type="application/octet-stream"
date=`date -R`
_signature="PUT\n\n${content_type}\n${date}\n${resource}"
signature=`echo -en ${_signature} | openssl sha1 -hmac ${s3_secret} -binary | base64`

curl -X PUT -T "$full_filename" \
          -H "Host: ${host}" \
          -H "Date: ${date}" \
          -H "Content-Type: ${content_type}" \
          -H "Authorization: AWS ${s3_key}:${signature}" \
          "${endpoint}${resource}"
