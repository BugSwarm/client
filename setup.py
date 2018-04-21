from setuptools import setup
from setuptools import find_packages

setup(
    name='bugswarm-client',
    version='0.0.1',
    url='https://github.com/BugSwarm/client',
    author='BugSwarm',
    author_email='dev.bugswarm@gmail.com',

    description='The BugSwarm CLI',
    long_description='The BugSwarm CLI',
    zip_safe=False,
    packages=find_packages(),
    namespace_packages=[
        'bugswarm',
    ],
    install_requires=[
        'Click==6.7',
        'requests==2.18.4',
        'bugswarm-common==0.0.1',
    ],
    dependency_links=[
        'git+https://github.com/BugSwarm/common.git#egg=bugswarm-common-0.0.1',
    ],

    entry_points={
        'console_scripts': [
            'bugswarm = bugswarm.client.bugswarm:cli',
        ],
    },
)
