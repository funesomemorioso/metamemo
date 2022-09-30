#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

celery --app metamemo worker --beat --loglevel info
