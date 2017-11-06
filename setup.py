from setuptools import setup


setup(
    name='bugswarm',
    version='0.1',
    py_modules=['bugswarm'],
    install_requires=[
        'Click==6.7',
        'requests==2.18.4',
    ],
    entry_points='''
        [console_scripts]
        bugswarm=bugswarm:cli
    ''',
)
