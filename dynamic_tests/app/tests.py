"""
Running solutions tests.
"""

import os
import logger_utils

import test_cases as tc
import testers_with_import as twi
from tester_with_running import auto_tests, TestResult

logger = logger_utils.get_logger(__name__)

# { <solution_file> : <test_cases> } for all solutions
TEST_FILE_TEST_CASE = {
    'topic_1/task_1_beautiful_number.py': tc.TEST_CASE_module_1_task_1,
    'topic_3/task_1_basic_operations.py': tc.TEST_CASE_module_3_task_1,
    'topic_4/task_1_cezar.py': tc.TEST_CASE_module_4_task_1,
    'topic_4/task_2_genetics.py': tc.TEST_CASE_module_4_task_2,
    'topic_4/task_3_first_last_occurrence.py': tc.TEST_CASE_module_4_task_3,
    'topic_6/task_1_dict_methods.py': tc.TEST_CASE_module_6_task_1,
    'topic_6/task_2_matrix.py': tc.TEST_CASE_module_6_task_2,
    'topic_6/task_3_google_search.py': tc.TEST_CASE_module_6_task_3,
    'topic_6/task_4_chunking.py': tc.TEST_CASE_module_6_task_4,
    'topic_6/task_5_lists.py': tc.TEST_CASE_module_6_task_5,
    'topic_7/task_1_unique_cities.py': tc.TEST_CASE_module_7_task_1,
    'topic_7/task_2_number_of_matching.py': tc.TEST_CASE_module_7_task_2,
    'topic_7/task_3_set_generator.py': tc.TEST_CASE_module_7_task_3,
    'topic_7/task_4_shared_numbers.py': tc.TEST_CASE_module_7_task_4,
    'topic_7/task_5_identical_numbers.py': tc.TEST_CASE_module_7_task_5,
    'topic_8/task_1_change_letters.py': tc.TEST_CASE_module_8_task_1,
    'topic_8/task_2_cat.py': tc.TEST_CASE_module_8_task_2,
    'topic_10/task_3_honors_students.py': tc.TEST_CASE_module_10_task_3,
    'topic_10/task_5_list_conversion.py': tc.TEST_CASE_module_10_task_5,
    'topic_10/task_6_enumerate.py': tc.TEST_CASE_module_10_task_6,
    'topic_10/task_7_inside_ball.py': tc.TEST_CASE_module_10_task_7,
}

TEST_FILE_IMPORT_TEST = {
    'topic_10/task_1_mean_function.py': twi.testing_module_10_task_1,
    'topic_10/task_2_filling_matrix.py': twi.testing_module_10_task_2,
    'topic_10/task_4_info_kwargs_function.py': twi.testing_module_10_task_4,
    'topic_10/task_8_negative_non_negative.py': twi.testing_module_10_task_8,
    'topic_11/task_1_vector.py': twi.testing_module_11_task_1,
    'topic_12/task_1_book_card.py': twi.testing_module_12_task_1,
    'topic_13/task_1_figure.py': twi.testing_module_13_task_1,
    'topic_13/task_2_classes.py': twi.testing_module_13_task_2,
}


def testing(solutions_dir: str) -> tuple[int, int, int]:
    """
    Return the number of solutions that passed all the tests, tests count
    and the number of timeout.
    :param solutions_dir: path to repo directory with solutions
    :return: ( accepted_solutions , tests_count , timeout_count )
    """
    accepted_solutions = 0
    timeout_count = 0
    for solution_file, test_cases in TEST_FILE_TEST_CASE.items():
        _solution_file = os.path.join(solutions_dir, solution_file)
        if not os.path.exists(_solution_file):
            continue

        results: list[TestResult] = auto_tests(
            solution_file=solution_file,
            base_dir=os.path.realpath(solutions_dir),
            test_cases=test_cases,
            timeout=15)

        # logger.info(f'{solution_file.split("ns/")[1]} - {results}')
        logger.info(f'{solution_file} - {results}')

        if results:
            # If all test_cases for solution are accepted
            if all(res.accepted for res in results):
                accepted_solutions += 1
            if any(res.comment == 'TIMEOUT' for res in results):
                timeout_count += 1

    for solution_file, tester in TEST_FILE_IMPORT_TEST.items():
        _solution_file = os.path.join(solutions_dir, solution_file)
        if not os.path.exists(_solution_file):
            continue

        results: list[TestResult] = tester(
            base_dir=os.path.realpath(solutions_dir))

        logger.info(f'{solution_file} - {results}')

        if results:
            # If all tester running for solution are accepted
            if all(res.accepted for res in results):
                accepted_solutions += 1

    return (accepted_solutions,
            len(TEST_FILE_TEST_CASE) + len(TEST_FILE_IMPORT_TEST),
            timeout_count)
