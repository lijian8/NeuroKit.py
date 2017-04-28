from setuptools import setup, find_packages

setup(
name = "neurokit",
description = ("A Python Toolbox for Statistics and Signal Processing (EEG, EDA, ECG, EMG...)."),
version = "0.1.1",
license = "MIT",
author = "Dominique Makowski",
author_email = "dom.makowski@gmail.com",
maintainer = "Dominique Makowski",
maintainer_email = "dom.makowski@gmail.com",
packages = find_packages(),
package_data = {},
package_data = {
        "neuropsydia.data":["*.csv"]},
install_requires = [
        'numpy',
        'pandas',
        'scipy',
        "sklearn",
        "matplotlib",
        'mne',
        'bioread',
        'nolds',
        "biosppy",
        "hrv",
        "Pillow",
        "cvxopt"],
dependency_links=[
	"https://github.com/rhenanbartels/hrv/zipball/develop"],
long_description = open('README.md').read(),
keywords = "python signal processing EEG EDA ECG hrv rpeaks biosignals complexity",
url = "https://github.com/neuropsychology/NeuroKit.py",
download_url = 'https://github.com/neuropsychology/NeuroKit.py/tarball/master',
test_suite='nose.collector',
tests_require=['nose'],
classifiers = [
	'Intended Audience :: Science/Research',
	'Intended Audience :: Developers',
	'Programming Language :: Python',
	'Topic :: Software Development',
	'Topic :: Scientific/Engineering',
	'Operating System :: Microsoft :: Windows',
	'Operating System :: Unix',
	'Operating System :: MacOS',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6']
)
