from fabric.api import task

@task
def migrate():
        pass

@task
def push():
        pass

@task
def provision():
        pass

@task(default=True)
def full_deploy():
    if not provisioned:
        provision()
    push()
    migrate()
