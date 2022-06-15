from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func


def five(file_list: list):
    recommendations = []
    if not search_with_func(file_list, func=parsers.is_exists_pattern,
                            pattern=r'.ljust\(|.rjust\('):
        recommendations.append(
            Recommendation(
                name=f'Использование функции ljust() или rjust()',
                task='Тема 6. Задача 2.'
            )
        )
    if not search_with_func(
            file_list,
            func=parsers.is_exists_iteration_through_nested_list):
        recommendations.append(
            Recommendation(
                name=f'Перебор элементов вложенных списков',
                task='Тема 6. Задача 2.'
            ))
    if not search_with_func(file_list, func=parsers.is_using_function,
                            function_name='min|max|len'):
        recommendations.append(
            Recommendation(
                name=(f'Использование функции min() или max(), или len() со '
                      f'вложенными списками'),
                task='Тема 6. Задача 4.'
            ))
    if not search_with_func(file_list, parsers.is_exists_indexing_nested_list):
        recommendations.append(
            Recommendation(
                name=f'Использование индексации с вложенными списками',
                task='Тема 6. Задача 2.'
            ))
    if not search_with_func(file_list, parsers.is_exists_creating_nested_list):
        recommendations.append(
            Recommendation(
                name=f'Создание вложенных списков',
                task='Тема 6. Задача 2.'
            ))
    return recommendations


def four(file_list: list):
    recommendations = []
    if not search_with_func(file_list,
                            func=parsers.is_exists_list_expression):
        recommendations.append(
            Recommendation(
                name='Использование списочных выражений',
                task='Тема 6. Задача 2.'
            ))
    if not search_with_func(file_list,
                            func=parsers.is_exists_del_list):
        recommendations.append(
            Recommendation(
                name='Удаление элементов - del',
                task='Тема 6. Задача 5.'
            ))
    if not search_with_func(file_list, func=parsers.is_using_method,
                            method_name='extend'):
        recommendations.append(
            Recommendation(
                name='Расширение списков - extend',
                task='Тема 6. Задача 5.'
            ))
    if not search_with_func(file_list, func=parsers.is_using_method,
                            method_name='insert'):
        recommendations.append(
            Recommendation(
                name='Добавление элементов в списки - insert',
                task='Тема 6. Задача 5.'
            ))
    if not search_with_func(file_list, func=parsers.is_using_method,
                            method_name='append'):
        recommendations.append(
            Recommendation(
                name='Добавление элементов в списки - append',
                task='Тема 6. Задача 2.'
            ))
    return recommendations


def three(file_list: list):
    recommendations = []
    if not search_with_func(file_list, func=parsers.is_exist_slices):
        recommendations.append(
            Recommendation(
                name=f'Использование срезов',
                task='Тема 4. Задача 2.'
            ))
    if not search_with_func(file_list, func=parsers.is_exists_indexing):
        recommendations.append(
            Recommendation(
                name=f'Использование индексации',
                task='Тема 6. Задача 1.'
            ))
    if not search_with_func(file_list, func=parsers.is_exists_getting_length):
        recommendations.append(
            Recommendation(
                name=f'Длина списка',
                task='Тема 6. Задача 2.'
            ))
    if not search_with_func(file_list, func=parsers.is_exists_creating_list):
        recommendations.append(
            Recommendation(
                name=f'Создание списков',
                task='Тема 10. Задача 5.'
            ))
    return recommendations


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Умеет работать со списками и воспроизводит операции над ними',
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
