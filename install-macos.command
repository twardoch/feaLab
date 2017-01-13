#!/usr/bin/env bash

dir=${0%/*}
if [ "$dir" = "$0" ]; then
  dir="."
fi
cd "$dir"

# Check if Homebrew is installed
if [ ! -x "$(which brew)" ]; then
	echo "# You must install Homebrew first!"
	open "http://brew.sh/"
	exit 1
fi

# Install harfbuzz if needed
if [ ! -x "$(which hb-view)" ]; then
	echo "# Install 'harfbuzz'"
	brew install harfbuzz
else
	echo "# 'harfbuzz' is installed."
fi 

# Install me
echo "# Install 'feaLab'"
pip install --user --upgrade -r py-requirements.txt
pip install --user --upgrade .
echo "# Done!"

