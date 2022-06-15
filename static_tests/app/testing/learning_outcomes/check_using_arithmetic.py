from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func


def five(file_list: list):
    recommendations = []
    for operator in ('__truediv__', '__mul__', '__sub__', '__add__'):
        if search_with_func(file_list, operator=operator,
                            func=parsers.is_exists_overload_arithmetic):
            continue
        recommendations.append(
            Recommendation(
                name=(f'Использование перегрузки арифметических операций: '
                      f'{operator}'),
                task='Тема 11. Задача 1.'
            )
        )
    return recommendations


def four(file_list: list):
    recommendations = []
    for operator, task in (('-=', 'Тема 6. Задача 1.'),
                           ('*=', 'Тема 6. Задача 5.'),
                           ('+=', 'Тема 6. Задача 2.')):
        if search_with_func(file_list, operator=operator,
                            func=parsers.is_exists_arithmetic_operator):
            continue
        recommendations.append(
            Recommendation(
                name=f'Использование сокращенного вида: {operator}',
                task=task
            )
        )
    return recommendations


def three(file_list: list):
    recommendations = []
    for operator in ('%', '//', '**', '/', '*', '-', '+'):
        if search_with_func(file_list, operator=operator,
                            func=parsers.is_exists_arithmetic_operator):
            continue
        recommendations.append(
            Recommendation(
                name=f'Использование: {operator}',
                task='Тема 3. Задача 1.'
            )
        )
    return recommendations


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Использует арифметические операции',
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
