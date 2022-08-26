from setuptools import setup, find_packages
from typing import List
import os, pathlib


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

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
path_to_init = here / 'bgameb' / '__init__.py'
version_line = list(
    filter(lambda l: l.startswith('VERSION'), open(path_to_init))
)[0]
PKG_VERSION = get_version(eval(version_line.split('=')[-1]))


setup(
    name='bgameb',
    version=PKG_VERSION,
    install_requires=get_dependencies('requirements.txt'),
    description='Board Game Builder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Konstantin Klepikov',
    author_email='oformleno@gmail.com',
    url='https://github.com/KonstantinKlepikov/BoardGameBuilder',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="boardgame",
    license='MIT',
    python_requires='>=3.8.10',
    packages=find_packages(),
)