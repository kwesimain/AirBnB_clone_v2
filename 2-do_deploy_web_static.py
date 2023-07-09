#!/usr/bin/python3
"""
Web server deployment
"""
from fabric.api import env, put, run
import os


# Define the web server IP addresses
env.hosts = ['3.84.239.171', '52.87.222.81']


def do_deploy(archive_path):
    """Distributes an archive to your web servers and deploys it."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/<archive filename without extension> on the web server
        archive_filename = os.path.basename(archive_path)
        archive_folder = '/data/web_static/releases/{}'.format(os.path.splitext(archive_filename)[0])
        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, archive_folder))

        # Remove the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted folder to a new location
        run('mv {}/web_static/* {}'.format(archive_folder, archive_folder))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(archive_folder))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current linked to the new version of your code
        run('ln -s {} /data/web_static/current'.format(archive_folder))

        return True
    except:
        return False

