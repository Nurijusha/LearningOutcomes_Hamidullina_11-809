from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func


def five(file_list: list):
    recommendations = []
    if not search_with_func(file_list, parsers.is_exists_generator_of_sets):
        recommendations.append(
            Recommendation(
                name=f'Использование генераторов множества',
                task='Тема 7. Задача 3.'
            )
        )
    if not search_with_func(file_list, parsers.is_using_method,
                            method_name='issuperset|issubset|isdisjoint'):
        recommendations.append(
            Recommendation(
                name=(f'Использование методов для подмножеств или '
                      f'надмножеств: issuperset(), или issubset(), или '
                      f'isdisjoint()'),
                task='Тема 7. Задача 5.'
            )
        )
    return recommendations


def four(file_list: list):
    recommendations = []
    if not search_with_func(file_list, func=parsers.is_using_method,
                            method_name=('update|intersection_update|'
                                         'difference_update|'
                                         'symmetric_difference_update')):
        recommendations.append(
            Recommendation(
                name=('Использование методов для изменения множества:'
                      'или update(), или intersection_update(), '
                      'или difference_update(), '
                      'или symmetric_difference_update()'),
                task='Тема 7. Задача 4.'
            ))
    if not search_with_func(file_list, func=parsers.is_using_method,
                            method_name=('union|intersection|difference|'
                                         'symmetric_difference')):
        recommendations.append(
            Recommendation(
                name=('Использование методов: union(), или intersection(),'
                      'или difference(), или symmetric_difference()'),
                task='Тема 7. Задача 2.'
            ))
    if not search_with_func(file_list, func=parsers.is_using_method,
                            method_name='remove|discard|pop|clear'):
        recommendations.append(
            Recommendation(
                name=('Удаление из множества - либо remove(), либо'
                      'discard(), либо pop(), либо clear()'),
                task='Тема 7. Задача 3.'
            ))
    if not search_with_func(file_list, func=parsers.is_using_method,
                            method_name='add'):
        recommendations.append(
            Recommendation(
                name='Добавление элементов в множество - add()',
                task='Тема 7. Задача 1.'
            ))
    return recommendations


def three(file_list: list):
    recommendations = []
    if not search_with_func(file_list, parsers.is_using_function,
                            function_name='sum|min|max'):
        recommendations.append(
            Recommendation(
                name=('Использование встроенних функций: sum(), или min(), '
                      'или max()'),
                task='Тема 7. Задача 2.'
            ))
    if not search_with_func(file_list, parsers.is_exists_getting_length):
        recommendations.append(
            Recommendation(
                name='Длина множества',
                task='Тема 7. Задача 1.'
            ))
    if not search_with_func(file_list, parsers.is_exists_creating_set):
        recommendations.append(
            Recommendation(
                name='Создание множества',
                task='Тема 7. Задача 4.'
            ))
    return recommendations


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Умеет работать с множествами',
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
