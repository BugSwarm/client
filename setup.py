from setuptools import setup


setup(
    name='bugswarm',
    version='0.1',
    py_modules=['bugswarm'],
    install_requires=[
        'Click==6.7',
    ],
    entry_points='''
        [console_scripts]
        bugswarm=bugswarm:cli
    ''',
)
