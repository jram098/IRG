from setuptools import setup, find_packages

import os

#include the non python files
def package_files(directory, strip_leading):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            package_file = os.path.join(path, filename)
            paths.append(package_file[len(strip_leading):])
    return paths

car_templates=['templates/*']
web_controller_html = package_files('donkeycar/parts/controllers/templates', 'donkeycar/')


extra_files = car_templates + web_controller_html
print('extra_files', extra_files)

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='irmark1',
    version='1.0',
    long_description = long_description,
    description='Intelligent Racing Mark One Python Package.',
    url='https://github.com/augcog/IRG',
    author='Allen Y. Yang',
    author_email='yang@eecs.berkeley.edu',
    license='Apache v2.0',
    entry_points={
        'console_scripts': [
            'irg=irmark1.management.base:execute_from_command_line',
        ],
    },
    install_requires=['numpy', 
                      'pillow',
                      'docopt',
                      'tornado',
                      'requests',
                      'h5py',
                      'moviepy',
                      'pandas',
                      'PrettyTable',
                      'paho-mqtt'
                     ],

    extras_require={
                    'nano': [
                        'Adafruit_PCA9685',                        
                        ],
                    'pc': [
                        'matplotlib',
                        ],
                    'dev' : [
                        'pytest',
                        'pytest-cov',
                        'responses',
                        ],
                    'ci': ['codecov'],
                    'tf': ['tensorflow>=1.9.0'],
                    'tf_gpu': ['tensorflow-gpu>=1.9.0'],
                    },
    package_data={
        'irmark1': extra_files, 
        },

      include_package_data=True,

      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: Apache License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.

          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='selfdriving cars',

      packages=find_packages(exclude=(['tests', 'docs', 'site', 'env'])),
      )
