from setuptools import setup, find_packages

setup(
    name='mgToolApi',
    
    version='0.3',
    description='MuG Tool API',
    
    url='http://www.multiscalegenomics.eu',
    download_url='https://github.com/Multiscale-Genomics/mg-tool-api',
    
    author='Marco Pasi, Javier Conejero',
    author_email='',

    license='GPL v2',

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
