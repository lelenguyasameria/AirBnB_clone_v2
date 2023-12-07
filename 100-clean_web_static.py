#!/usr/bin/python3
"""module for do_clean funtion """

from fabric.api import local, run

env.user = 'ubuntu'
env.hosts = ['18.215.160.22', '35.175.129.140']


def do_clean(number=0):
    """ deletes archives
    args:
         number(int): number of archives to keep
    """
    number = int(number)
    if number != 0:
        number += 1
    else:
        number = 2

    local('cd versions')
    local(f"ls -t | tail -n +{number} | xargs rm -rf")
    run('cd /data/web_static/releases')
    run(f"ls -t | tail -n +{number} | xargs rm -rf")
