from fabric.api import task, run, local, settings, env, sudo, put

@task
def adduser(user='sechiro'):
    env.user = 'root'
    result = check_user(user=user)
    if result.failed:
        run('useradd %s' % user)
    else:
        print 'User "%s" already exists!' % user

@task
def passwd(user='sechiro'):
    env.user = 'root'
    result = check_user(user=user)
    if result.failed:
        print 'User "%s" does not exist!' % user
    else:
        run('passwd %s' % user)

@task
def groupadd(user='sechiro'):
    env.user = 'root'
    result = check_user(user=user)
    if result.failed:
        print 'User "%s" does not exist!' % user
    else:
        run('usermod -a -G wheel %s' % user)

@task
def check_user(user='sechiro'):
    with settings(warn_only=True):
        result = run('id %s' % user, quiet=True)
        return result

@task
def add_sudoers(group='%wheel'):
    env.user = 'root'
    tempfile = '/tmp/wheel_nopass'
    result = check_sudoers(group=group)
    if result.failed:
        local('echo "%s ALL=(ALL) NOPASSWD: ALL" > %s' % (group, tempfile) )
        local('cat %s' % tempfile)
        put(tempfile, '/etc/sudoers.d/', mode=0440)
    else:
        print 'The sudoers setting of wheel group exists already.'
        print result.stdout

    local('rm %s' % tempfile )

@task
def check_sudoers(group='%wheel',conf='/etc/sudoers.d/wheel_nopass'):
    with settings(warn_only=True):
        result = run('ls -l %s' % conf, quiet=True)
        return result


@task(default=True)
def full_deploy(user='sechiro'):
    """ fab init_user:user=sechiro """
    adduser(user)
    groupadd(user)
    passwd(user)
    add_sudoers(user)

