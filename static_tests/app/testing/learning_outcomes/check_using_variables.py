import cdmpyparser

from testing.models import LearningOutcome, Recommendation
from testing import utils

from logger_utils import get_logger

logger = get_logger(__name__)


def is_using_constants(file_list: list):
    for file in file_list:
        module_info = cdmpyparser.getBriefModuleInfoFromFile(file)
        if any(var.name.isupper() for var in module_info.globals):
            return True, None
    logger.debug('Не использует константы с правильным оформлением')
    return False, Recommendation(
        name='Использование констант с правильным оформлением',
        task='Тема 13. Задача 1.'
    )


def is_using_local_vars(file_list: list):
    for file in file_list:
        all_variables = utils.get_all_variables(file)
        module_info = cdmpyparser.getBriefModuleInfoFromFile(file)
        if len(all_variables) - len(module_info.globals):
            return True, None
    logger.debug('Не использует локальные переменные')
    return False, Recommendation(
        name='Использование локальных переменных',
        task='Тема 11. Задача 1.'
    )


def is_using_global_vars(file_list: list):
    for file in file_list:
        module_info = cdmpyparser.getBriefModuleInfoFromFile(file)
        if module_info.globals:
            return True, None
    logger.debug('Использует глобальные переменные')
    return False, Recommendation(
        name='Использование глобальных переменных',
        task='Тема 4. Задача 1.'
    )


def is_using_vars(file_list: list):
    for file in file_list:
        all_variables = utils.get_all_variables(file)
        if all_variables:
            return True, None
    logger.debug('Не обьявляет переменные')
    return False, Recommendation(
        name='Обьявление переменных',
        task='Тема 4. Задача 1.'
    )


def five(file_list: list):
    result, recommendation = is_using_constants(file_list)
    if result:
        return []
    return [recommendation]


def four(file_list: list):
    recommendations = []
    for f in (is_using_local_vars, is_using_global_vars):
        result, recommendation = f(file_list)
        if not result:
            recommendations.append(recommendation)
    return recommendations


def three(file_list: list):
    result, recommendation = is_using_vars(file_list)
    if result:
        return []
    return [recommendation]


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Использует переменные',
    )

    if not file_list:
        learning_outcome.score = 2
        return learning_outcome

    for func_score in (five, four, three):
        recommendations = func_score(file_list)
        # If all the criteria of this level are passed
        if not recommendations:
            break
        # If recommendations are exists, add to the learning outcome
        for recommendation in recommendations:
            learning_outcome.recommendations.append(recommendation)
        learning_outcome.score -= 1
    return learning_outcome
