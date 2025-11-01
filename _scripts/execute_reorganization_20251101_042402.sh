#!/bin/bash
# Reorganization execution script
# Generated: 2025-11-01 04:24:02

echo '🗂️ Starting reorganization...'
echo ''

# Move 1/8
echo '[1/8] Moving 0 files...'
mkdir -p '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_pip__internal'
mv '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/pip/_internal'/* '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_pip__internal/' 2>/dev/null
rmdir '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/pip/_internal' 2>/dev/null

# Move 2/8
echo '[2/8] Moving 0 files...'
mkdir -p '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_pip__vendor'
mv '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/pip/_vendor'/* '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_pip__vendor/' 2>/dev/null
rmdir '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/pip/_vendor' 2>/dev/null

# Move 3/8
echo '[3/8] Moving 0 files...'
mkdir -p '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_urllib3_util'
mv '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/urllib3/util'/* '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_urllib3_util/' 2>/dev/null
rmdir '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/urllib3/util' 2>/dev/null

# Move 4/8
echo '[4/8] Moving 0 files...'
mkdir -p '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_urllib3_contrib'
mv '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/urllib3/contrib'/* '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_urllib3_contrib/' 2>/dev/null
rmdir '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/urllib3/contrib' 2>/dev/null

# Move 5/8
echo '[5/8] Moving 0 files...'
mkdir -p '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_setuptools__vendor'
mv '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/setuptools/_vendor'/* '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_setuptools__vendor/' 2>/dev/null
rmdir '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/setuptools/_vendor' 2>/dev/null

# Move 6/8
echo '[6/8] Moving 0 files...'
mkdir -p '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_setuptools_config'
mv '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/setuptools/config'/* '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_setuptools_config/' 2>/dev/null
rmdir '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/setuptools/config' 2>/dev/null

# Move 7/8
echo '[7/8] Moving 0 files...'
mkdir -p '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_setuptools_command'
mv '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/setuptools/command'/* '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_setuptools_command/' 2>/dev/null
rmdir '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/setuptools/command' 2>/dev/null

# Move 8/8
echo '[8/8] Moving 0 files...'
mkdir -p '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_setuptools__distutils'
mv '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/setuptools/_distutils'/* '/Users/steven/Documents/python/leonardo/myenv/lib_python3.11_site-packages_setuptools__distutils/' 2>/dev/null
rmdir '/Users/steven/Documents/python/leonardo/myenv/lib/python3.11/site-packages/setuptools/_distutils' 2>/dev/null

echo ''
echo '✅ Reorganization complete!'
