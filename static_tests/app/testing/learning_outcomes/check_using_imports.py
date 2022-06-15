from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func
from testing.utils import get_module_info


def five(file_list: list):
    if not search_with_func(file_list, func=parsers.is_exists_import_alias):
        return [Recommendation(
            name='Использование псведонимов',
            task='Тема 10. Задача 5.'
        )]
    return []


def four(file_list: list):
    if not search_with_func(file_list, func=parsers.is_exists_import_from):
        return [Recommendation(
            name='Использование конструкции from',
            task='Тема 10. Задача 5.'
        )]
    return []


def three(file_list: list):
    is_using_imports = False
    for file in file_list:
        module_info = get_module_info(file)
        if module_info.imports:
            is_using_imports = True
            break

    if is_using_imports:
        return []

    return [Recommendation(
        name='Импортирование модулей',
        task='Тема 8. Задача 1.'
    )]


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Умеет работать с модулями',
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
