#!/usr/bin/env bash

cd ..
rsync -av --exclude '.git' --exclude '.pyc' --exclude 'venv' tiny-statistical-data root@120.24.71.96:/data/wwwroot/
