# new_job
Python program to write a job template. Supports templates for PBS (Ocelote and El Gato) and SLURM (Puma).

## Description:

```
$ ./new_job.py -h
usage: new_job.py [-h] [-m MGR] [-g GRP] [-q QUEUE] [-n NCPU] [-b MEM] [-t TIME] [-e EMAIL] [-f] job

Create a new job file template

positional arguments:
  job                   Job name

optional arguments:
  -h, --help            show this help message and exit
  -m MGR, --mgr MGR     Job manager (default: SLURM)
  -g GRP, --grp GRP     Research Group (default: None)
  -q QUEUE, --queue QUEUE
                        Queue prioirity (default: Standard)
  -n NCPU, --ncpu NCPU  Number of CPUs (default: 12)
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

$ cat foo.sh
#!/usr/bin/bash

#PBS -W group_list=None
#PBS -q Standard
#PBS -l select=1:ncpus=12
#PBS -l walltime:24:00:00
#PBS -M Anonymous@localhost
#PBS -m bea

# Load modules

DIR="/home/ken/documents/research/new_job"
```
Or a template can be made for SLURM:

```
$ ./new_job.py bar.sh -m SLURM
Done, see new script "bar.sh".

$ cat bar.sh
#!/usr/bin/bash

### REQUIRED: 
### Specify the PI group for this job
#SBATCH --account=None
### Set the partition for your job.
#SBATCH --partition=Standard
### Set the number of cores that will be used for this job.
#SBATCH --ntasks=12
### Set the memory required for this job.
#SBATCH --mem=64gb
### Specify the time required for this job, hhh:mm:ss
#SBATCH --time=24:00:00
### OPTIONAL:
### Set the job name
#SBATCH --job-name=
### Request email when job begins and ends
### SBATCH --mail-type=ALL
### Specify email address to use for notification
### SBATCH --mail-user=Anonymous@localhost

# Load modules

DIR="/home/ken/documents/research/new_job"
```
### Setting your own defaults

The defaults can be changed by creating a "~/.new_job.py" configuration file with any of all of the following fields: mgr, grp, queue, ncpu, mem, time, email.

For example, mine looks like:

```
$ cat ~/.new_job.py
mgr=PBS
grp=bhurwitz
email=schackartk@email.arizona.edu
```
