#-*- coding:utf-8 -*-
from fabric import api
from fabric.api import run, sudo, put, env, settings, local
from fabric.decorators import hosts, roles, task
import os

@task
def add_ssh_nodns():
    result = check_nodns()
    if result.failed:
        sudo('echo "UseDNS no" >> /etc/ssh/sshd_config')
        sudo('tail','/etc/ssh/sshd_config')
        sudo('sudo service ssh restart')

@task
def check_nodns():
    with settings(warn_only=True):
        result = sudo('grep "UseDNS no" /etc/ssh/sshd_config')
    return result

@task
def install_gcc():
    sudo('apt-get -y install gcc')

@task
def update():
    sudo('apt-get -y update')

@task
def restart():
    sudo('shutdown -ry now')

@task
def set_vim():
    api.sudo('update-alternatives --set editor /usr/bin/vim.basic')

@task(default=True)
def initial_setting():
    """ [idem] fab os_init.ubuntu -u sechiro -H 192.168.11.100 """
    add_ssh_nodns()
    set_vim()
    install_gcc()
    update()
    #restart()
