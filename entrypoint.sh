#!/bin/bash

[ -v ENVIRONMENT ] && export ENVIRONMENT=$ENVIRONMENT || export ENVIRONMENT=$OPENSHIFT_BUILD_REFERENCE

if [[ ${ENVIRONMENT} = 'LOCAL' ]]; then
    exec uvicorn asgi:app --log-level=info --host 0.0.0.0 --port 8000 --workers 2 --no-access-log
else
    exec uvicorn asgi:app --log-level=info --host 0.0.0.0 --port 8000 --workers 2 --no-access-log
fi
