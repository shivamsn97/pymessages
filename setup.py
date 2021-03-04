from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pymessages',
      version='0.1',
      description='This is a Google Messages Client library to send message with a backend .eg. with flask to send otp messages. This module uses your own number to work as a sms gateway api and you can send message to other person with your own number.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: ISC License (ISCL)',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries',
      ],
      keywords='python sms-api sms-gateway google-messages',
      url='http://github.com/shivamsn97/pymessages',
      author='Shivam Saini',
      author_email='shivamsn97@gmail.com',
      license='ISC',
      packages=find_packages(),
      install_requires=[
          'pyppeteer',
          'pyee',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
