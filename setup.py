# setup.py is used to build the entire machine learning project as a package so that others can install and use it
from typing import List

from setuptools import find_packages, setup

def get_requirements(file_path: str) -> List[str]:
    '''
    This function will return the list of requirements mentioned in the requirements.txt file.
    from typing import List is used to specify the type of the return value of the function. 
    In this case, it is a list of strings.
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        # the above line will read the requirements.txt file and return a list of strings where each string is a package name.
        requirements = [req.replace("\n", "") for req in requirements]
        # this will remove the newline character from each package name in the list.
        if '-e .' in requirements:
            requirements.remove('-e .')
            # this will remove the -e . from the list of requirements as it is not a package name.
    return requirements

setup(
    name="mlproject",
    version="0.0.1",
    author = "Chibi",
    author_email = "chibidj6@gmail.com",
    packages= find_packages(),
    install_requires= get_requirements('requirements.txt')
)