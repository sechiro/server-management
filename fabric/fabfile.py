#-*- coding:utf-8 -*-
from fabric import api
from fabric.api import run, sudo, put, env
from fabric.decorators import hosts, roles, task
import os

# import fabric tasks
import init_user
import vmware
import os_init

env.roledefs={"server":["webserver.local"],"workstation":["10.10.10.10"]}

@hosts('10.0.0.1')
def printenv():
    """ Print ALL env variables """
    print env
    print env.host

def deploy_vmwaretools(archive_name='../../resources/VMwareTools.tar.gz',work_dir='/tmp'):
    """ fab deploy_vmwaretools:host=192.168.11.201 """
    env.user = 'root'
    archive_file = os.path.basename(archive_name)
    put_vmwaretools()
    api.run('ls %s' % work_dir)
    with api.cd(work_dir):
        api.run('tar xf ' + archive_file)
    with api.cd('%s/vmware-tools-distrib' % work_dir):
        api.sudo('./vmware-install.pl')

def put_vmwaretools(archive_name='../../resources/VMwareTools.tar.gz',work_dir='/tmp'):
    """ fab put_vmwaretools:archive_name=VMwareTools,work_dir=/tmp,host:192.168.11.201 """
    # Default: Symblic Link of VMwareTools archive
    put(archive_name, work_dir)
    run('ls %s' % work_dir)

def add_ssh_nodns():
    api.sudo('echo "UseDNS no" >> /etc/ssh/sshd_config')
    api.sudo('tail','/etc/ssh/sshd_config')
    api.sudo('sudo service ssh restart')

def add_nopass_sudo():
    config_file = 'sechiro-nopass'
    api.sudo('echo "sechiro ALL=(ALL)       NOPASSWD: ALL" > /etc/sudoers.d/' + config_file)
    api.sudo('chmod 440 /etc/sudoers.d/' + config_file)
    api.sudo('ls -l /etc/sudoers.d/')
    api.sudo('cat /etc/sudoers.d/' + config_file)

def install_gcc():
    api.sudo('apt-get -y install gcc')

def update():
    api.sudo('apt-get -y update')

def restart():
    api.sudo('shutdown -ry now')

def command_test():
    api.put('testfile', '/tmp')
    api.sudo('echo test > /tmp/testfile2')
    api.run('ls -l /tmp')

def set_vim():
    api.sudo('update-alternatives --set editor /usr/bin/vim.basic')

def initial_setting():
    set_vim()
    add_nopass_sudo()
    install_gcc()
    update()
    #restart()
