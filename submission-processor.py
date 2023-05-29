import click
import pathlib
import os
from executor import run_command

@click.command()
@click.option('--basedir', default=None, help='Directory to find executables')
@click.option('--identifier', required=True, help='Identify this submission')
@click.option('--artifacts-path', default=None, help='Location of artifacts')
def run(basedir, identifier, artifacts_path):
	commandOMP = ["python", os.path.join(artifacts_path, "submission-processor-omp.py")]
	commandOMP += ["--basedir", basedir]
	commandOMP += ["--identifier", identifier]
	commandOMP += ["--artifacts-path", artifacts_path]
	commandOMP = " ".join(commandOMP)
	pomp = run_command(commandOMP, cwd=basedir, output_file="None")
	rcomp = pomp.returncode
	print(rcomp)

	commandMPI = ["python", os.path.join(artifacts_path, "submission-processor-mpi.py")]
	commandMPI += ["--basedir", basedir]
	commandMPI += ["--identifier", identifier]
	commandMPI += ["--artifacts-path", artifacts_path]
	commandMPI = " ".join(commandMPI)
	pmpi = run_command(commandMPI, cwd=basedir, output_file="None")
	rcmpi = pmpi.returncode
	print(rcmpi)
	


if __name__=="__main__":
    run()
