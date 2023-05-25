import os
import shlex
import subprocess
from contexttimer import Timer


def run_executable(executable, args, num_threads=None, num_runs=1, capture_output=True):
    command = executable
    
    if args is not None:
        command += " " + (" ").join(list(args))

    print("Command: %s (%s threads)" % (command, str(num_threads)))

    c = shlex.split(command)

    my_env = os.environ.copy()
    
    if num_threads is not None:
        my_env['OMP_NUM_THREADS'] = str(num_threads)
        my_env['KMP_AFFINITY'] = 'scatter'
    
    
    timings = []
    for i in range(num_runs):
        with Timer() as t:
            p = subprocess.run(c, capture_output=capture_output, text=True, env=my_env)
        
        if(p.returncode):
            print(p.stdout)
            print(p.stderr)
            return None
        timings.append(t.elapsed)
    
    return min(timings)


def run_command(command, cwd, shell=False, output_file=None):
    print("Executing command `%s`"%command)
    print(cwd)
    if command is None:
        return
    c = shlex.split(command)
    print(c)
    p = subprocess.run(c, cwd=cwd, shell=shell, capture_output=True)

    if output_file is not None:
        with open(output_file, 'w') as file:
            file.write(command)
            file.write("\n")
            file.write(p.stdout.decode('utf-8'))
            file.write("\n")
            file.write(p.stderr.decode('utf-8'))
    return p
