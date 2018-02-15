from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession

setup(
    name='noonoo',
    version="1.0.0",
    description='Cleanup old (or untagged) images from an AWS ECR (Elastic Container Repository)',
    url='https://github.com/steinnes/noonoo',
    author='Steinn Eldjarn Sigurdarson',
    author_email='steinnes@gmail.com',
    keywords=['aws', 'ecr', 'docker', 'containers'],
    install_requires=[str(req.req) for req in parse_requirements("requirements.txt", session=PipSession())],
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        noonoo=noonoo:janitor
    '''
)
