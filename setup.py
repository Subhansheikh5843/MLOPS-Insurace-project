from setuptools import setup,find_packages

# This simple script is often saved as a file called setup.py in your project’s root directory. Its main purpose is to tell Python how to package and distribute your project so that others can install and use it easily (for example, via pip). Let’s break it down:


# setup: A function used to provide metadata and configuration settings about your package (such as the package name, version, author info, etc.). When someone runs an install command, this function tells the installer exactly how to build and install your project.

# find_packages: A helper function that automatically searches through your project directory to find all packages (folders with an __init__.py file) that should be included in the distribution. This saves you from manually listing each package.


from typing import List

HYPHON_E_DOT = "-e ."

def get_requirements(filepath:str)-> List[str]:
  requirements = []
  
  with open(filepath) as file_obj:
    requirements = file_obj.readlines()
    requirements = [i.replace("\n","") for i in requirements]
    if HYPHON_E_DOT in requirements:
      requirements.remove(HYPHON_E_DOT)
    

    
setup(name='ML_Pipeline_project',
      version='0.0.1',
      description='Machine Learning pipeline project',
      author='Subhan Mujtaba',
      author_email='subhansheikh5843@gmail.com',
      packages=find_packages(),
      install_requires = get_requirements("requirements.txt"),
     )