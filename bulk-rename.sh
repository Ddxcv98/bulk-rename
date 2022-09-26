#!/bin/bash

if [ -z "$EDITOR" ]
then
    vim="$(whereis vim | awk '{ print $2 }')"

    if [ -z "$vim" ]
    then
        echo 'EDITOR variable not set' 1>&2
        exit 1
    fi

    export EDITOR="$vim"
fi

python "$(dirname "$0")/src/main.py" "$@"
