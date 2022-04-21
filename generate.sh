#!/bin/bash

##############################################
#
#   Creating mailboxes for test python script
#
##############################################

MAILBOXES=`cat mailboxes.txt`
CUR_DIR=`pwd`
MB_DIR="$CUR_DIR/mail/mail.ru"

echo $CUR_DIR
echo $MB_DIR

for mb in $MAILBOXES
do
  MB_PATH=$MB_DIR/$mb
  echo "Path for mailbox - ${MB_PATH}"
  if [ ! -d $MB_PATH ]; then
    mkdir -p $MB_PATH
    echo "..... Creating .... ${MB_PATH}"
  else
    echo "..... Directory existing"
  fi
done

echo "    DONE"
