#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Purpose: Python program to create new job files
"""

import argparse
import os
import platform
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from typing import NamedTuple, Optional, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    job: str
    mgr: str
    group: str
    queue: str
    ncpus: int
    mem: int
    time: int
    email: str
    overwrite: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get arguments """

    parser = argparse.ArgumentParser(
        prog='new_job.py',
        description='Create a new job file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    rc_file = os.path.join(str(Path.home()), '.new_job.py')
    defaults = get_defaults(open(rc_file) if os.path.isfile(rc_file) else None)
    username = os.getenv('USER') or 'Anonymous'
    hostname = os.getenv('HOSTNAME') or 'localhost'

    parser.add_argument('job', help='Job name', type=str)

    parser.add_argument('-m',
                        '--mgr',
                        type=str,
                        default=defaults.get('mgr', 'ocelote',
                        help='Job manager')

    parser.add_argument('-g',
                        '--grp',
                        type=str,
                        default=defaults.get('group'),
                        help='Research Group')

    parser.add_argument('-q',
                        '--queue',
                        type=str,
                        default=defaults.get('queue', 'Standard'),
                        help='Queue prioirity')

    parser.add_argument('-n',
                        '--ncpu',
                        type=int,
                        default=defaults.get('ncpu', 12),
                        help='Number of CPUs')

    parser.add_argument('-m',
                        '--mem',
                        type=str,
                        default=defaults.get('mem', 64),
                        help='Memory in GB')
                            
    parser.add_argument('-t',
                        '--time',
                        type=str,
                        default=defaults.get('time', 24),
                        help='Wall time in hr')

    parser.add_argument('-e',
                        '--email',
                        type=str,
                        default=defaults.get('email', f'{username}@{hostname}'),
                        help='Email address')

    parser.add_argument('-f',
                        '--force',
                        help='Overwrite existing',
                        action='store_true')

    args = parser.parse_args()

    args.job = args.job.strip().replace('-', '_')

    if not args.program:
        parser.error(f'Not a usable filename "{args.job}"')

    return Args(job=args.program,
                mgr=args.mgr,
                grp=args.grp,
                queue=args.queue,
                ncpu=args.ncpu,
                mem=args.mem,
                time=args.time,
                email=args.email,
                overwrite=args.force)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    job = args.job

    if os.path.isfile(program) and not args.overwrite:
        answer = input(f'"{program}" exists.  Overwrite? [yN] ')
        if not answer.lower().startswith('y'):
            sys.exit('Will not overwrite. Bye!')
    
    if args.mgr.lower() == 'ocelote':
        content = ocelote_body(args)
    elif args.mgr.lower() == 'slurm':
        content = slurm_body(args)
    else:
        sys.exit(f'Unrecognized job manager: {args.mgr}.')
    
    print(content, file=open(job, 'wt'), end='')

    if platform.system() != 'Windows':
        subprocess.run(['chmod', '+x', program], check=True)

    print(f'Done, see new script "{program}".')

# --------------------------------------------------
def ocelote_body(args: Args) -> str:
    """ Ocelote job template """

    return f"""#!/usr/bin/env bash

    #PBS -W group_list={args.grp}
    #PBS -q {args.queue}
    #PBS -l select=1:ncpus={args.ncpu}
    #PBS -l walltime:{args.time}:00:00
    #PBS -M {args.email}
    #PBS -m bea

    # Load modules

    DIR=\"os.getcwd()\"

"""

# --------------------------------------------------
def slurm_body(args: Args) -> str:
    """ SLURM job template """

    return f"""
"""

# --------------------------------------------------
def get_defaults(file_handle: Optional[TextIO]):
    """ Get defaults from ~/.new.py """

    defaults = {}
    if file_handle:
        for line in file_handle:
            match = re.match('([^=]+)=([^=]+)', line)
            if match:
                key, val = map(str.strip, match.groups())
                if key and val:
                    defaults[key] = val

    return defaults


# --------------------------------------------------
if __name__ == '__main__':
    main()
