from setuptools import find_packages, setup

setup(name='ACT4E-exercises',
      version="0.1",
      package_dir={'': 'src'},
      packages=find_packages('src'),

      entry_points={"console_scripts": ["act4e-test = act4e_tests:test_main", ]},
      extras_require={},
      )
