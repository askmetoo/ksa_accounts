from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ksa_accounts/__init__.py
from ksa_accounts import __version__ as version

setup(
	name="ksa_accounts",
	version=version,
	description="Localisation App for KSA Accounts",
	author="Havenir Solutions",
	author_email="hello@havenir.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
