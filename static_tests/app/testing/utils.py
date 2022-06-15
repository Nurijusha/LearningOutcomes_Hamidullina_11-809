from io import StringIO
import re

import cdmpyparser
from radon.metrics import mi_visit
from pylint.lint import Run
from pylint.reporters.text import TextReporter


def get_module_info(file) -> cdmpyparser.BriefModuleInfo:
    c = cdmpyparser.getBriefModuleInfoFromFile(file)
    return c


def get_all_variables(file_name) -> set:
    # ^\s* - строка начинается с 0 или более пробелов
    # (\w+) - один или более буква, а также цифры и _
    # после знака равно любые символы
    pattern = r'^\s*(?P<variable>\w+) = .+'
    variables = set()
    with open(file_name, 'r') as file:
        for line in file.readlines():
            match = re.search(pattern, line)
            if match:
                variables.add(match.group('variable'))
    return variables


def get_class_functions_decorators(file_name) -> set:
    """
    Return decorators of methods inside classes.
    """
    decorators = set()
    c = get_module_info(file_name)
    for cls in c.classes:
        for func in cls.functions:
            for dec in func.decorators:
                decorators.add(dec.name)
    return decorators


def is_using_abstractmethod(file_list: list) -> bool:
    """ Return True if abstractmethod is exists in any file. """
    for file in file_list:
        decorators = get_class_functions_decorators(file)
        if 'abstractmethod' in decorators:
            return True
    return False


def get_classes_with_base(file_name) -> set:
    """ Return classes with parent class. """
    classes = set()
    c = get_module_info(file_name)
    for cls in c.classes:
        if cls.base:
            classes.add(cls.name)
    return classes


def is_using_inheritance(file_list: list) -> bool:
    """ Return True if inheritance class is exists in any file. """
    for file in file_list:
        if get_classes_with_base(file):
            return True
    return False


def get_classes_attributes(file_name) -> set:
    """ Return attributes of each class in file. """
    attributes = set()
    c = get_module_info(file_name)
    for cls in c.classes:
        for attr in cls.instanceAttributes:
            attributes.add(attr.name)
    return attributes


def is_using_private_attributes(file_list: list) -> bool:
    for file in file_list:
        attributes = get_classes_attributes(file)
        if attributes:
            if any([attr.startswith('_') for attr in attributes]):
                return True
    return False


def is_using_self(file_list: list) -> bool:
    """ Return True if any method in class using self argument. """
    for file in file_list:
        c = get_module_info(file)
        for cls in c.classes:
            for func in cls.functions:
                if 'self' in [k.name for k in func.arguments]:
                    return True
    return False


def is_using_constructors(file_list: list) -> bool:
    """ Return True if '__init__' function is exists in any file. """
    for file in file_list:
        module_info = get_module_info(file)
        if '__init__' in [func.name for cls in module_info.classes
                          for func in cls.functions]:
            return True
    return False


def is_using_classes(file_list: list) -> bool:
    """ Return True if class is exists in any file. """
    for file in file_list:
        module_info = get_module_info(file)
        if module_info.classes:
            return True
    return False


def is_using_methods(file_list: list) -> bool:
    """ Return True if class method is exists in any file. """
    for file in file_list:
        module_info = get_module_info(file)
        if [meth for cls in module_info.classes for meth in cls.functions]:
            return True
    return False


def get_maintainability_indexes(file_list: list) -> list:
    """
    Calculate maintainability index for each file and return list of them.
    """
    maintainability_indexes = []
    for file_name in file_list:
        with open(file_name, 'r') as file:
            code = file.read()
            mi = mi_visit(code, multi=True)
            maintainability_indexes.append(mi)
    return maintainability_indexes


def get_count_duplicates_conventions(file_list: list) -> tuple[int, int]:
    """
    Return detected duplicated code fragments and count of code style
    violations.

    :param file_list: files to checking.
    :return: duplicates_count, conventions_count
    """
    pylint_output = StringIO()
    reporter = TextReporter(pylint_output)

    # Prepare args with files and params for pylint
    args = [file for file in file_list]
    args.append('--disable=all')
    # Enable Convention category to detecting
    args.append('--enable=С')
    # Enable detecting duplicates
    args.append('--enable=R0801')
    # Disable unnecessary messages
    args.append('--disable=C0103,C2001,C1901,C0209')

    Run(args, reporter=reporter, do_exit=False)

    pattern = r'\bR0801'
    duplicates_count = len(re.findall(pattern, pylint_output.getvalue()))
    pattern = r'(module_\d+/task_\w+.py):\d+:\d+: C\d+:'
    conventions_count = len(set(re.findall(pattern, pylint_output.getvalue())))

    return duplicates_count, conventions_count
