from testing.models import LearningOutcome
from testing.utils import get_maintainability_indexes
from testing.helpers import get_score_from_maintainability_indexes


def get_learning_outcome(file_list):
    learning_outcome = LearningOutcome(
        name=('Понимает сложность функций и методов класса, пишет код с '
              'наименьшей сложностью'),
    )

    if not file_list:
        learning_outcome.score = 2
        return learning_outcome

    maintainability_indexes = get_maintainability_indexes(file_list)
    if not maintainability_indexes:
        learning_outcome.score = 2
        return learning_outcome
    score = get_score_from_maintainability_indexes(maintainability_indexes)

    learning_outcome.score = score

    return learning_outcome
