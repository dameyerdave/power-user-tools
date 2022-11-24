import sys
import os
from subprocess import Popen, PIPE
import pty
import tty
import select
import termios


class Interactive():
    """
    Execute a command interactively with pseudo terminal
    found at https://stackoverflow.com/questions/41542960/run-interactive-bash-with-popen-and-a-dedicated-tty-python
    """

    def __init__(self, command='/bin/bash'):
        self.command = command

    def run(self):
        old_tty = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())

        env = os.environ.copy()
        master, slave = pty.openpty()

        try:
            p = Popen(
                self.command.split(),
                preexec_fn=os.setsid,
                stdin=slave,
                stdout=slave,
                stderr=slave,
                env=env)

            while p.poll() is None:
                r, w, e = select.select([sys.stdin, master], [], [])
                if sys.stdin in r:
                    d = os.read(sys.stdin.fileno(), 10240)
                    os.write(master, d)
                elif master in r:
                    o = os.read(master, 10240)
                    if o:
                        os.write(sys.stdout.fileno(), o)

        finally:
            # restore tty settings back
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
