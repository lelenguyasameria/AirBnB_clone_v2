#!/usr/bin/env bash
# Script to set up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file
echo "<html><head></head><body>Test Page</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership recursively to the ubuntu user and group
sudo chown -R lelenguya:lelenguya /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
nginx_server_name="server_name codesammy.tech;"
nginx_alias_config="location /hbnb_static { alias /data/web_static/current/; }"

# Check if the server_name is already configured
if ! grep -q "$nginx_server_name" "$nginx_config"; then
    # Add server_name if it doesn't exist
    sudo sed -i "/^\s*listen.*/a $nginx_server_name" "$nginx_config"
fi

# Check if the /hbnb_static alias is already configured
if ! grep -q "$nginx_alias_config" "$nginx_config"; then
    # Add /hbnb_static alias configuration
    sudo sed -i "/^\s*server_name.*/a $nginx_alias_config" "$nginx_config"
fi

# Restart Nginx
sudo service nginx restart

exit 0

