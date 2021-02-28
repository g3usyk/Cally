#!/bin/bash
VERSION_PREFIX=$(sed -n '4p' __init__.py | cut -c17-23 | sed 's/,/_/g; s/ //g; s/^/v/g')
VERSION_NAME="cally_${VERSION_PREFIX}"
mkdir -p dist
rm -rf dist/*
mkdir dist/"${VERSION_NAME}"
cp ./__init__.py dist/"${VERSION_NAME}"
cp -r ./src dist/"${VERSION_NAME}"
cd ./dist || return
zip -r "${VERSION_NAME}".zip "${VERSION_NAME}"
cd ..