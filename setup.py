#!/usr/bin/env python

#   Copyright 2012 Niko Usai <usai.niko@gmail.com>, http://mogui.it
#
#   this file is part of pyorient
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from setuptools import setup

setup(name='pyorient',
    version='1.1.2',
    author='Niko Usai <mogui83@gmail.com>, Domenico Lupinetti <ostico@gmail.com>',
    description='OrientDB native client library',
    long_description=open('README.md').read(),
    license='LICENSE',
    packages = [
        'pyorient',
        'pyorient.messages',
    ]
)
