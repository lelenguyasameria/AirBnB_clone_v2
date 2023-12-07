#!/usr/bin/env bash
""" module for fabric function do_pack """

from fabric.api import local
from datetime import datetime


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
