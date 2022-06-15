import os
import sys
import importlib

from tester_with_running import TestResult
from logger_utils import get_logger

logger = get_logger(__name__)


def with_custom_dir_and_python_path(func):
    """
    Decorator for setting current directory and PYTHONPATH before running
    testing and after.
    """

    def wrapper(base_dir, *args, **kwargs):
        # Save cwd for future recovering
        cwd = os.getcwd()
        # Set current directory to dir with solutions
        os.chdir(base_dir)
        # Add solutions dir to PYTHONPATH
        sys.path.append(base_dir)

        res = func(base_dir, *args, **kwargs)

        # Recover all settings
        sys.path.remove(base_dir)
        os.chdir(cwd)

        return res

    return wrapper


def reload_module(module_name: str) -> None:
    """
    Importing or Re-importing module and its parent modules.
    I.e. for the case 'from foo.bar import hello' need to reloading 'foo.bar'
    and 'foo'. And after call main importing.

    :param module_name: full module name with parents.
    :return: if module is not exists, raise ImportError. Else None.
    """
    if '.' in module_name:
        parent = module_name.split('.')[0]
        reload_module(parent)

    if module_name in sys.modules:
        del sys.modules[module_name]

    importlib.import_module(module_name)


@with_custom_dir_and_python_path
def testing_module_10_task_1(base_dir: str) -> list[TestResult]:
    try:
        reload_module('topic_10.task_1_mean_function')
        from topic_10.task_1_mean_function import mean
    except ImportError:
        return [TestResult(0, False, 'Import error')]

    results = []
    if mean() != 0.0:
        results.append(TestResult(0, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(0, True, 'ACCESS'))

    if mean(7) != 7.0:
        results.append(TestResult(1, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(1, True, 'ACCESS'))

    if mean(1.5, True, ['джфыщкпл'], 'beegeek', 2.5, (1, 2)) != 2.0:
        results.append(TestResult(2, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(2, True, 'ACCESS'))

    if mean(True, ['stop'], 'beegeek', (1, 2)) != 0.0:
        results.append(TestResult(3, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(3, True, 'ACCESS'))

    if mean(-1, 2, 3, 10, ('5')) != 3.5:
        results.append(TestResult(4, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(4, True, 'ACCESS'))

    return results


@with_custom_dir_and_python_path
def testing_module_10_task_2(base_dir: str) -> list[TestResult]:
    try:
        reload_module('topic_10.task_2_filling_matrix')
        from topic_10.task_2_filling_matrix import matrix
    except ImportError:
        return [TestResult(0, False, 'Import error')]

    results = []
    if matrix() != [[0]]:
        results.append(TestResult(0, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(0, True, 'ACCESS'))

    if matrix(3) != [[0, 0, 0], [0, 0, 0], [0, 0, 0]]:
        results.append(TestResult(1, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(1, True, 'ACCESS'))

    if matrix(2, 5) != [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]:
        results.append(TestResult(2, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(2, True, 'ACCESS'))

    if matrix(3, 4, 9) != [[9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9]]:
        results.append(TestResult(3, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(3, True, 'ACCESS'))

    return results


@with_custom_dir_and_python_path
def testing_module_10_task_4(base_dir: str) -> list[TestResult]:
    try:
        reload_module('topic_10.task_4_info_kwargs_function')
        from topic_10.task_4_info_kwargs_function import info_kwargs
    except ImportError:
        return [TestResult(0, False, 'Import error')]

    output = info_kwargs(first_name='Timur', last_name='Guev', age=28,
                         job='teacher')
    expected = 'age: 28\nfirst_name: Timur\njob: teacher\nlast_name: Guev'

    results = []
    if output.strip() != expected:
        results.append(TestResult(0, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(0, True, 'ACCESS'))

    return results


@with_custom_dir_and_python_path
def testing_module_10_task_8(base_dir: str) -> list[TestResult]:
    try:
        reload_module('topic_10.task_8_negative_non_negative')
        from topic_10.task_8_negative_non_negative import is_non_negative_num
    except ImportError:
        return [TestResult(0, False, 'Import error')]

    results = []
    if is_non_negative_num('10.34ab') != False:
        results.append(TestResult(0, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(0, True, 'ACCESS'))

    if is_non_negative_num('10.45') != True:
        results.append(TestResult(1, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(1, True, 'ACCESS'))

    if is_non_negative_num('-18') != False:
        results.append(TestResult(2, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(2, True, 'ACCESS'))

    if is_non_negative_num('123.122.12') != False:
        results.append(TestResult(3, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(3, True, 'ACCESS'))

    if is_non_negative_num('987') != True:
        results.append(TestResult(4, False, 'WRONG ANSWER'))
    else:
        results.append(TestResult(4, True, 'ACCESS'))

    return results


@with_custom_dir_and_python_path
def testing_module_11_task_1(base_dir: str) -> list[TestResult]:
    try:
        reload_module('topic_11.task_1_vector')
        from topic_11.task_1_vector import Position
    except ImportError:
        return [TestResult(0, False, 'Import error')]

    # If any of methods is not implemented, return WRONG ANSWER
    methods = ('__add__', '__sub__', '__mul__', '__floordiv__',
               '__truediv__', '__mod__')
    if not all(method in Position.__dict__ for method in methods):
        return [TestResult(0, False, 'WRONG ANSWER')]

    p1 = Position(24, 36)
    p2 = Position(12, 18)

    results = []
    try:
        add_pos = p1 + p2
        if add_pos.x != 36 or add_pos.y != 54:
            results.append(TestResult(0, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(0, True, 'ACCESS'))

        sub_pos = p1 - p2
        if sub_pos.x != 12 or sub_pos.y != 18:
            results.append(TestResult(1, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(1, True, 'ACCESS'))

        mul_pos = p1 * p2
        if mul_pos.x != 288 or mul_pos.y != 648:
            results.append(TestResult(2, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(2, True, 'ACCESS'))

        floordiv_pos = p1 // p2
        if floordiv_pos.x != 2 or floordiv_pos.y != 2:
            results.append(TestResult(3, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(3, True, 'ACCESS'))

        truediv_pos = p1 / p2
        if truediv_pos.x != 2.0 or truediv_pos.y != 2.0:
            results.append(TestResult(4, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(4, True, 'ACCESS'))

        mod_pos = p1 % p2
        if mod_pos.x != 0 or mod_pos.y != 0:
            results.append(TestResult(5, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(5, True, 'ACCESS'))
    except TypeError as e:
        return [TestResult(0, False, 'WRONG ANSWER')]
    except AttributeError as e:
        return [TestResult(0, False, 'WRONG ANSWER')]

    return results


@with_custom_dir_and_python_path
def testing_module_12_task_1(base_dir: str) -> list[TestResult]:
    try:
        reload_module('topic_12.task_1_book_card')
        from topic_12.task_1_book_card import BookCard
    except ImportError:
        return [TestResult(0, False, 'Import error')]

    methods = ('__init__', '__lt__', '__eq__')

    private_attrs = ('_author', '_title', '_publishing_house', '_year',
                     '_num_pages', '_num_copies')
    annotations = BookCard.__dict__.get('__annotations__')

    # If not exists all need private attributes
    if not all(attr in annotations for attr in private_attrs):
        return [TestResult(0, False, 'WRONG ANSWER')]

    # If methods not implemented
    if not all(meth in BookCard.__dict__ for meth in methods):
        return [TestResult(0, False, 'WRONG ANSWER')]

    results = []
    # Checking setters and getters for all attributes
    try:
        book_card = BookCard(author='Рустам',
                             title='Крутая книга',
                             publishing_house='Дом №1',
                             year=2022,
                             num_pages=500,
                             num_copies=1000000)

        book_card.author = 'Не Рустам'
        if book_card._author != 'Не Рустам' or book_card.author != 'Не Рустам':
            results.append(TestResult(0, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(0, True, 'ACCESS'))

        book_card.title = 'Не Крутая книга'
        if (book_card._title != 'Не Крутая книга' or
                book_card.title != 'Не Крутая книга'):
            results.append(TestResult(1, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(1, True, 'ACCESS'))

        book_card.publishing_house = 'Дом №2'
        if (book_card._publishing_house != 'Дом №2' or
                book_card.publishing_house != 'Дом №2'):
            results.append(TestResult(2, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(2, True, 'ACCESS'))

        book_card.year = 2023
        if book_card._year != 2023 or book_card.year != 2023:
            results.append(TestResult(3, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(3, True, 'ACCESS'))

        book_card.num_pages = 200
        if book_card._num_pages != 200 or book_card.num_pages != 200:
            results.append(TestResult(4, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(4, True, 'ACCESS'))

        book_card.num_copies = 1000
        if book_card._num_copies != 1000 or book_card.num_copies != 1000:
            results.append(TestResult(4, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(4, True, 'ACCESS'))
    except TypeError:
        return [TestResult(0, False, 'WRONG ANSWER')]
    except NameError:
        return [TestResult(0, False, 'WRONG ANSWER')]
    except AttributeError:
        return [TestResult(0, False, 'WRONG ANSWER')]

    return results


@with_custom_dir_and_python_path
def testing_module_13_task_1(base_dir: str) -> list[TestResult]:
    try:
        reload_module('topic_13.task_1_figure')
        from topic_13.task_1_figure import Shape, Circle, Rectangle, Square
    except ImportError:
        return [TestResult(0, False, 'Import error')]

    # Base class of Circle and Rectangle - Shape
    for _class in (Circle, Rectangle):
        bases = _class.__bases__
        if len(bases) != 1 or Shape not in bases:
            return [TestResult(0, False, 'WRONG ANSWER')]

    # Base class of Square - Rectangle
    if len(Square.__bases__) != 1 or Rectangle not in Square.__bases__:
        return [TestResult(0, False, 'WRONG ANSWER')]

    # Methods must be in all classes
    methods = ('get_perimeter', 'get_square')
    for _class in (Shape, Circle, Rectangle, Square):
        if not all(meth in _class.__dict__ for meth in methods):
            return [TestResult(0, False, 'WRONG ANSWER')]

    results = []
    # Checking methods of each class
    try:
        circle = Circle(6)
        if circle.get_square() != 113.04 or circle.get_perimeter() != 37.68:
            results.append(TestResult(0, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(0, True, 'ACCESS'))

        rectangle = Rectangle(3, 4)
        if rectangle.get_square() != 12 or rectangle.get_perimeter() != 14:
            results.append(TestResult(1, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(1, True, 'ACCESS'))

        square = Square(5)
        if square.get_square() != 25 or square.get_perimeter() != 20:
            results.append(TestResult(2, False, 'WRONG ANSWER'))
        else:
            results.append(TestResult(2, True, 'ACCESS'))
    except TypeError:
        return [TestResult(0, False, 'WRONG ANSWER')]
    except NameError:
        return [TestResult(0, False, 'WRONG ANSWER')]
    except AttributeError:
        return [TestResult(0, False, 'WRONG ANSWER')]

    return results


@with_custom_dir_and_python_path
def testing_module_13_task_2(base_dir: str) -> list[TestResult]:
    try:
        reload_module('topic_13.task_2_classes')
        from topic_13.task_2_classes import (Country, Republic, Monarchy,
                                              Kingdom)
    except ImportError:
        return [TestResult(0, False, 'Import error')]

    # Base class for Republic - Country
    if len(Republic.__bases__) != 1 or Country not in Republic.__bases__:
        return [TestResult(0, False, 'WRONG ANSWER')]

    # Base classes for Kingdom - Country and Monarchy
    kd_bases = Kingdom.__bases__
    if len(kd_bases) != 2 or not all(base in kd_bases for base in (Country,
                                                                   Monarchy)):
        return [TestResult(0, False, 'WRONG ANSWER')]

    # Methods must be implemented in every class
    methods = ('__str__', '__repr__')
    for _cls in (Country, Republic, Monarchy, Kingdom):
        if not all(meth in _cls.__dict__ for meth in methods):
            return [TestResult(0, False, 'WRONG ANSWER')]

    return [TestResult(0, True, 'ACCESS')]
