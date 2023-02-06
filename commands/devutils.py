"""
Development utilities
====================================
Tools for developers.
"""

import click
import sh
import re
from commands.helpers import TableOutput as T
from os.path import isfile, isdir
from dotenv import load_dotenv

# declare the commands globally
git = sh.Command('git')

def __render_message(msg):
  match = re.match(r'(?P<type>^\[.+\])? ?(?P<msg>.*)', msg)
  if match and match.group('type'):
    return f"[b][blue]{match.group('type')}[/blue] {match.group('msg')}[/b]"
  return f"[b]{msg}[/b]"

@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('arguments', nargs=-1)
def xpgl(arguments):
  """
    XPGL is a wrapper around git log. It provides you a tabular output of 
    the most recent git commits
  """
  rows = []
  cnt = 1
  for line in git('--no-pager', 'log', '-n', '10', *arguments, '--pretty=%h#%d#%s#%cn#%cr'):
    cols = line.rstrip('\n').split('#')
    cols[1], cols[2], cols[3], cols[4] = cols[3], cols[4], __render_message(cols[2]), cols[1]
    cols.insert(0, str(cnt))
    rows.append(cols)
    cnt += 1
  T.out(rows, headers=('N', 'Hash', 'Who', 'When', 'Message', 'Info'), show_lines=True)

if __name__ == '__main__':
  xpgl()