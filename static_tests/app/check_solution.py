import os
import shutil
import importlib.util
from typing import Iterable

import git
from git import Repo

from logger_utils import get_logger

logger = get_logger(__name__)


class SolutionTests:
    # Directory for repository with solutions
    dir_with_repo = 'solutions'
    repo: git.Repo
    file_list: list = []

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

    def run_tests(self):
        """
        Performs static testing and returns the result as a list of learning
        outcomes.
        :return: [LearningOutcome] for this solution or False if error
        """
        downloaded = self._download_code()
        if not downloaded or not os.path.isdir(self.dir_with_repo):
            return False
        if not self._get_files_list():
            return False

        lo_dir = 'testing/learning_outcomes'
        checks = [os.path.join(lo_dir, x) for x in os.listdir(lo_dir) if
                  x.startswith('check_')]
        learning_outcomes = []

        for lo_file in checks:
            spec = importlib.util.spec_from_file_location("lo_module",
                                                          lo_file)
            lo_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lo_module)
            try:
                logger.info(f'Начало проверки с файлом {lo_file}')
                lo = lo_module.get_learning_outcome(self.file_list)
                # If returned more then one learning outcome
                if isinstance(lo, Iterable):
                    for item in lo:
                        learning_outcomes.append(item)
                else:
                    learning_outcomes.append(lo)
            except AttributeError:
                logger.error(f'В файле {lo_file} отсутствует функция '
                             f'get_learning_outcome')

        self._delete_dir_with_repo()

        return learning_outcomes

    def _delete_dir_with_repo(self):
        # Delete cloned repository
        shutil.rmtree(self.dir_with_repo)

    def _get_files_list(self):
        """ Recursive creating list with .py files. """
        self.file_list.clear()
        for root, dirs, files in os.walk(self.dir_with_repo, topdown=True):
            dirs[:] = [x for x in dirs if 'venv' not in x
                       and 'pycache' not in x]
            for file in files:
                if file.endswith('.py'):
                    self.file_list.append(os.path.join(root, file))
        return True
