#!/usr/bin/env bash

cd ..
rsync -av --exclude '.git' --exclude '.pyc' --exclude '__pycache__' --exclude 'TAGS' --exclude 'venv' tiny_statistical_data root@120.24.71.96:/data/wwwroot/
