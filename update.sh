#!/bin/env bash
REPO_URL="https://github.com/n3tworkh4x/xharvestor.git"
DIR="xharvestor"
BRANCH="main" 

if [ -d "$DIR" ] && [ -d "$DIR/.git" ]; then
  cd "$DIR" || exit
  git fetch origin
  git reset --hard origin/$BRANCH
  git clean -fd
else
  echo "Cloning repository..."
  git clone "$REPO_URL"
  cd "$DIR" || exit
fi

