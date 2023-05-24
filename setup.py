from setuptools import setup

setup(
    name="votelib",
    version='0.1',
    py_modules=['hello'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        votelib=votelib.cli:cli
    ''',
)
