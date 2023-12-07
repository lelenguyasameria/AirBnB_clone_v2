#!/usr/bin/env bash
""" module for fabric functions do_pack, do_deploy """

from fabric.api import local, run, put, env
from datetime import datetime
from os.path import exists

env.user = 'ubuntu'
env.hosts = ['18.215.160.22', '35.175.129.140']


def do_pack():
    """ generates a .tgz archive from the contents of the web_static folder """
    try:
        local('mkdir -p versions')
        time = datetime.now().strftime('%Y%m%d%H%M%S')
        path = f'versions/web_static_{time}.tgz'
        local(f"tar -cvzf {path} web_static/")
        return path
    except Exception:
        return None


def do_deploy(archive_path):
    """ uploads archives to remote server """
    if not exists(archive_path):
        return False
    try:
        file = archive_path[9:]
        new = f'/data/web_static/releases/{file[:-4]}'
        path = '/tmp/' + file
        put(archive_path, '/tmp/')
        run(f'sudo mkdir -p {new}')
        run(f'sudo -xzf {file} -C {new}')
        run(f'sudo rm {file}')
        run(f'sudo mv {new}/web_static/* {new}')
        run(f'sudo rm -rf {new}/web_static')
        run(f'sudo rm -rf /data/web_static/current')
        run(f'sudo -ls {new} /data/web_static/current')
        return True
    except Exception:
        return False
