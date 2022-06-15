from testing.models import LearningOutcome
from testing.utils import get_count_duplicates_conventions


def get_learning_outcome(file_list):
    learning_outcome_duplicates = LearningOutcome(
        name=('Понимает в чем заключается дублирование кода и избегает его '
              'при помощи рефакторинга'),
    )
    learning_outcome_conventions = LearningOutcome(
        name='Следует руководству по стилю',
    )

    if not file_list:
        learning_outcome_duplicates.score = 2
        learning_outcome_conventions.score = 2
        return learning_outcome_duplicates, learning_outcome_conventions

    duplicates_count, conventions_count = get_count_duplicates_conventions(
        file_list)

    if duplicates_count in (2, 3):
        learning_outcome_duplicates.score = 4
    elif duplicates_count > 3:
        learning_outcome_duplicates.score = 3

    if conventions_count:
        conv_percentage = len(file_list) * 100 / conventions_count
        if conv_percentage >= 95:
            learning_outcome_conventions.score = 5
        elif conv_percentage >= 80:
            learning_outcome_conventions.score = 4
        elif conv_percentage >= 70:
            learning_outcome_conventions.score = 3
        else:
            learning_outcome_conventions.score = 2

    return learning_outcome_duplicates, learning_outcome_conventions
