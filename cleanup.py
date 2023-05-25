import click
import datetime
import csv
import os
import shutil
import shlex
import subprocess
from mako.template import Template
import portalocker


def read_results(results_file):
    results = []
    with open(results_file, "r") as ifile:
        reader = csv.DictReader(ifile)
        results = list(reader)
    return results


def run_command(command, cwd=None, shell=False):
    print("Executing command `%s`" % command)
    c = shlex.split(command)
    p = subprocess.Popen(c, cwd=cwd, shell=shell)
    return p.wait()


def generate_leaderboard(template_file, results, main_column, output_file, freq):
    leaderboard_template = Template(filename=template_file)
    time = datetime.datetime.now()
    timedelta = datetime.timedelta(hours=freq)
    
    columns = list(results[0].keys())
    if main_column is not None:
        results = sorted(results, reverse=True, key=lambda d: d[main_column])
        # Make main column the second column (first after ID)
        columns.insert(1, columns.pop(columns.index(main_column)))
    leaderboard_string = leaderboard_template.render(rows=results, columns=columns, time=str(time),
                                                     next_time=str(time+timedelta))
    lock = portalocker.Lock(output_file)

    with lock:
        with open(output_file, "w") as text_file:
            text_file.write(leaderboard_string)

    return output_file

def publish_file(output_file, git_repo):
    publish_dir = git_repo.split("/")[-1].split(".")[0]

    if not os.path.exists(publish_dir):
        run_command("git clone %s" % git_repo)
    else:
        run_command("git pull origin main", cwd=publish_dir)
    run_command("git checkout main", cwd=publish_dir)
    shutil.move(output_file, "%s/%s" % (publish_dir, output_file))
    run_command("git add %s" % output_file, cwd=publish_dir)
    run_command("git commit -m\"Update leaderboard\"", cwd=publish_dir)
    run_command("git push origin main", cwd=publish_dir)


def cleanup(*args):
    for f in args:
        os.remove(f)


@click.command()
@click.option('--template-file', required=True, help='The template file')
@click.option('--results-file', required=True, help='The results file')
@click.option('--output-file', required=True, help='The output file for the leaderboard')
@click.option('--freq', required=True, type=int, help='The update frequency')
@click.option('--git-repo', required=True, help='The git repo')
def run(template_file, results_file, output_file, freq, git_repo, main_column=None):
    results = read_results(results_file)
    output_file = generate_leaderboard(template_file, results, main_column, output_file, freq)
    publish_file(output_file, git_repo)
    #cleanup(results_file)

if __name__=="__main__":
    run()