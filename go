#! /bin/bash

set -e

action=$1
dir=`dirname $0`

activate_virtualenv() {
  if [[ -z $VIRTUAL_ENV ]]; then
    echo -e "\e[33m★\e[39m Activating virtualenv"
    source $dir/venv/bin/activate
  fi
}

setup() {
  if [[ -d $dir/venv/ ]]; then
    echo -e "\e[33m★\e[39m Removing old virtualenv"
    rm -rf $dir/venv/
  fi

  echo -e "\e[33m★\e[39m Setting up virtualenv"
  pip install virtualenv
  virtualenv $dir/venv

  activate_virtualenv

  echo -e "\e[33m★\e[39m Installing Python dependencies"
  pip install -r $dir/requirements.txt
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
