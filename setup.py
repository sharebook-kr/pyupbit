import io
import os

from setuptools import setup


def get_spec(filename, mode='r'):
    def wrapper():
        here = os.path.dirname(__file__)
        result = {}
        with io.open(os.path.join(here, filename), encoding='utf-8') as src_file:
            result = src_file.read()
        return result
    return wrapper


get_requirements = get_spec('requirements.txt')
setup(
    name            = 'pyupbit',
    version         = '0.2.6',
    description     = 'python wrapper for Upbit API',
    url             = 'https://github.com/sharebook-kr/pyupbit',
    author          = 'Lukas Yoo, Brayden Jo',
    author_email    = 'brayden.jo@outlook.com, jonghun.yoo@outlook.com, pystock@outlook.com',
    install_requires= get_requirements(),
    license         = 'MIT',
    packages        = ['pyupbit'],
    zip_safe        = False
)
