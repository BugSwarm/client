from setuptools import setup
from setuptools import find_packages

setup(
    name='bugswarm-client',
    version='0.0.3',
    url='https://github.com/BugSwarm/client',
    author='BugSwarm',
    author_email='dev.bugswarm@gmail.com',

    description='The official command line client for the BugSwarm artifact dataset',
    long_description='The official command line client for the BugSwarm artifact dataset',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ],
    zip_safe=False,
    packages=find_packages(),
    namespace_packages=[
        'bugswarm',
    ],
    install_requires=[
        'Click==6.7',
        'requests==2.18.4',
        'bugswarm-common==0.0.3',
    ],

    entry_points={
        'console_scripts': [
            'bugswarm = bugswarm.client.bugswarm:cli',
        ],
    },
)
