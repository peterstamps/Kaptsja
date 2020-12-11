#!/bin/bash
# let command prompt disappear temporarily
myprompt = $PS1
PS1=""
python ./scripts/KaptsjaSite.py
echo ==========================
echo Kaptsja Web site started INFO
echo ============================
PS1=myprompt