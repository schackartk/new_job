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
    grp: str
    queue: str
    ncpu: int
    node: int
    mem: int
    time: int
    email: str
    overwrite: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get arguments """

    parser = argparse.ArgumentParser(
        prog='new_job.py',
        description='Create a new job file template',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    rc_file = os.path.join(str(Path.home()), '.new_job.py')
    defaults = get_defaults(open(rc_file) if os.path.isfile(rc_file) else None)
    username = os.getenv('USER') or 'Anonymous'
    hostname = os.getenv('HOSTNAME') or 'localhost'

    parser.add_argument('job', help='Job file name', type=str)

    parser.add_argument('-m',
                        '--mgr',
                        type=str,
                        default=defaults.get('mgr', 'SLURM'),
                        help='Job manager')

    parser.add_argument('-g',
                        '--grp',
                        type=str,
                        default=defaults.get('grp'),
                        help='Research Group')

    parser.add_argument('-q',
                        '--queue',
                        type=str,
                        default=defaults.get('queue', 'standard'),
                        help='Queue priority')

    parser.add_argument('-c',
                        '--ncpu',
                        type=int,
                        default=defaults.get('ncpu', 14),
                        help='Number of CPUs')

    parser.add_argument('-n',
                        '--node',
                        type=int,
                        default=defaults.get('node', 1),
                        help='Number of nodes')

    parser.add_argument('-b',
                        '--mem',
                        type=int,
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

    if not args.job:
        parser.error(f'Not a usable filename "{args.job}"')

    return Args(job=args.job,
                mgr=args.mgr,
                grp=args.grp,
                queue=args.queue,
                ncpu=args.ncpu,
                node=args.node,
                mem=args.mem,
                time=args.time,
                email=args.email,
                overwrite=args.force)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    job = args.job

    if os.path.isfile(job) and not args.overwrite:
        answer = input(f'"{job}" exists.  Overwrite? [yN] ')
        if not answer.lower().startswith('y'):
            sys.exit('Will not overwrite. Bye!')
    
    if args.mgr.lower() == 'pbs':
        header = pbs_header(args)
    elif args.mgr.lower() == 'slurm':
        header = slurm_header(args)
    else:
        sys.exit(f'Unrecognized job manager: "{args.mgr}".')

    content = '#!/bin/bash' + header + body()
    
    print(content, file=open(job, 'wt'), end='')

    if platform.system() != 'Windows':
        subprocess.run(['chmod', '+x', job], check=True)

    print(f'Done, see new script "{job}".')

# --------------------------------------------------
def pbs_header(args: Args) -> str:
    """ PBS job template """

    return f"""\n
### REQUIRED
### Research group/PI
#PBS -W group_list={args.grp}
### Job queue (standard|windfall|high_pri)
#PBS -q {args.queue}
### Number of nodes
### Number of CPUs per node (fraction of 28 e.g. 7, 14, 21)
### Amount of memory per node (<= 168 on ocelote)
#PBS -l select={args.node}:ncpus={args.ncpu}:mem={args.mem}gb
### Job walltime (HHH:MM:SS) (<=240 hrs)
#PBS -l walltime={args.time}:00:00
### OPTIONAL
### Job name
### PBS -N JobName
### Standard output filename
### PBS -o out_filename.txt
### Standard error filename
### PBS -e error_filename.txt
### Email notifications (𝚋̲egin|𝚎̲nd|𝚊̲bnormal end)
### PBS -m bea
### Email addresss
### PBS -M {args.email}

"""

# --------------------------------------------------
def slurm_header(args: Args) -> str:
    """ SLURM job template """

    return f"""\n
### REQUIRED: 
### Research group/PI
#SBATCH --account={args.grp}
### Job queue (standard|windfall|high_pri)
### If windfall, omit --account
#SBATCH --partition={args.queue}
### Number of nodes
#SBATCH --nodes={args.node}
### Number of CPUs per node 
#SBATCH --ntasks={args.ncpu}
### Amount of memory per node
#SBATCH --mem={args.mem}gb
### Job walltime (HHH:MM:SS)
#SBATCH --time={args.time}:00:00
### OPTIONAL:
### Job name
### SBATCH --job-name=JobName
### Standard output filename
### SBATCH -o out_filename.txt
### Standard error filename
### SBATCH -e error_filename.txt
### Email notifications (BEGIN|END|FAIL|ALL)
### SBATCH --mail-type=ALL
### Email addresss
### SBATCH --mail-user={args.email}
"""

# --------------------------------------------------
def body() -> str:
    """ Example body"""

    return f"""
# Source ~/.bashrc for aliases and $PATH
source ~/.bashrc

# Activate a conda environment
# source activate my_env

# Load any necessary modules
# module load my_modules

# Get current directory to help establish paths
DIR=\"{os.getcwd()}\"

"""

# --------------------------------------------------
def get_defaults(file_handle: Optional[TextIO]):
    """ Get defaults from ~/.new_job.py """

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
