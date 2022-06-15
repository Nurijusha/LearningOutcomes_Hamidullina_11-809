import requests
from celery.utils.log import get_task_logger

from celery import shared_task, states
from celery.result import AsyncResult
from celery.exceptions import Ignore

from .models import Solution, LearningOutcome, SolutionTesting, Recommendation

logger = get_task_logger(__name__)


def create_save_learning_outcome(solution: Solution, name: str, score: int):
    """
    Create, save and return new LearningOutcome with received parameters.
    """
    learning_outcome = LearningOutcome(
        solution=solution,
        name=name,
        score=score
    )
    logger.info(f'Create new Learning Outcome ({learning_outcome}) for '
                f'Solution ({solution})')
    learning_outcome.save()
    return learning_outcome


def create_save_learning_outcome_with_recs(solution: Solution,
                                           lo_result: dict):
    """
    Creating LearningOutcome with its recommendations.
    """
    name = lo_result.get('name')
    score = lo_result.get('score')
    if not all((name, score)):
        return
    learning_outcome = create_save_learning_outcome(solution=solution,
                                                    name=name,
                                                    score=score)
    recs_dict = lo_result.get('recommendations')
    if recs_dict:
        for rec in recs_dict:
            recommendation, _ = Recommendation.objects.get_or_create(
                name=rec['name'],
                task=rec['task']
            )
            learning_outcome.recommendations.add(recommendation)


def check_set_status_solution_testing(dynamic_test_task_id: str = None,
                                      static_test_task_id: str = None,
                                      status: str = 'SUCCESS'):
    """
    Check dynamic and static testing celery tasks states for received
    SolutionTesting (getting with one of ids) and set status.
    If any celery task FAILURE -> status = FAILURE.
    If any celery task STARTED -> status = STARTED.
    If all celery tasks SUCCESS -> status = SUCCESS.

    If received status other than 'SUCCESS' -> set SolutionCeleryTask for it.
    """
    if dynamic_test_task_id:
        solution_testing = SolutionTesting.objects.get(
            dynamic_test_task_id=dynamic_test_task_id
        )
        if not solution_testing.static_test_task_id:
            solution_testing.status = status
            solution_testing.save()
            return
    else:
        solution_testing = SolutionTesting.objects.get(
            static_test_task_id=static_test_task_id
        )
        if not solution_testing.dynamic_test_task_id:
            solution_testing.status = status
            solution_testing.save()
            return

    if status != 'SUCCESS':
        solution_testing.status = status
        solution_testing.save()
        return
    if solution_testing.status != 'STARTED':
        return

    dt_task_state = AsyncResult(solution_testing.dynamic_test_task_id).state
    st_task_state = AsyncResult(solution_testing.static_test_task_id).state

    if any(state == 'FAILURE' for state in (dt_task_state, st_task_state)):
        new_status = 'FAILURE'
    elif any(state == 'STARTED' or state == 'PENDING' for state in (dt_task_state, st_task_state)):
        new_status = 'STARTED'
    elif all(state == 'SUCCESS' for state in (dt_task_state, st_task_state)):
        new_status = 'SUCCESS'
    else:
        logger.error(f'dynamic testing task state = {dt_task_state}')
        logger.error(f'static testing task state = {st_task_state}')
        new_status = 'UNKNOWN'

    solution_testing.status = new_status
    solution_testing.save()


def set_task_state(dynamic_testing_task: shared_task = None,
                   static_testing_task: shared_task = None,
                   state: str = states.FAILURE):
    """
    Set task state and solution_celery_task status to <state> parameter.
    And update state of SolutionTesting object.

    :param dynamic_testing_task: shared_task object
    :param static_testing_task: shared_task object
    :param state: new state for task. Default - FAILURE
    :return: None
    """
    # If called from dynamic testing
    if dynamic_testing_task:
        dynamic_testing_task.update_state(state=state)
        check_set_status_solution_testing(
            dynamic_test_task_id=dynamic_testing_task.request.id,
            status=state
        )
        return
    # If called from static testing
    static_testing_task.update_state(state=state)
    check_set_status_solution_testing(
        static_test_task_id=static_testing_task.request.id,
        status=state
    )


@shared_task(bind=True)
def dynamic_testing(self, github_url: str, solution_id: int):
    """
    Running dynamic testing. Save resulting learning outcomes.
    """
    solution = Solution.objects.filter(id=solution_id).first()
    # If solution deleted from other task
    if not solution:
        set_task_state(dynamic_testing_task=self)
        # Without this raise, task state will be set to SUCCESS
        raise Ignore()

    try:
        payload = {'github_url': github_url}
        # Run dynamic testing
        response = requests.get('http://dynamic-tests:6000/do-dynamic-tests/',
                                json=payload,
                                timeout=360)
        response = response.json()
        if response.get('result') == 'error':
            set_task_state(self)
            raise Ignore()

        working_code_score = int(response.get('result'))
        create_save_learning_outcome(
            solution,
            'Умеет писать работоспособный код',
            working_code_score
        )

        # If none of the tasks passed the unit tests - access_time_score = 2
        access_time_score = 2 if working_code_score == 2 else int(
            response.get('access_time'))
        create_save_learning_outcome(
            solution,
            ('Соблюдает время работы программы,указанное в требованиях к '
             'задачам'),
            access_time_score
        )

        set_task_state(dynamic_testing_task=self, state=states.SUCCESS)
    except Exception as e:
        logger.error(e)
        # Delete solution, because testing Failed
        solution.delete()
        set_task_state(dynamic_testing_task=self)
        raise Ignore()


@shared_task(bind=True)
def static_testing(self, github_url: str, solution_id: int):
    """
    Running static testing. Save resulting learning outcomes.
    """
    solution = Solution.objects.filter(id=solution_id).first()
    # If solution deleted from other task
    if not solution:
        set_task_state(static_testing_task=self)
        # Without this raise, task state will be set to SUCCESS
        raise Ignore()

    try:
        payload = {'github_url': github_url}
        # Run static testing
        response = requests.get('http://static-tests:6001/do-static-tests/',
                                json=payload,
                                timeout=360)
        response = response.json()
        if response.get('result') == 'error':
            set_task_state(self)
            raise Ignore()
        for learning_outcome in response['result']:
            create_save_learning_outcome_with_recs(
                solution=solution,
                lo_result=learning_outcome,
            )
        set_task_state(static_testing_task=self, state=states.SUCCESS)
    except Exception as e:
        logger.error(e)
        # Delete solution, because testing Failed
        solution.delete()
        set_task_state(static_testing_task=self)
        raise Ignore()
