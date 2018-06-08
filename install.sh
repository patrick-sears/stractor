#!/bin/bash


wd=`pwd -P`

cd "$HOME/bin"


if [[ -e "prs-stractor" ]]; then
  rm "prs-stractor"
fi



ln -sf "$wd/stractor.py" "prs-stractor"





