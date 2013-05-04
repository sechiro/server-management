#-*- coding:utf-8 -*-
from fabric import api
from fabric.api import run, sudo, put, env
from fabric.decorators import hosts, roles, task
import os

# import fabric tasks
import init_user
import vmware
import os_init

@task
def printenv():
    """ Print ALL env variables """
    print env
    print env.host

def restart():
    sudo('shutdown -ry now')
