from setuptools import setup, find_packages

setup(
    name='cotion',
    version='1.0.0',
    packages=find_packages(),
    package_data={'cotion': ['config.json']},
    entry_points={
        'console_scripts': [
            'cotion = cotion.main:main',
        ],
    },
)

