import os
import shutil

import git
from git import Repo

import logger_utils
from tests import testing

logger = logger_utils.get_logger(__name__)


class SolutionTests:
    # Directory for repository with solutions
    dir_with_repo = 'solutions'
    repo: git.Repo
    result: tuple[int, int] | bool
    accepted_solutions: int = 0
    tasks_count: int = 0
    timeout_count: int = 0

    def __init__(self, url):
        self.url = url

    def _prepare_dir(self):
        if os.path.exists(self.dir_with_repo):
            self._delete_dir_with_repo()

    def _download_code(self):
        """ Clone github repository by url. """
        self._prepare_dir()

        try:
            self.repo = Repo.clone_from(self.url, self.dir_with_repo)
        except Exception as e:
            logger.error(f'Error when cloning repository. url - {self.url}')
            return False
        if self.repo:
            return True
        return False

    def run_tests(self) -> tuple[float, float] | tuple[bool, bool]:
        """
        Performs dynamic testing and returns the result as a percentage.
        :return: percentage of correctly solved tasks
        """
        downloaded = self._download_code()
        if not downloaded:
            return False, False
        if os.path.isdir(self.dir_with_repo):
            result = testing(self.dir_with_repo)
            if result:
                try:
                    (self.accepted_solutions, self.tasks_count,
                     self.timeout_count) = result
                    logger.info(
                        f'Accepted count - {self.accepted_solutions}, '
                        f'Total tasks count - {self.tasks_count}, '
                        f'Timeout count - {self.timeout_count}'
                    )
                except TypeError or ValueError:
                    pass
            else:
                return False, False
        self._delete_dir_with_repo()
        # Percentage of correct solutions
        percentages_prog = self.accepted_solutions * 100 / self.tasks_count
        time_access = self.tasks_count - self.timeout_count
        # Percentage of access time solutions
        percentages_timeout = time_access * 100 / self.tasks_count
        return percentages_prog, percentages_timeout

    def _delete_dir_with_repo(self):
        # Delete cloned repository
        shutil.rmtree(self.dir_with_repo)
