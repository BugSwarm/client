from distutils.core import setup


setup(
    name='bugswarm',
    packages=['client'],
    version='0.1',
    description='The BugSwarm CLI',
    author='Naji Dmeiri',
    author_email='ndmeiri@gmail.com',
    maintainer='',
    maintainer_email='',
    url='https://github.com/BugSwarm/client',
    download_url='https://github.com/BugSwarm/client/archive/0.1.tar.gz',
    keywords=['bugswarm', 'client', 'cli', 'dataset', ],

    install_requires=[
        ('Click==6.7'),
        'requests==2.18.4',
    ],
    entry_points='''
        [console_scripts]
        bugswarm=bugswarm:cli
    ''',
)
