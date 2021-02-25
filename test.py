#!/usr/bin/env python
"""
Runs tests from a directory


Usage:
    test.py init <local> <reference>
    test.py add -r <test_dir>...
    test.py run [-m] [-s|-v] all
    test.py run [-m] [-s|-v] <files>...

Options:
    -r --recursive            : Add all files in subdirectories
    -v --verbose              : Verbose mode to report entire output, not just diffs
    -s --silent               : Show no diffs
    -m --memory               : valgrind

"""
line_len = 50 # total of 56

import subprocess
from docopt import docopt
import os
import sys
import json
from collections import deque


VALGRIND_ARGUMENTS = [
  'valgrind',
  '--tool=memcheck',
  '--leak-check=full',
  '--show-reachable=yes',
  '--track-origins=yes',
  '--error-exitcode=1',
  '-s'
]


def comp(loc, ref, test):
    loc_return = subprocess.run([loc, test], capture_output=True)
    ref_return = subprocess.run([ref, test], capture_output=True)
    # print(loc_return.stderr, ref_return.stderr)
    return ((loc_return.returncode == ref_return.returncode) and (loc_return.stdout == loc_return.stdout)), loc_return, ref_return


def valgrind(loc, test):
    process = subprocess.Popen([*VALGRIND_ARGUMENTS,loc, test], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    code = process.wait()
    errors = process.stderr.readlines()
    # print(code)
    return code, errors


def display_comp(loc, ref, test, verbose):
    run_res = comp(loc, ref, test)
    if not run_res[0]:
        print(f"TEST     : {test}" + " "*(line_len - len(test)-5) + ": FAIL")
        if verbose == 2:
            print("-" * (line_len+5))
            print(f"LOCAL:")
            print(run_res[1].stdout)
            print(f"REFERENCE:")
            print(run_res[2].stdout)
            print("-" * (line_len+5) )
        elif verbose == 1:
            print("-" * (line_len+5))
            print(f"LOCAL:")
            print(run_res[1].stdout)
            print(f"REFERENCE:")
            print(run_res[2].stdout)
            print("-" * (line_len+5) )


        elif verbose == 0:
            pass
    else:
        print(f"TEST     : {test}" + " "*(line_len - len(test)-5) + ": OK")
    return run_res

def parse_vg_success(vg_output):
    status = {"free": "X", "errors": "X", "segfault": "O"}
    # free
    if "All heap blocks were freed" in vg_output:
        status['free'] = "O"
    if "ERROR SUMMARY: 0 errors" in vg_output:
        status['errors'] = "O"
    if "SIGSEGV" in vg_output:
        status['segfault'] = "X"
    print("VALGRIND SUMMARY:" + "-" * (line_len - 17))
    print(f"FREE: {status['free']}, ERROR: {status['errors']}, SIGSEGV: {status['segfault']}")


def parse_vg_failure(vg_output):
    status = {"lost": "X", "errors": "X", "segfault": "O"}
    # free
    if "definitely lost: 0 bytes" in vg_output and "indirectly lost: 0 bytes" in vg_output:
        status['lost'] = "O"
    if "SIGSEGV" in vg_output:
        status['segfault'] = "X"
    if "ERROR SUMMARY: 0 errors" in vg_output:
        status['errors'] = "O"
    print("VALGRIND SUMMARY:" + "-" * (line_len - 17))
    print(f"LOST_MEM: {status['lost']}, ERRORS: {status['errors']}, SIGSEGV: {status['segfault']}")


    # bad

def display_valgrind(loc, test, ref_error, verbose):
    run_vg = valgrind(loc, test)




    if (run_vg[0] == 0) == (len(ref_error) == 0):
        print(f"VALGRIND : {test[:min(len(test),50)]}" + " "*(line_len - len(test) - 5) + ": OK")
    else:
        print(f"VALGRIND : {test[:min(len(test),50)]}" + " "*(line_len - len(test) - 5) + ": FAIL")
        if len(ref_error) == 0:
            parse_vg_success(run_vg[1])
        else:
            parse_vg_failure(run_vg[1])
        # exited error parsing
    return run_vg[0]

def run(loc, ref, test, vg, v):
    if v == 2:
        comp_res = display_comp(loc, ref, test, v)
        if vg:
            vg_res = display_valgrind(loc, test, comp_res[2].stderr,  v)
    else:
        comp_res = display_comp(loc, ref, test, v)
        if vg:
            vg_res = display_valgrind(loc, test, comp_res[2].stderr,  v)


    return comp_res

def run_test_all(loc, ref, vg, v):
    count = 0

    line_len = 50

    for test in config['list']:
        result = run(config['loc'], config['ref'], test, vg, v)
        if result[0]:
            count+= 1

    print(f"Passed: {count}/{len(config['list'])}")

# def vg_test():
#     for test in full_tests:

def load_config():
    try:
        with open("./.test/config.json", 'r') as fp:
            config = json.load(fp)
    except FileNotFoundError:
        raise Exception("Test configuration hasn't been initialized. Run `test init <local> <reference>` to initialize implementations or use `test <local> <reference> <test_file>")
    return config

def save_config(config):
    with open("./.test/config.json", 'w') as fp:
        json.dump(config, fp)

def add_dir(dir_list, recurse):
    config = load_config()
    q = deque(dir_list)
    new_list = []
    while q:
        elem = q.popleft()
        if os.path.isdir(elem):
            q.extend([f"{elem}/{new_elem}" for new_elem in os.listdir(elem)])
        else:
            new_list.append(elem)
    config['list'].extend(new_list)
    save_config(config)

def init_config(local, reference):
    loc_exec = local
    ref_exec = reference
    config = {"loc": loc_exec, "ref": ref_exec, "list": []}
    if not os.path.isdir("./.test/"):
        os.mkdir("./.test/")
    save_config(config)
    print("Initialization complete")



def parse_verbose(verbose, silent):
    if verbose:
        return 2
    if silent:
        return 0
    else:
        return 1

if __name__ == "__main__":
    args = docopt(__doc__)
    v = parse_verbose(args['--verbose'], args['--silent'])
    if args['init']:
        init_config(args['<local>'], args['<reference>'])

    if args['add']:
        add_dir(args['<test_dir>'], args['--recursive'])

    if args['run']:
        config = load_config()
        for file in args['<files>']:
            run(config['loc'], config['ref'], file, args['--memory'], v)

    if args['run'] and args['all']:
        config = load_config()
        run_test_all(config['loc'], config['ref'], args['--memory'], v)
