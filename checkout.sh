#!/bin/bash
#$1 - url to git repo
#$2 - directory with repo files (created after download)
#$3 - branch to download files
#$4 - directory or file to download
git clone --no-checkout "$1"
cd "$2"
git sparse-checkout init --cone
git sparse-checkout set "$4"
git checkout "$3"