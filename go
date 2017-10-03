#! /bin/bash

set -e

action=$1
dir=`dirname $0`

activate_virtualenv() {
  if [[ -z $VIRTUAL_ENV ]]; then
    echo -e "\033[33m★\033[39m Activating virtualenv"
    source $dir/venv/bin/activate
  fi
}

setup() {
  if [[ -d $dir/venv/ ]]; then
    echo -e "\033[33m★\033[39m Removing old virtualenv"
    rm -rf $dir/venv/
  fi

  echo -e "\033[33m★\033[39m Setting up virtualenv"
  pip install virtualenv
  virtualenv -p python3 $dir/venv

  activate_virtualenv

  echo -e "\033[33m★\033[39m Installing Postgresql"
  # sudo apt install postgresql

  echo -e "\033[33m★\033[39m Installing sass"
  gem install sass

  echo -e "\033[33m★\033[39m Installing Python dependencies"
  pip install -r $dir/requirements.txt
  gem install sass

  echo -e "\033[33m★\033[39m Installing node dependencies"
  npm install
}

if [[ $action == "setup" ]]; then
  setup
  exit 0;
fi

if [[ ! -d $dir/venv/ ]]; then
  setup
fi

activate_virtualenv
./go.py $@
