#!/usr/bin/env bash
# Only for development

# source setup.sh
export DIR_PWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$PYTHONPATH:$DIR_PWD"

echo $PYTHONPATH
