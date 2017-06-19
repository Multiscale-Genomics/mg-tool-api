from setuptools import setup, find_packages

setup(
    name='mgToolApi',
    version='0.3',
    description='MuG DMP API',
    
    url='http://www.multiscalegenomics.eu',
    download_url='https://github.com/Multiscale-Genomics/mg-tool-api',
    
    author='Marco Pasi, Javier Conejero',
    #author_email='',
    
    license='Apache 2.0',
    
    packages=find_packages(),
    
    install_requires = [
        'configparser', 'pytest'
    ],

    tests_require=[
        'pytest',
    ],
)
