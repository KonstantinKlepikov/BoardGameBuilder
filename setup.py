from setuptools import setup, find_packages
from typing import List
import os


def get_version(ver: str) -> str:
    """Get version of package

    Args:
        ver (str): version string

    Returns:
        str: version string
    """
    if not isinstance(ver[-1], int):
        return '.'.join(
            map(str, ver[:-1]) + ver[-1]
        )
    return '.'.join(map(str, ver))

def read(path: str):
    """Read textual data

    Args:
        path (str): path to file
    """
    with open(path, 'r') as f:
        return f.read()

def strip_comments(string: str) -> str:
    """Remove comments string

    Args:
        string (str): some string

    Returns:
        str: striped string
    """
    return string.split('#', 1)[0].strip()

def get_dependencies(*req: str) -> List[str]:
    """Get dependencies from requirements.txt

    Returns:
        List[str]: list of dependencies strings
    """
    return list(filter(
        None,
        [strip_comments(l) for l in open(
            os.path.join(os.getcwd(), *req)
        ).readlines()]
    ))

path_to_init = os.path.join(
    os.path.dirname(__file__), 'src', '__init__.py'
)
version_line = list(
    filter(lambda l: l.startswith('VERSION'), open(path_to_init))
)[0]
PKG_VERSION = get_version(eval(version_line.split('=')[-1]))
README = os.path.join(
    os.path.dirname(__file__), 'README.md'
)

setup(
    name='bgameb',
    version=PKG_VERSION,
    install_requires=get_dependencies('requirements.txt'),
    description='Board Game Builder',
    long_description=read(README),
    long_description_content_type='text/markdown',
    author='Konstantin Klepikov',
    author_email='oformleno@gmail.com',
    url='https://github.com/KonstantinKlepikov/BoardGameBuilder',
    license='MIT',
    python_requires='>=3.8.10',
    packages=find_packages(),
)