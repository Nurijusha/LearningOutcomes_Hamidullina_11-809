import os
import sys
from subprocess import PIPE, TimeoutExpired, run
from collections import namedtuple
from logger_utils import get_logger

logger = get_logger(__name__)

TestResult = namedtuple('TestResult', 'number accepted comment')


def get_text_from_case(test_iter: tuple | list) -> str:
    """
    Return raw string from iterable object to pass to the subprocess input
    or output.
    :param test_iter: iterable object with lines for script`s stdin
    :return: e.g. "2\n3\n4\n"
    """
    return '\n'.join(str(s) for s in test_iter)


def run_test(solution_file: str, base_dir: str, test_input: str, expected: str,
             python_path: str, timeout: int = 15) -> tuple[bool, str]:
    """
    Run test case for solution with stdin parameters.
    :param solution_file: path of .py file with solution
    :param base_dir: path to solutions base_dir
    :param test_input: input string for stdin
    :param expected: expected result from solution
    :param python_path: PYTHONPATH environment for running subprocess
    :param timeout: time to complete the solution
    :return: bool (ok solution or no) and comment ('ACCEPT', 'WRONG ANSWER',
    'TIMEOUT', 'ERROR')
    """
    try:
        proc = run(
            [sys.executable, solution_file],
            input=test_input,
            stdout=PIPE,
            stderr=PIPE,
            timeout=timeout,
            encoding='utf-8',
            cwd=base_dir,
            env={'PYTHONPATH': python_path}
        )
    except TimeoutExpired:
        return False, 'TIMEOUT'

    if proc.returncode:
        logger.error(f'ERROR when running with code {proc.returncode} - '
                     f'{proc.stderr}')
        return False, 'ERROR'
    # Deleting unnecessary whitespaces in each line from output
    output = proc.stdout.split('\n')
    output = '\n'.join([line.strip() for line in output if line])

    if output == str(expected).strip():
        return True, 'ACCESS'
    else:
        return False, 'WRONG ANSWER'


def auto_tests(solution_file: str, base_dir: str, test_cases: dict,
               timeout: int):
    """
    Run all test_cases for <solution_file> and return results [ TestResult() ]
    :param solution_file: path of .py file with solution
    :param base_dir: path to solutions base_dir
    :param test_cases: test cases dict { input : expected }
    :param timeout: timeout for solution execution
    :return: list of results
    """
    results = []

    python_path = [p for p in sys.path if p != os.getcwd()]
    python_path.append(base_dir)
    python_path = ':'.join(python_path)

    for i, test in enumerate(test_cases.items()):
        _input, expected = test
        # Prepare input string
        if isinstance(_input, (tuple, list)):
            _input = get_text_from_case(_input)
        else:
            _input = str(_input)

        # Prepare output string
        if isinstance(expected, (tuple, list)):
            expected = get_text_from_case(expected)

        accepted, comment = run_test(
            solution_file=solution_file,
            base_dir=base_dir,
            test_input=_input,
            expected=expected,
            python_path=python_path,
            timeout=timeout)
        results.append(TestResult(i, accepted, comment))
        if comment == 'TIMEOUT':
            break
    return results
