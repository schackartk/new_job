# new_job.py
Python program to write a job template. Supports templates for PBS (Ocelote and El Gato) and SLURM (Puma).

## Description:

```
$ ./new_job.py -h
usage: new_job.py [-h] [-m MGR] [-g GRP] [-q QUEUE] [-c NCPU] [-n NODE] [-b MEM] [-t TIME] [-e EMAIL] [-f] job

Create a new job file template

positional arguments:
  job                   Job name

optional arguments:
  -h, --help            show this help message and exit
  -m MGR, --mgr MGR     Job manager (default: SLURM)
  -g GRP, --grp GRP     Research Group (default: None)
  -q QUEUE, --queue QUEUE
                        Queue prioirity (default: standard)
  -c NCPU, --ncpu NCPU  Number of CPUs (default: 14)
  -n NODE, --node NODE  Number of nodes (default: 1)
  -b MEM, --mem MEM     Memory in GB (default: 64)
  -t TIME, --time TIME  Wall time in hr (default: 24)
  -e EMAIL, --email EMAIL
                        Email address (default: None)
  -f, --force           Overwrite existing (default: False)
```

The only required argument is `job`, the name of the job file to be created.

The correct selection of `-m|--mgr` is essential to getting the desired template format.

A template can be made for PBS:

```
$ ./new_job.py foo.sh -m PBS
Done, see new script "foo.sh".

$ head foo.sh
#!/bin/bash

### REQUIRED
### Research group/PI
#PBS -W group_list=None
### Job queue (standard|windfall|high_pri)
#PBS -q standard
### Number of nodes
### Number of CPUs (fraction of 28 e.g. 7, 14, 28)
### Amount of memory
```
Or a template can be made for SLURM:

```
$ ./new_job.py bar.sh -m SLURM
Done, see new script "bar.sh".

$ head bar.sh
#!/bin/bash

### REQUIRED:
### Research group/PI
#SBATCH --account=bhurwitz
### Job queue (standard|windfall|high_pri)
#SBATCH --partition=standard
### Number of nodes
#SBATCH --nodes=1
### Number of CPUs 
```
### Setting your own defaults

The defaults can be changed by creating a "~/.new_job.py" configuration file with any or all of the following fields: mgr, grp, queue, ncpu, node, mem, time, email.

For example, mine looks like:

```
$ cat ~/.new_job.py
mgr=PBS
grp=bhurwitz
email=schackartk@email.arizona.edu
```

By doing so, I do not need to use the `-e|--email`, or `-g|--grp` flags to include my information in the template by default.


## Installation

Firstly, you should clone this repository:

```
$ git clone git@github.com:schackartk/new_job.git
```

Then you can copy the `new_job.py` program to any directory currently in your `$PATH`.
It's common to place programs into a directory like `/usr/local/bin`, but this often will require root priviliges.
A common workaround is to create a writable directory in your `$HOME` where you can place programs.
One option is to use `$HOME/.local` as the "prefix" for local software installations. You can copy the program there:

```
$ cp new_job.py ~/.local/bin
```

To make sure that this directory is on your `$PATH`, you can add this to your `.bash_profile` (or `.bashrc`) file:

```
export PATH=$HOME/.local/bin:$PATH
```

## Authorship:

Author: Kenneth Schackart (schackartk1@gmail.com)

Acknowledgement: The concept is adapted from [new-py](https://github.com/kyclark/new.py) by Ken Youens-Clark
