from setuptools import setup, find_packages

setup(name='PySnip',
        author="Andrea Censi",
        author_email="andrea@cds.caltech.edu",
        version="0.1",
        package_dir={'':'src'},
        packages=find_packages('src'),
        entry_points={
         'console_scripts': [
              'pysnip-make = pysnip.make:pysnip_make_main',
           ]
        },
        install_requires=['compmake-z7'],
        extras_require={},
)

