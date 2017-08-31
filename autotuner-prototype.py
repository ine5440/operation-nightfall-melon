#!/usr/bin/python3
# Auto-tuner prototype
# Built for INE5540 robot overlords

import subprocess # to run stuff
import sys # for args, in case you want them
import time # for time

exec_file = 'matmult'
input_size = str(8)
exec_count = 16

def tune(compilation_line):
    # Compile code
    compilation_try = subprocess.run(filter(None, compilation_line))
#    if (compilation_try.returncode == 0):
#        print("Happy compilation")
#    else:
#        print("Sad compilation")

    # Run code
    t = 0
    for ex in range(exec_count):    
        t_begin = time.time() # timed run
        run_trial = subprocess.run(['./'+exec_file, input_size])
        t_end = time.time()
#        if (run_trial.returncode == 0):
#            print("Happy execution in "+str(t_end-t_begin))
#        else:
#            print("Sad execution")
        t += (t_end-t_begin) 
    return t

def test_flags(compilation_line, flags):
    t1 = tune(compilation_line)
    for flag in flags:
        compilation_line.append(flag)
        t2 = tune(compilation_line)
        if t1 > t2:
            compilation_line.pop()
        else:
            t1 = t2
    return compilation_line
    
def select_flags(compilation_line, flags):
    times = []
    for flag in flags:
        compilation_line.append(flag)
        t = tune(compilation_line)
        compilation_line.pop()
        times.append(t)
    best_try = 100
    count = 0
    best_time = 100000
    for t in times:
        if t < best_time:
            best_time = t
            best_try = count
        count+=1
    return flags[best_try]

def tuning_function(compilation_line, optmizations):
    print("Testing possible flags: "+" ".join(optmizations))
    best_steps = select_flags(compilation_line, optmizations)
    compilation_line.append(str(best_steps))
    print("Best compilation line so far is: "+" ".join(compilation_line));
    return compilation_line

def tuner(argv):
    exec_file = 'matmult'
    compilation_line = ['gcc','-o',exec_file,'mm.c']
    steps = '-DSTEP='

    possible_steps = [steps+str(2), steps+str(4), steps+str(8), steps+str(16), steps+str(32)]
    generic_optimizers = ['','-O1','-O2','-O3','-Ofast']
    loop_unrolling = ['-funroll-loops','-funroll-all-loops','']
    arch = ['-march=native','']

    compilation_line = tuning_function(compilation_line, possible_steps)
    compilation_line = tuning_function(compilation_line, generic_optimizers)
    compilation_line = tuning_function(compilation_line, loop_unrolling)
    compilation_line = tuning_function(compilation_line, arch)

if __name__ == "__main__":
    tuner(sys.argv[1:]) # go auto-tuner
