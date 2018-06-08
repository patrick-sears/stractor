#!/bin/bash


wd=`pwd -P`

cd "$HOME/bin"


if [[ -e "prs-stractor" ]]; then
  rm "prs-stractor"
fi

if [[ -e "prs-stractor_d" ]]; then
  rm "prs-stractor_d"
fi


ln -sf "$wd/aas" "prs-stractor"
ln -sf "$wd" "prs-stractor_d"





