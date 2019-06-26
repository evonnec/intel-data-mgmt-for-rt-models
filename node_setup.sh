#!/bin/bash
echo ""
echo ""
echo "Cool, now we'll check if you have Node installed"
echo ""
echo ""

export HOME=`pwd`
export NVM_DIR=`pwd`/.nvm/


node_installed=`which node`
if [ $node_installed ]
then
  echo "Great! You already have Node."
else
  echo "Ah, seems like Node is missing. Let's install it now!"
  cd ~
  curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh -o install_nvm.sh
fi

bash install_nvm.sh
source ~/.profile
#source .bashrc
nvm install 10.12
nvm use 10.12
npm i -g yarn
echo "Great! Now you have `node -v` installed"
