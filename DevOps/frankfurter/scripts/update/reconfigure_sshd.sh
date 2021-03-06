#!/bin/bash

FRANKFURTER_DIR=$(git rev-parse --show-toplevel)/DevOps/frankfurter
USER=ubuntu
IP=192.168.7.2

cd $FRANKFURTER_DIR

IDENTITY_PATH=~/.ssh/frankfurter_seiya
if [ -e $IDENTITY_PATH ]; then
  chmod 600 $IDENTITY_PATH
  echo "Restricted identity file permissions to user read/write."
else
  echo -e "\x1b[1;31m'$IDENTITY_PATH' does not exist.\x1b[0m"
  exit
fi

OPTIONS="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
OPTIONS="$OPTIONS -o IdentityFile=$IDENTITY_PATH"

CMD="cp /etc/ssh/sshd_config ~/sshd_config.bak"
CMD="$CMD && sudo mv ~/sshd_config /etc/ssh"
CMD="$CMD && sudo restart ssh"

scp $OPTIONS resources/sshd_config $USER@$IP:~
ssh $OPTIONS $USER@$IP $CMD
