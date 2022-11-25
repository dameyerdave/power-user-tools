import click
from commands.helpers import Interactive


@click.command()
@click.option('--port', '-p', type=int, default=22, help='the port to connect to')
@click.option('--identity', '-i', help='name of the key (should be placed inside ~/.ssh/...)')
@click.option('--force-password-auth', '-f', is_flag=True, default=False,  help='force password authentication')
@click.option('--disable-host-key-checking', '-d', is_flag=True, default=False, help='do not check if the host key is correct [!! be careful !!]')
@click.option('--verbose', '-v', is_flag=True, default=False, help='display verbose output')
@click.argument('connection')
def sussh(connection, port=22, identity=None, force_password_auth=False, disable_host_key_checking=False, verbose=False):
    _options = ''
    if force_password_auth:
        _options += ' -o PreferredAuthentications=password -o PubkeyAuthentication=no'
    if disable_host_key_checking:
        _options += ' -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

    _identity = ''
    if identity:
        _identity = f"-i ~/.ssh/{identity}"

    command = f"ssh {_options} {_identity} -p {port} {connection}"

    if verbose:
        print('RUNNING:', command)
    ssh = Interactive(command)
    ssh.run()


@click.command()
@click.argument('connection')
@click.argument('rport')
@click.argument('lport')
def surtun(connection, rport, lport):
    cmd = Interactive(
        f"ssh -4 -N -T -R {rport}:localhost:{lport} {connection}")
    cmd.run()


@click.command()
@click.argument('connection')
@click.argument('rport')
@click.argument('lport')
def suftun(connection, rport, lport):
    cmd = Interactive(
        f"ssh -4 -N -T -L {lport}:localhost:{rport} {connection}")
    cmd.run()
