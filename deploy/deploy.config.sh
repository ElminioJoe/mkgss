#!/bin/bash

# Configuration
PROJECT_NAME="kadzonzo"
PROJECT_DIR="$HOME/school-website/"
VENV_DIR="$HOME/school-website/.venv/$PROJECT_NAME"
VASSALS_DIR="$VENV_DIR/vassals"
SOCKET_FILE="$PROJECT_DIR/$PROJECT_NAME.sock"
UWSGI_CONFIG_FILE="$PROJECT_DIR/deploy/uwsgi.ini"
UWSGI_SERVICE_FILE="/etc/systemd/system/emperor.uwsgi.service"
NGINX_CONFIG_FILE="/etc/nginx/sites-available/$PROJECT_NAME.conf"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"
PYTHON_VERSION=$(python3 -c "import sys; print(sys.version.split(' ')[0][:3])")

# Function to display error messages and exit
function error_exit {
    echo "Error: $1" >&2
    exit 1
}

# Update system packages
sudo apt-get update || error_exit "Failed to update system packages."

# Install necessary packages
sudo apt-get install -y python3-venv python$PYTHON_VERSION-dev gcc nginx || error_exit "Failed to install necessary packages."

python3 -m venv $VENV_DIR || error_exit "Failed to create a virtual environment."
# Activate the Virtual environment
source $VENV_DIR/bin/activate || error_exit "Failed to activate virtual environment."

# Install project requirements
pip install -r $PROJECT_DIR/requirements.txt uwsgi || error_exit "Failed to install project requirements."

# Convert static asset files
python3 $PROJECT_DIR/manage.py collectstatic --no-input || error_exit "Failed to collect statics assets."

# Apply any outstanding database migrations
python3 $PROJECT_DIR/manage.py migrate || error_exit "Failed to apply database migrations."
# deactivate the virtual env
deactivate

# Configure uWSGI
cat <<EOF >$UWSGI_CONFIG_FILE
[uwsgi]
chdir = $PROJECT_DIR
module = $PROJECT_NAME.wsgi:application
home = $VENV_DIR # path to python venv
master = true
processes = 5
socket = $SOCKET_FILE
chmod-socket = 666
vacuum = true
daemonize = $HOME/uwsgi-emperor.log
die-on-term = true
EOF

# Create systemd service file for uWSGI
sudo cat <<EOF >$UWSGI_SERVICE_FILE
[Unit]
Description=uWSGI Emperor service for kadzonzo website
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/uwsgi --emperor $VASSALS_DIR --uid www-data --gid www-data
Restart=always
KillSignal=SIGQUIT
Type=notify
# StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
EOF

# create a vassals instance and link it to the wsgi.ini file
mkdir $VASSALS_DIR
sudo ln -s $UWSGI_CONFIG_FILE $VASSALS_DIR

# Start and enable uWSGI service
sudo systemctl start emperor.uwsgi.service || error_exit "Failed to start uWSGI service."
sudo systemctl enable emperor.uwsgi.service || error_exit "Failed to enable uWSGI service."

# Configure Nginx
sudo cat <<EOF >$NGINX_CONFIG_FILE
upstream django {
    server unix://$PROJECT_DIR/deploy/$PROJECT_NAME.sock;
}

server {
    listen      80;
    server_name $SERVER_NAME;
    charset     utf-8;

    # max upload size
    client_max_body_size    75M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias $PROJECT_DIR/static;
    }
    location /static/ {
        alias $PROJECT_DIR/media;
    }

    location / {
        uwsgi_pass  django;
        include     $PROJECT_DIR/deploy/uwsgi_params;
    }
}
EOF

# Enable the Nginx server block
sudo ln -s $NGINX_CONFIG_FILE $NGINX_ENABLED_DIR || error_exit "Failed to enable Nginx server block."

# Test Nginx configuration
sudo nginx -t || error_exit "Nginx configuration test failed."

# Restart Nginx
sudo systemctl restart nginx || error_exit "Failed to restart Nginx."

echo "Django deployment with uWSGI and Nginx completed successfully."
