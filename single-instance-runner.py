import click
import shlex
import subprocess
import portalocker
import csv
import os
import sys
from contexttimer import Timer
import portalocker

from writer import write_results
from executor import run_executable


@click.command()
@click.option('--basedir', default=None, help='Directory to find executables')
@click.option('--executable', required=True, help="Name of executable to run")
@click.option('--identifier', required=True, help='Identify this submission')
@click.option('--results-file', required=True, help='Where to write the results')
@click.option('--num-par', required=True, type=int,
              help='Number of parallel processors')
@click.option('--parallel', type=click.Choice(['MPI', 'OpenMP'],
                                              case_sensitive=False),
              required=True, help='Which kind of parallelism to use (OpenMP/MPI)')
@click.option('--args', default=None, help='(Optional) Arguments for executable')
def run(basedir, executable, identifier, results_file, num_par, parallel, args):
    all_data = []

    if basedir is None:
        basedir = "."

    e_full_path = os.path.join(basedir, executable)
    args = args.split(",")
    num_threads = None
    if parallel == "MPI":
        e_full_path = "mpirun -np %d %s" % (num_par, e_full_path)
    else:
        num_threads = num_par

    runtime = run_executable(e_full_path, args, num_threads, num_runs=3, capture_output=False)

    if runtime is None:
        print("Provided command is erroring out. Timings are meaningless. Moving on...")
        sys.exit(-1)
    
    results_to_write = {'id': identifier, 'executable': executable, 'num_par': num_par,
                        'runtime': runtime}
    write_results(results_to_write,
                  lambda x: (x['id'] == str(identifier) and
                             x['executable'] == str(executable) and
                             x['num_par'] == str(num_par)),
                  results_file)


if __name__=="__main__":
    run()