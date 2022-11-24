from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Power User Tools make your life so much easier.'

setup(
    name='power-user-tools',
    version='0.0.1',
    author='dameyerdave',
    author_email='dameyerdave@gmail.com',
    url='https://github.com/dameyerdave/power-user-tools',
    description='Power User Tools make your life so much easier',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'sussh = commands.sussh:main',
                'surtun = commands.shellex:surtun'
            ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='power user tools ssh sshd reverse tunnel docker easy development',
    install_requires=requirements,
    zip_safe=False
)
