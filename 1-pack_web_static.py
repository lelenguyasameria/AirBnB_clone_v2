#!/usr/bin/python3
"""
Fabric script to automate the deployment process.
"""

from fabric import task
from datetime import datetime
import os

# Define timestamp as a global variable
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

@task
def do_pack(c):
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        - Archive path if successfully generated.
        - None if there was an error.
    """
    try:
        # Create the "versions" folder if it doesn't exist
        c.run("mkdir -p versions")

        # Generate archive filename using current timestamp
        archive_name = "web_static_{}.tgz".format(timestamp)

        # Create the .tgz archive
        c.run("tar -czvf versions/{} web_static".format(archive_name))

        # Return the archive path
        return os.path.join("versions", archive_name)
    except Exception as e:
        print("Error:", e)
        return None

@task
def deploy(c):
    """
    Deploys the web_static content to the servers.
    """
    archive_path = do_pack(c)
    if archive_path:
        # Upload the archive to the server
        c.put(archive_path, "/tmp/")

        # Extract the contents of the archive
        c.run("mkdir -p /data/web_static/releases/")
        c.run("tar -xzf /tmp/{} -C /data/web_static/releases/".format(os.path.basename(archive_path)))

        # Create a symbolic link
        c.run("rm -rf /data/web_static/current")
        c.run("ln -s /data/web_static/releases/{} /data/web_static/current".format(timestamp))

# Ensure this script is executable

