from setuptools import setup
import viff

long_description = open('README.md').read()

REQUIREMENTS = ['numpy',
                'sys']

CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3 :: Only']

setup(name='viff',
      version=viff.__version__,
      description='Read and write old Khoros/VisiQuest viff and xv formats',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/patrick-c-odriscoll/viff-xv',
      author="Patrick C O'Driscoll",
      author_email='patrick.c.odriscoll@gmail.com',
      license='MIT',
      py_modules=['viff'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='viff xv khoros visiquest')
