import click
from commands.helpers import Interactive


@click.command
@click.argument('connection')
@click.argument('rport')
@click.argument('lport')
def surtun(connection, rport, lport):
    cmd = Interactive(
        f"ssh -4 -N -T -R {rport}:localhost:{lport} {connection}")
    cmd.run()
