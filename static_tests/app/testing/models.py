import json


class LearningOutcome:
    """ Образовательный результат. """
    def __init__(self, name, score: int = 5, recommendations: list = None):
        self.name = name
        self.score = score
        self.recommendations = recommendations if recommendations else []

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4, ensure_ascii=False)

    def __str__(self):
        return f'{self.name} - {self.score}'


class Recommendation:
    """ Рекоммендация. """
    def __init__(self, name: str, task: str):
        """
        New Recommendation.
        :param name: name of the criterion
        :param task: task to repeat (e.g. 'Модуль 1. Задача 1.')
        """
        self.name = name
        self.task = task

    def __str__(self):
        return f'{self.name} - {self.task}'
