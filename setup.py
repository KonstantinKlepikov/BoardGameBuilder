from setuptools import setup
import os


def get_version(ver):
    if not isinstance(ver[-1], int):
        return '.'.join(
            map(str, ver[:-1]) + ver[-1]
        )
    return '.'.join(map(str, ver))


path_to_init = os.path.join(
    os.path.dirname(__file__), 'src', '__init__.py'
)
version_line = list(
    filter(lambda l: l.startswith('VERSION'), open(path_to_init))
)[0]
PKG_VERSION = get_version(eval(version_line.split('=')[-1]))


setup(
    name='bgb',
    version=PKG_VERSION,
    description='Board Game Builder',
    long_description="""
        Object oriented framework for build boardgame logic on python
        """,
    author='Konstantin Klepikov',
    author_email='oformleno@gmail.com',
    url='https://github.com/KonstantinKlepikov/BoardGameBuilder',
    license='MIT',
)