#!/bin/bash
rm -r ~/htdocs
ln -s /opt/bitnami/apache2/htdocs /home/bitnami/htdocs
cp ../* ~/htdocs
cp -r ../images ~/htdocs
sudo /opt/bitnami/ctlscript.sh restart apache
