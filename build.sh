#!/bin/bash

sudo apt-get update -qy
sudo apt-get install -y dpkg-dev python3-pip
pip3 install -r requirements.txt
pip3 list
export PATH="/usr/bin/python3:$PATH"
pip install pyinstaller
pyinstaller --onefile opengui_src/opengui.py
mkdir -p ${PACKAGE_NAME}_${PACKAGE_VERSION}_all/DEBIAN
mkdir -p ${PACKAGE_NAME}_${PACKAGE_VERSION}_all/usr/bin
mkdir -p ${PACKAGE_NAME}_${PACKAGE_VERSION}_all/usr/share/opengui/svg
cp dist/opengui ${PACKAGE_NAME}_${PACKAGE_VERSION}_all/usr/bin/opengui
cp -R opengui_package_template/DEBIAN/* ${PACKAGE_NAME}_${PACKAGE_VERSION}_all/DEBIAN/ -v
cp -R usr/share/* ${PACKAGE_NAME}_${PACKAGE_VERSION}_all/usr/share/
dpkg-deb --build ${PACKAGE_NAME}_${PACKAGE_VERSION}_all
ls -la
