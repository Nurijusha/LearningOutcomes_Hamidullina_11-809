from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func


def five(file_list: list):
    recommendations = []
    if not search_with_func(file_list, func=parsers.is_exists_nested_loop):
        recommendations.append(
            Recommendation(
                name=f'Использование вложенных циклов: for-for',
                task='Тема 6. Задача 3.'
            )
        )
    return recommendations


def four(file_list: list):
    recommendations = []
    for operator, task in (('continue', 'Тема 4. Задача 1.'),
                           ('break', 'Тема 6. Задача 3.'),
                           ('while', 'Тема 7. Задача 1.'),
                           ('for', 'Тема 6. Задача 2.')):
        if not search_with_func(file_list, func=parsers.is_exists_pattern,
                                pattern=operator):
            recommendations.append(
                Recommendation(
                    name=f'Использование {operator}',
                    task=task
                ))
    if not search_with_func(file_list, func=parsers.is_exists_for_range):
        recommendations.append(
            Recommendation(
                name=f'Использование for с range',
                task='Тема 4. Задача 1.'
            ))
    return recommendations


def three(file_list: list):
    recommendations = []
    for operator, task in (('elif', 'Тема 4. Задача 3.'),
                           ('else', 'Тема 3. Задача 3.'),
                           ('if', 'Тема 4. Задача 3.')):
        if not search_with_func(file_list, func=parsers.is_exists_pattern,
                                pattern=operator):
            operator = '' if operator == 'if' else operator
            recommendations.append(
                Recommendation(
                    name=f'Использование конструкции if - {operator}',
                    task=task
                ))
    return recommendations


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Умеет работать с условными и циклическими операторами',
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
