from __future__ import print_function, division, absolute_import
from setuptools import setup, find_packages
import sys
from codecs import open
from os import path
try: 
    from sh import pandoc
    isPandoc = True
except ImportError: 
    isPandoc = False

# Get the long description from the README file
readmepath = path.join(path.realpath(path.dirname(__file__)), 'README.md')
if path.exists(readmepath): 
    if isPandoc: 
        long_description = pandoc(readmepath, read='markdown', write='rst')
    else: 
        long_description = open(readmepath, encoding='utf-8').read()

needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
needs_wheel = {'bdist_wheel'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

setup(
    name="feaLab",

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.3.0',

    description='Tools for dealing with OpenType Layout and the Adobe FDK for OpenType FEA code.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/twardoch/feaLab',
    download_url='https://github.com/twardoch/feaLab/archive/master.zip',

    # Author details
    author='Adam Twardoch',
    author_email='adam+github@twardoch.com',

    # Choose your license
    license='LICENSE.txt',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: MacOS X',
        "Environment :: Console",
        'Operating System :: MacOS :: MacOS X', 
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords=['opentype', 'font', 'harfbuzz', 'afdko', 'svg', 'fea'], 

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    package_dir={"": "Lib"},
    packages=find_packages("Lib"),
    include_package_data=True,

    setup_requires=pytest_runner + wheel,
    tests_require=[
        'pytest>=2.8',
    ],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['sh>=1.11',
        ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'hb_render=feaLab.hb_render:main',
        ],
    },
)
