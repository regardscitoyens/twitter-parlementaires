#!/bin/bash

sudo apt-get install pip
sudo pip install virtualenv virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv --no-site-packages twitter-parls
workon twitter-parls
pip install -r requirements.txt
add2virtualenv .
deactivate

echo
echo
echo "Installation complete!"

if ! test -e twitterconfig.py; then
  cp twitterconfig.py{.example,}
  echo
  echo "Please edit twitterconfig.py and set your Twitter API credentials"
fi

echo
echo "Add to your crontab a line such as the following to automatically update evry hour:"
echo "00 * * * * "$(dirname $0)"/bin/update.sh"

