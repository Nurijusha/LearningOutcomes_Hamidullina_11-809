from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func


def five(file_list: list):
    if search_with_func(
            file_list,
            func=parsers.is_using_function, function_name='ord|chr'):
        return []
    return [
        Recommendation(
            name='Хранение строки в памяти: использование ord() или'
                 'chr()',
            task='Тема 4. Задача 1.'
        )
    ]


def four(file_list: list):
    recommendations = []
    for method_name, task in (('replace', 'Тема 10. Задача 8.'),
                              ('find', 'Тема 4. Задача 3.'),
                              ('lower|upper', 'Тема 4. Задача 2.'),
                              ('split|join', 'Тема 6. Задача 2.')):
        if search_with_func(file_list, func=parsers.is_using_method,
                            method_name=method_name):
            continue
        recommendations.append(
            Recommendation(
                name=f'Использование методов: {method_name}',
                task=task
            )
        )
    if not search_with_func(file_list, func=parsers.is_exist_slices):
        recommendations.append(
            Recommendation(
                name='Использование срезов',
                task='Тема 10. Задача 5.'
            )
        )
    return recommendations


def three(file_list: list):
    recommendations = []
    if not search_with_func(file_list,
                            func=parsers.is_exists_str_iteration):
        recommendations.append(
            Recommendation(
                name='Использование итерирования строк',
                task='Тема 4. Задача 1.'
            )
        )
    if not search_with_func(file_list, func=parsers.is_exists_indexing):
        recommendations.append(
            Recommendation(
                name='Использование индексации',
                task='Тема 4. Задача 1.'
            )
        )
    if not search_with_func(file_list, func=parsers.is_exists_getting_length):
        recommendations.append(
            Recommendation(
                name='Длина строки',
                task='Тема 10. Задача 5.'
            )
        )
    if not search_with_func(file_list,
                            func=parsers.is_exists_creating_str):
        recommendations.append(
            Recommendation(
                name='Создание строки',
                task='Тема 4. Задача 1.'
            )
        )
    return recommendations


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Умеет работать со строками',
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
