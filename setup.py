from setuptools import find_packages, setup

setup(name='ACT4E-exercises',
      version="1.2.2",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      extras_require={},
      zip_safe=False,
include_package_data= True
)
