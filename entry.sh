#!/bin/bash
set -euo pipefail
help_and_exit() {
    echo "       <path-to-script> worker <job-file-without-extension>"
    exit 1
}

if [ "$#" -lt 1 ]; then
    help_and_exit
fi


JOB_MODULE="$2"
exec python3.9 -m "worker.$JOB_MODULE"
