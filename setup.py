from setuptools import setup
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

def read_md(path: str):
    """Read markdown for README.md

    Args:
        path (str): path to README.md
    """
    with open(path, 'r') as f:
        return f.read()


path_to_init = os.path.join(
    os.path.dirname(__file__), 'src', '__init__.py'
)
version_line = list(
    filter(lambda l: l.startswith('VERSION'), open(path_to_init))
)[0]
PKG_VERSION = get_version(eval(version_line.split('=')[-1]))
README=os.path.join(
    os.path.dirname(__file__), 'README.md'
)


setup(
    name='bgb',
    version=PKG_VERSION,
    description='Board Game Builder',
    long_description=read_md(README),
    long_description_content_type='text/markdown',
    author='Konstantin Klepikov',
    author_email='oformleno@gmail.com',
    url='https://github.com/KonstantinKlepikov/BoardGameBuilder',
    license='MIT',
)