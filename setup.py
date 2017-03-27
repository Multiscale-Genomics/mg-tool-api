from setuptools import setup, find_packages

setup(
    name='mg-tool-api',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
