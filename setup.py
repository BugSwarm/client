from distutils.core import setup

setup(
    name='bugswarm',
    version='0.0.1',
    url='https://github.com/BugSwarm/client',
    author='BugSwarm',
    author_email='dev.bugswarm@gmail.com',
    description='The BugSwarm CLI',
    keywords=[
        'bugswarm',
        'client',
        'cli',
    ],
    zip_safe=False,
    py_modules=[
        'main',
    ],
    install_requires=[
        'Click==6.7',
        'requests==2.18.4',
        'bugswarm-common==0.0.1',
    ],
    dependency_links=[
        'git+https://github.com/BugSwarm/common.git#egg=bugswarm-common-0.0.1',
    ],

    entry_points='''
        [console_scripts]
        bugswarm=main:cli
    ''',
)
