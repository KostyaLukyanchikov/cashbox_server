#!/bin/bash

[ -v ENVIRONMENT ] && export ENVIRONMENT=$ENVIRONMENT || export ENVIRONMENT=$OPENSHIFT_BUILD_REFERENCE

if [[ ${ENVIRONMENT} = 'LOCAL' ]]; then
    exec uvicorn asgi:app --log-level=info --host 0.0.0.0 --port 8000 --ws-ping-interval=70 --ws-ping-timeout=60 --workers 1 --no-access-log
else
    exec uvicorn asgi:app --log-level=info --host 0.0.0.0 --port 8000 --ws-ping-interval=70 --ws-ping-timeout=60 --workers 1 --no-access-log
fi
