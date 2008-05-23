from setuptools import setup, find_packages

version = '0.1'
readme = open('README.txt', 'rb').read()

setup(name='pleiades.normalizer',
      version=version,
      description="Normalize Latin labels of the Barrington Atlas to ASCII",
      long_description=readme,
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='latin unicode normalization',
      author='Sean Gillies',
      author_email='sgillies@frii.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pleiades'],
      include_package_data=True,
      zip_safe=False,
      test_suite='pleiades.normalizer.tests.test_suite',
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
