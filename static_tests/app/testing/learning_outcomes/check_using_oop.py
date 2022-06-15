from testing.models import LearningOutcome, Recommendation
from testing import parsers
from testing.helpers import search_with_func
import testing.utils as utils


def five(file_list: list):
    recommendations = []

    if not search_with_func(file_list,
                            func=parsers.is_exists_multiple_inheritance):
        recommendations.append(
            Recommendation(
                name='Использование множественного наследования',
                task='Тема 13. Задача 2.'
            ))

    if not search_with_func(file_list, func=parsers.is_exists_super_function):
        recommendations.append(
            Recommendation(
                name='Использование super()',
                task='Тема 13. Задача 2.'
            ))
    return recommendations


def four(file_list: list):
    recommendations = []

    if not utils.is_using_abstractmethod(file_list):
        recommendations.append(
            Recommendation(
                name='Использование абстрактных классов',
                task='Тема 13. Задача 1.'
            ))

    if not search_with_func(file_list, func=parsers.is_exists_getter_setters):
        recommendations.append(
            Recommendation(
                name='Использование геттеров и сеттеров',
                task='Тема 12. Задача 1.'
            ))

    if not utils.is_using_inheritance(file_list):
        recommendations.append(
            Recommendation(
                name=('Использование наследования в соответствии с правилами '
                      'наследования методов и атрибутов'),
                task='Тема 13. Задача 1.'
            ))

    return recommendations


def three(file_list: list):
    recommendations = []

    if not utils.is_using_private_attributes(file_list):
        recommendations.append(
            Recommendation(
                name='Указание приватных атрибутов',
                task='Тема 12. Задача 1.'
            ))

    if not utils.is_using_self(file_list):
        recommendations.append(
            Recommendation(
                name='Использование ключевого слова self',
                task='Тема 12. Задача 1.'
            ))

    if not utils.is_using_constructors(file_list):
        recommendations.append(
            Recommendation(
                name='Использование конструктора',
                task='Тема 12. Задача 1.'
            ))

    if not utils.is_using_methods(file_list):
        recommendations.append(
            Recommendation(
                name='Создание методов',
                task='Тема 12. Задача 1.'
            ))

    if not utils.is_using_classes(file_list):
        recommendations.append(
            Recommendation(
                name='Объявление классов',
                task='Тема 12. Задача 1.'
            ))

    return recommendations


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name='Использует ООП',
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
