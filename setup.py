from setuptools import setup, find_packages
from typing import List
import os, pathlib


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

setup(
    name='bgameb',
    install_requires=get_dependencies('requirements.txt'),
    extras_require={
        "dev": get_dependencies('requirements-dev.txt'),
    },
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
    keywords="framework",
    license='MIT',
    python_requires='>=3.8.10',
    packages=find_packages(),
    use_incremental=True,
    setup_requires=["incremental==21.3.0"],
)