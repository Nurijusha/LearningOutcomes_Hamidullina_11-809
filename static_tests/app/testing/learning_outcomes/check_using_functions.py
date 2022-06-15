from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func
from testing.utils import get_module_info


def five(file_list: list):
    recommendations = []

    is_using_decorator = False
    for file in file_list:
        module_info = get_module_info(file)
        if 'Decorator[' in module_info.niceStringify():
            is_using_decorator = True
            break
    if not is_using_decorator:
        recommendations.append(
            Recommendation(
                name='Использует декораторы',
                task='Тема 12. Задача 1.'
            ))

    for function_name, task in (('zip', 'Тема 10. Задача 7.'),
                                ('enumerate', 'Тема 10. Задача 6.'),
                                ('all|any', 'Тема 10. Задача 3.'),
                                ('reduce', 'Тема 10. Задача 5.'),
                                ('filter', 'Тема 10. Задача 5.'),
                                ('map', 'Тема 10. Задача 5.')):
        if not search_with_func(file_list, func=parsers.is_using_function,
                                function_name=function_name):
            recommendations.append(
                Recommendation(
                    name=f'Использование функции {function_name}()',
                    task=task
                ))

    return recommendations


def four(file_list: list):
    recommendations = []
    if not search_with_func(file_list, func=parsers.is_exists_pattern,
                            pattern='lambda'):
        recommendations.append(
            Recommendation(
                name='Использование лямбда выражения',
                task='Тема 10. Задача 8.'
            ))

    for pattern, task in (('\(.*\*\*kwargs.*\)', 'Тема 10. Задача 4.'),
                          ('\(.*\*args.*\)', 'Тема 10. Задача 1.')):
        if not search_with_func(file_list, func=parsers.is_exists_pattern,
                                pattern=pattern):
            text = '**kwargs' if 'k' in pattern else '*args'
            recommendations.append(
                Recommendation(
                    name=f'Использование аргументов {text}',
                    task=task
                ))

    return recommendations


def three(file_list: list):
    recommendations = []
    is_using_functions = False
    is_using_args = False
    for file in file_list:
        module_info = get_module_info(file)
        if module_info.functions:
            is_using_functions = True
            if any([func.arguments for func in module_info.functions]):
                is_using_args = True
                break

    if not is_using_functions:
        recommendations.append(
            Recommendation(
                name='Создание функции',
                task='Тема 6. Задача 4.'
            ))
    if not is_using_args:
        recommendations.append(
            Recommendation(
                name='Передача параметров в функцию',
                task='Тема 6. Задача 4.'
            ))

    if not search_with_func(file_list, func=parsers.is_exists_pattern,
                            pattern='return'):
        recommendations.append(
            Recommendation(
                name='Использование оператора возврата значений',
                task='Тема 6. Задача 4.'
            ))
    return recommendations


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Умеет объявлять и работать с функциями',
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
