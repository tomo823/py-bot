#!/bin/bash

curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash

echo 'export PATH=$PATH:$(npm bin -g)' >> ~/.bashrc
echo 'source "$HOME/.rye/env"' >> ~/.bashrc
. "$HOME/.rye/env"
