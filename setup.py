from distutils.core import setup

setup(
    name='linkedin_auth',
    version='0.1',
    author='Michael Gile',
    author_email='mgile@mac.com',
    url='',
    description='Django application to utilize the LinkedIn API as an authentication mechanism.',
    packages=['linkedin_auth'],
    license='Apache License, Version 2.0',
    package_data={'':['*.txt']},
    requires=['simplejson', 'LinkedIn-Client-Library']
)