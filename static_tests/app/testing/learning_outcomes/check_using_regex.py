from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func
from testing.utils import get_module_info


def five(file_list: list):
    recommendations = []
    if not search_with_func(file_list, func=parsers.is_exists_regex_matching):
        recommendations.append(
            Recommendation(
                name=f'Поиск совпадений',
                task='Тема 8. Задача 2.'
            ))
    return recommendations


def four(file_list: list):
    recommendations = []
    if not search_with_func(file_list, func=parsers.is_exists_multiple_regex):
        recommendations.append(
            Recommendation(
                name=f'Использование групп регулярных выражений',
                task='Тема 8. Задача 1.'
            ))
    return recommendations


def three(file_list: list):
    recommendations = []
    if not search_with_func(file_list, func=parsers.is_exists_regex_character):
        recommendations.append(
            Recommendation(
                name='Использование основного синтаксиса (d, D, w, W, b, B, s, S)',
                task='Тема 8. Задача 1.'
            ))

    if not search_with_func(file_list, func=parsers.is_using_method,
                            method_name='rstrip|lstrip|strip'):
        recommendations.append(
            Recommendation(
                name='Использование rstrip(), или lstrip(), или strip()',
                task='Тема 8. Задача 1.'
            ))

    is_regex_imported = False
    for file in file_list:
        module_info = get_module_info(file)
        if module_info.imports:
            if 're' in [imp.name for imp in module_info.imports]:
                is_regex_imported = True
                break
    if not is_regex_imported:
        recommendations.append(
            Recommendation(
                name='Использование модуля re',
                task='Тема 8. Задача 1.'
            ))

    return recommendations


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Умеет использовать регулярные выражения',
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
