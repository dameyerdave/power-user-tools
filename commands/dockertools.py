"""
Dockertools
====================================
Tools to manage Docker.
"""

import os
import sys
import click
import sh
from commands.helpers import Executor as E, Message as M, TableOutput as T
from os.path import isfile, isdir
from dotenv import load_dotenv

# declare the commands globally
bash = sh.Command('bash')
docker = sh.Command('docker')


@click.command(context_settings={"ignore_unknown_options": True})
@click.option('--shell', '-s', is_flag=True, default=False, help='open a shell to the container, basically exec')
@click.option('--logs', '-l', is_flag=True, default=False, help='follows the logs, basically logs -f')
@click.option('--ignore-override', '-i', is_flag=True, default=False, help='ignores the docker-compose.override.yml')
@click.argument('docker_arguments', nargs=-1)
def dcc(docker_arguments, shell=False, logs=False, ignore_override=False):
    """
    DCC is a wrapper around docker-compose. If you are executing it inside a git
    repository it will set the following environment variables:
    - GIT_VERSION
    - GIT_BRANCH
    - GIT_LASTCOMMITDATE
    - GIT_COMMITHASH
    You can use those in the build process to pass the git version information to the application. 

    Additionally it handles the docker-compose files. You can set the environment variable DCC_ENV to
    whatever string is in between docker-compose.<????>.yml. DCC will then take docker-compose.yml as
    the base file, the next is the docker-compose.<????>.yml and if a docker-compose.override.yml exists
    it will take this as the last compose file in the -f ordering.
    """
    if not isfile('docker-compose.yml'):
        M.error('There is no docker-compose.yml file in this directory!')
        sys.exit(1)
    dcc_env = None
    env = {
        'GIT_VERSION': '?.?.?',
        'GIT_BRANCH': 'N/A',
        'GIT_LASTCOMMITDATE': 'N/A',
        'GIT_COMMITHASH': 'N/A'
    }
    if isfile('.env'):
        load_dotenv('.env')
        dcc_env = os.environ.get('DCC_ENV')
        M.debug(f"Running DCC environment {dcc_env}.")
    else:
        M.warn(f"No .env file found in current directory: {os.getcwd()}")
    if isdir('.git'):
        if E.success('git rev-parse --is-inside-work-tree'):
            env['GIT_VERSION'] = E.run('git describe --always')
            env['GIT_BRANCH'] = E.run('git rev-parse --abbrev-ref HEAD')
            env['GIT_LASTCOMMITDATE'] = E.run('git log -1 --format=%cI')
            env['GIT_COMMITHASH'] = E.run('git rev-parse HEAD')
        M.debug('Git repository detected.')
    else:
        M.warn("Not a git repository.")

    docker_files = [
        'docker-compose.yml'
    ]
    if dcc_env:
        docker_files.append(f"docker-compose.{dcc_env}.yml")
    if not ignore_override and isfile('docker-compose.override.yml'):
        docker_files.append('docker-compose.override.yml')
    if shell:
        docker_arguments = ['exec', *docker_arguments, '/bin/bash']
    elif logs:
        docker_arguments = ['logs', '-f', *docker_arguments]
    command = f"docker-compose -f {' -f '.join(docker_files)} {' '.join(docker_arguments)}"
    M.debug(f"Command: {command}")
    os.environ.update(env)
    try:
        bash('-c', command, _fg=True)
    except Exception as ex:
        M.error(f"Error executing command {command}: {ex}")


@click.command()
@click.argument('filter', required=False)
def dtls(filter: str = None):
    _filter = ''
    if filter:
        _filter = f"--filter name={filter}"
    command = "docker ps %s -a --format '{{.Names}}#{{.Status}}#{{.Image}}'" % _filter
    output = E.run(command)
    T.out(output, headers=('Name', 'Status', 'Image'))


@click.command()
@click.argument('filter', required=False)
def dtins(filter: str = None):
    rows = []
    args = ['ps', '-a', '--format', '{{.Names}}']
    if filter:
        args.append('--filter ')
        args.append(f"name={filter}")
    for container in docker(*args, _iter=True):
        container = container.rstrip('\n')
        insp = docker('inspect', '-f',
                      '{{ .State.Status }}#{{ .HostConfig.RestartPolicy.Name }}', container)
        rows.append(f"{container}#{insp}")
    T.out(rows, headers=('Name', 'Status', 'Restart'))


def __get_container_name(pattern):
    containers = E.run('docker ps -a --format "{{.Names}}"').split('\n')
    found_containers = []
    for container in containers:
        if pattern in container:
            found_containers.append(container)
    if len(found_containers) == 1:
        return found_containers[0]
    elif len(found_containers) == 0:
        M.error(f"No container found with name {pattern}.")
        raise
    else:
        M.error(
            f"More than one containers found with name {pattern}: {', '.join(found_containers)}")
        raise


@click.command()
@click.argument('pattern')
def dtail(pattern):
    try:
        docker('logs', '-f', __get_container_name(pattern), _fg=True)
    except:
        pass


@click.command()
@click.argument('pattern')
def dtsh(pattern):
    try:
        docker('exec', '-it', __get_container_name(pattern),
               '/bin/bash', _fg=True)
    except sh.ErrorReturnCode as ex:
        try:
            docker('exec', '-it', __get_container_name(pattern),
                   '/bin/sh', _fg=True)
        except:
            pass
    except:
        pass


@click.command()
@click.option('--force', '-f', is_flag=True, default=False, help='force removal, do not ask')
def dtclean(force):
    try:
        argss = [
            ['image', 'prune'],
            ['image', 'prune', '-a'],
            ['container', 'prune'],
            ['system', 'prune'],
            ['builder', 'prune', '-a']
        ]
        for args in argss:
            if force:
                args.append('-f')
            docker(*args, _fg=True)
    except:
        pass
