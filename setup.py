from setuptools import setup, find_packages
import sys

long_description = "Power User Tools make your life so much easier."

sys.executable = '/usr/bin/env python3'

setup(
    name="power-user-tools",
    version="0.1.8",
    author="dameyerdave",
    author_email="dameyerdave@gmail.com",
    url="https://github.com/dameyerdave/power-user-tools",
    description="Power User Tools make your life so much easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "sussh = commands.sshutils:sussh",
            "surtun = commands.sshutils:surtun",
            "suftun = commands.sshutils:suftun",
            "sumount = commands.sshutils:sumount",
            "dcc = commands.dockertools:dcc",
            "dtls = commands.dockertools:dtls",
            "dtail = commands.dockertools:dtail",
            "dtsh = commands.dockertools:dtsh",
            "dtclean = commands.dockertools:dtclean",
            "dtins = commands.dockertools:dtins",
            "dtvols = commands.dockertools:dtvols",
            "dtmounts = commands.dockertools:dtmounts",
            "xpgl = commands.devutils:xpgl",
        ]
    },
    scripts=[
        "shell/dtip",
        "shell/dtports",
        "shell/dtnet",
        "shell/dtimg",
        "shell/dtstart",
        "shell/dtstop",
        "shell/dtrestart",
        "shell/dtrm",
        "shell/xppr",
        "shell/xprandpw",
        "shell/xpgrmhistory",
        "shell/ktls",
        "shell/ktclean",
        "shell/ktdeploy",
        "shell/ktinitbash",
        "shell/ktpods",
        "shell/ktns",
    ],
    options={
        'build_scripts': {
            'executable': '/usr/bin/env python3',
        },
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="power user tools ssh sshd reverse tunnel docker easy development",
    install_requires=[
        "click==8.1.3",
        "python-dotenv==0.21.0",
        "friendlylog==1.0.2",
        "yachalk==0.1.5",
        "rich==12.6.0",
        "sh==2.0.6",
    ],
    zip_safe=False,
)
