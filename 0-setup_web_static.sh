#!/usr/bin/env bash
# Bash script that sets up web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx

sudo mkdir -p /data/web_static/releases/test/i
sudo mkdir -p /data/web_static/shared/

printf %s "<!DOCTYPE html>
<html>
	<head>
	</head>
	<body>
		Holberton School
	</body>
</html>
" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data

sudo sed -i '23i location /hbnb_static {\n\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-enabled/default

sudo service nginx restart
