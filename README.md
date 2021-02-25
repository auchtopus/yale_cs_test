# Yale CS test suite

Automate testing + valgrinding of custom test cases.


## Installation

Download `test.py` into a directory SEPARATE from your pset directory. This is to prevent the default `submit` script from including this code into the submissions.

## Usage
1. Initialize the test script, notifying it of your local implementation and the reference implementation
```
./test.py init <your_implementation> <reference_implementation>
```

For instance, run `./test.py init ~/cs323/proj1/my_proj1 /c/cs323/proj1/proj1`

2. Add test cases:

Test cases can be added with
```
./test.py add [-r] <test_dir>...
```
You can add individual files, or add directories with the `-r` flag.


3. Run tests:
To run tests:
```
./test.py [-m] [-s|-v] run <files>... // to run a list of test files
./test.py [-m] [-s|-v] run all // to run all the test files that have been added
```

Options:
* `-m` runs valgrind as well, comparing the output of your valgind to the output of the reference valgrind. It will notify of errors, unreachable memory, or segfaults. `X` means no erros, `O` indicates an error in the result
* `-s` runs silently, so does not show any output or diffs. It only reports whether a test passed or failed
* `-v` runs verbosely, showing the full outputs of your implementation and the reference implementation.
By default, the program will show diffs.
