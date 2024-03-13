#!/usr/bin/env bash

DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

BUNDLE="put"

cd ${DIR}/..
mkdir -p ${BUNDLE}
python3 -m pip download --platform=linux --only-binary=:all: power-user-tools -d ${BUNDLE}
tar cvzf ${BUNDLE}.tar.gz ${BUNDLE}

rm -rf ${BUNDLE}
