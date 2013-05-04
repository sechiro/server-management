#-*- coding:utf-8 -*-
from fabric import api
from fabric.api import run, sudo, put, env, settings
from fabric.decorators import hosts, roles, task
import os

@task(default=True)
def deploy_vmwaretools(user=env.user,archive_name='../../resources/VMwareTools.tar.gz',work_dir='/tmp'):
    """ [idem] fab deploy_vmwaretools:user=root """
    env.user = user
    archive_file = os.path.basename(archive_name)
    result = check_install()
    if result.failed:
        put_vmwaretools(user)
        run('ls %s' % work_dir)
        with api.cd(work_dir):
            sudo('tar xf ' + archive_file)
        with api.cd('%s/vmware-tools-distrib' % work_dir):
            sudo('yes "" | ./vmware-install.pl')
    else:
        print 'VMware Tools is already installed.'

@task
def put_vmwaretools(user=env.user,archive_name='../../resources/VMwareTools.tar.gz',work_dir='/tmp'):
    """ [idem] fab put_vmwaretools:archive_name=VMwareTools.tar.gz,work_dir=/tmp,host:192.168.11.201 """
    archive_file = os.path.basename(archive_name)
    with settings(warn_only=True):
        result = run('ls -l %s' % work_dir + '/' + archive_file, quiet=True)
        if result.failed:
            put(archive_name, work_dir)
            run('ls -l %s' % work_dir)

@task
def check_install():
    """ [idem] Check VMware tools uninstaller file. """
    uninstall_bin = '/usr/bin/vmware-uninstall-tools.pl'
    with settings(warn_only=True):
        result = run('ls -l %s' % uninstall_bin)
    return result
