#!/usr/bin/python3
# Auto-tuner prototype
# Built for INE5540 robot overlords

import subprocess # to run stuff
import sys # for args, in case you want them
import time # for time

exec_file = 'matmult'

def tune(compilation_line, input_size):
    # Compile code
    compilation_try = subprocess.run(compilation_line)
    if (compilation_try.returncode == 0):
        print("Happy compilation")
    else:
        print("Sad compilation")

    # Run code
    t_begin = time.time() # timed run
    run_trial = subprocess.run(['./'+exec_file, input_size])
    t_end = time.time()
    if (run_trial.returncode == 0):
        print("Happy execution in "+str(t_end-t_begin))
    else:
        print("Sad execution")
    return (t_end-t_begin)


def tuner(argv):
    exec_file = 'matmult'
    compilation_line = ['gcc','-o',exec_file,'mm.c']
    steps = ['-DSTEP=']
    input_size = str(6)
    best_steps = steps_tries(compilation_line, input_size)
    print("Best compilation line so far is: "+" ".join(compilation_line+steps)+str(best_steps));

    
def steps_tries(compilation_line, input_size):
    # for step sizes divisible by 2, try to find the best
    times = []
    tries = [2, 4, 8, 16, 32]
    for i in tries:
        step_count = i
        steps = ['-DSTEP='+str(step_count)]
        print(compilation_line+steps)
        time = tune(compilation_line+steps, input_size)
        times.append(time)
    best_try = 100
    count = 0
    best_time = 100000
    for time in times:
        if time < best_time:
            best_time = time
            best_try = count
        count+=1
    return tries[best_try]



if __name__ == "__main__":
    tuner(sys.argv[1:]) # go auto-tuner
