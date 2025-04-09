#! /bin/bash

cd $1
git pull origin master --rebase
sudo systemctl restart $2
