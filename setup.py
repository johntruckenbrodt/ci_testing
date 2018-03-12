from setuptools import setup, find_packages

setup(name='ci_testing',
      packages=find_packages(),
      include_package_data=True,
      version='0.2',
      description='just some testing of Travis CI',
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
      ],
      install_requires=['progressbar2',
                        'pathos>=0.2',
                        'numpy',
                        'scoop'],
      url='https://github.com/johntruckenbrodt/ci_testing.git',
      author='John Truckenbrodt',
      author_email='john.truckenbrodt@uni-jena.de',
      license='MIT',
      zip_safe=False)
