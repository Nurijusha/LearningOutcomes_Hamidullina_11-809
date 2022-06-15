# Static testing of the repository

## Образовательные результаты

- Классы для хранения образовательных результатов и рекомендаций находятся в [models.py](/testing/models.py).
- Функции получения информации о модулях должны находиться в [utils.py](/testing/utils.py).
- Функции парсинга кода модуля должны находиться в [parsers.py](/testing/parsers.py)

### Добавление проверки нового образовательного результата:

1) Создать файл для проверки в папке [testing/learning_outcomes](testing/learning_outcomes). Название файла должно начинаться на ``check_``.
2) В этом файле реализовать функцию ```get_learning_outcome```, которая принимает список файлов для проверки (все решения задач из репозитория) и возвращает образовательный результат (экземпляр класса LearningOutcome).

```python
from testing.models import LearningOutcome, Recommendation


def five(file_list: list) -> [] | [Recommendation]:
    # Проверка на выполнение критериев 5го уровня
    pass


def four(file_list: list) -> [] | [Recommendation]:
    # Проверка на выполнение критериев 4го уровня
    pass


def three(file_list: list) -> [] | [Recommendation]:
    # Проверка на выполнение критериев 3го уровня
    pass


def get_learning_outcome(file_list: list) -> LearningOutcome:
    learning_outcome = LearningOutcome(
        name='Название Образовательного результата'
    )
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
```
---
## Дополнительная информация
- На выполнение критериев (образовательных результатов) проверяются файлы из полученного репозитория, названия которых начинаются на ``task_``. Например, task_1_cesar.py.
- 