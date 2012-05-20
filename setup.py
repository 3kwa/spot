from setuptools import setup

version = '0.1a'
readme = open('README.rst').read()

setup(
    name = 'spot',
    version = version,
    description = 'DotCloud environment loader',
    long_description = readme,
    py_modules = ['spot'],
    license = 'MIT',
    author = 'Eugene Van den Bulke',
    author_email = 'eugene.vandenbulke@gmail.com',
    url = 'http://github.com/3kwa/spot',
    test_suite = 'test_spot',
    install_requires = ['PyYAML >= 3.10'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',]
)
