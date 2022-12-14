from typing import List
import os, pathlib
from setuptools import setup, find_packages


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
NAME = 'bgameb'
AUTHOR = 'Konstantin Klepikov'
EMAIL = 'oformleno@gmail.com'
DESCRIPTION = 'Board Game Builder'
LONG_DESCRIPTION = (here / "README.md").read_text(encoding="utf-8")
SOURCE_URL = 'https://github.com/KonstantinKlepikov/BoardGameBuilder'
DOCS = 'https://konstantinklepikov.github.io/BoardGameBuilder/'

setup(
    name=NAME,
    install_requires=get_dependencies('requirements.txt'),
    extras_require={
        "dev": get_dependencies('requirements-dev.txt'),
    },
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=SOURCE_URL,
    project_urls={
        'Docs': DOCS,
        'Source': SOURCE_URL,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="framework",
    license='MIT',
    python_requires='>=3.9',
    packages=find_packages(exclude=('tests*',)),
    use_incremental=True,
)