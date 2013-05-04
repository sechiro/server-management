from fabric.api import task, run, local, settings, env, sudo, put

@task
def adduser(user='sechiro'):
    """ [idem] Add user if not exists. ex) fab adduser:user=sechiro """
    env.user = 'root'
    result = check_user(user=user)
    if result.failed:
        run('useradd %s' % user)
    else:
        print 'User "%s" already exists!' % user

@task
def passwd(user='sechiro'):
    """ [idem] Set general user's password. (root login required) ex) fab passwd:user=sechiro  """
    env.user = 'root'
    result = check_user(user=user)
    if result.failed:
        print 'User "%s" does not exist!' % user
    else:
        run('passwd %s' % user)

@task
def wheeladd(user='sechiro'):
    """ [idem] Add user to wheel group. ex) fab wheeladd:user=sechiro """
    env.user = 'root'
    result = check_user(user=user)
    if result.failed:
        print 'User "%s" does not exist!' % user
    else:
        run('usermod -a -G wheel %s' % user)

@task
def check_user(user='sechiro'):
    """ [idem] Check given user existence by using "id" command. ex) fab check_user:user=sechiro """
    with settings(warn_only=True):
        result = run('id %s' % user, quiet=True)
        return result

@task
def add_sudoers(group='wheel'):
    """ [idem] Add given group name(default:wheel) to sudoers with NOPASSWD privileges.  ex) fab add_sudoers:group=%wheel """
    env.user = 'root'
    tempfile = '/tmp/nopass_' + group
    result = check_sudoers(group=group)
    if result.failed:
        local('echo "%s ALL=(ALL) NOPASSWD: ALL" > %s' % ('%' + group, tempfile) )
        local('cat %s' % tempfile)
        put(tempfile, '/etc/sudoers.d/', mode=0440)
    else:
        print 'The sudoers setting of %s group exists already.' % group
        print result.stdout

    local('rm %s' % tempfile )

@task
def check_sudoers(group='wheel',confdir='/etc/sudoers.d'):
    """ [idem] Check sudoers setting file. ex) fab check_sudoers:confdir=/etc/sudoers.d """
    conffile = confdir + '/nopass_' + group
    with settings(warn_only=True):
        result = run('ls -l %s' % conffile, quiet=True)
        return result


@task(default=True)
def full_deploy(user='sechiro'):
    """ [idem] fab init_user:user=sechiro """
    adduser(user)
    wheeladd(user)
    passwd(user)
    add_sudoers(user)

