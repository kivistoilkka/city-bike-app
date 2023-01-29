from invoke import task

@task
def start(ctx):
    ctx.run("export FLASK_APP=src && flask run", pty=True)

@task
def start_with_build(ctx):
    ctx.run("export FLASK_APP=src && export BUILD_PROD_DB=True && flask run", pty=True)

@task
def dev(ctx):
    ctx.run(
        'export FLASK_APP=src && export FLASK_DEBUG=1 && export RUNNING_DEV=True && flask run',
        pty=True
    )

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    ctx.run("pylint --fail-under=9 src", pty=True)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)
