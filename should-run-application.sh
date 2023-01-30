#!/usr/bin/env bash

echo "foo"
echo $CIRCLE_SHA1
echo $CIRCLE_BASE_REVISION
echo "Files changes:"
CHANGED=`git diff --name-only $CIRCLECI_SHA $CIRCLE_BASE_REVISION`
CHANGES_OTHER_THAN_IMPORTS=`echo $CHANGED | grep -v imports`
if [ CHANGES_OTHER_THAN_IMPORTS ]; then
  echo "DO THE APPLICATION DEPLOYMENT!!!!!!"
else
  echo "SKIP THE DEPLOYMENT
fi
