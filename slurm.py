import pathlib
import os
from mako.template import Template
from executor import run_command


def submit_slurm_job(commands, template_file, num_cores=1,
                     num_tasks=1, time_limit=1, partition="course",
                     cwd=None, vars=None, dependencies=None,
                     job_name="slurm-job"):
    if vars is None:
        vars = {}
    
    if cwd is None:
        cwd = pathlib.Path().resolve()
    
    slurm_file_template = Template(filename=template_file)

    submission_file_string = slurm_file_template.render(commands=commands,
                                                        num_cores=num_cores,
                                                        num_tasks=num_tasks,
                                                        time_limit=time_limit,
                                                        partition=partition,
                                                        vars=vars, job_name=job_name)

    target_slurm_filename = os.path.join(cwd, 'submission.sh')

    with open(target_slurm_filename, "w") as text_file:
        text_file.write(submission_file_string)

    job_id = call_slurm(target_slurm_filename, cwd, dependencies)

    os.remove(target_slurm_filename)

    return job_id


def call_slurm(slurm_file, context_dir, dependencies=None):
    if dependencies is None:
        p = run_command("sbatch --nice \"%s\"" % slurm_file, cwd=context_dir)
    else:
        dependencies = [str(x) for x in dependencies]
        p = run_command("sbatch --nice --depend=afterany:%s \"%s\"" % (",".join(dependencies), slurm_file), cwd=context_dir)
        
    output = p.stdout.decode('utf-8')
    print(output)
    parts_of_output = output.split(" ")
    job_id = (parts_of_output[-1]).strip()
    assert(job_id.isnumeric())
    return int(job_id)


def run():
    job_id = submit_slurm_job(["echo Hi"], "slurm_template.tpl")


if __name__=="__main__":
    run()