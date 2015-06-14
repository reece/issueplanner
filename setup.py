from setuptools import setup, find_packages

import glob
import logging
import os


logging.basicConfig(
    level=logging.getLevelName(os.environ.get("BIOCOMMONS_LOG_LEVEL", "WARN")))

package_name="issueplanner"
short_description = "" #open("docs/short.txt").read().strip()
long_description = "" #open("docs/long.txt").read().strip()


setup(
    author="Reece Hart",
    author_email="reecehart@gmail.com",
    license="Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)",
    url="https://bitbucket.org/reece/" + package_name,

    description=short_description,
    long_description=long_description,
    name=package_name,
    packages=find_packages(),
    scripts = glob.glob("scripts/*"),
    #use_vcs_version={"version_handler": version_handler},
    zip_safe=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
      ],

    # keywords=[
    # ],

    # install_requires=[
    # ],

    setup_requires=[
        "hgtools",
        "wheel",
        "sphinx",
        "sphinxcontrib-fulltoc",
    ],

    tests_require=[
    #    "coverage",
    ],
)

## <LICENSE>
## Copyright 2014 HGVS Contributors (https://bitbucket.org/biocommons/hgvs)
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>
