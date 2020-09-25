from setuptools import setup

setup(
    name='bigmuddy',
    version='0.1',
    description='Big Muddy Railroad IO Utilities',
    author='Willy Mills',
    # packages=['bigmuddy'],
    include_package_data=True,
    install_requires=[
        'click',
        'RPi.GPIO',
    ],
)
