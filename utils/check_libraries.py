#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2012 The Plaso Project Authors.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This file contains simple checks for versions of dependent tools."""
import re
import urllib2
import OleFileIO_PL

LIBRARIES = ['pyevt', 'pyevtx', 'pylnk', 'pymsiecf', 'pyregf', 'pyvshadow']


def CheckVersion(library):
  """Return the version number for a given library."""
  url = urllib2.urlopen('http://code.google.com/p/{}/downloads/list'.format(
      library))
  if url.code != 200:
    return 0

  library_re = re.compile(' ({}.+tar.gz)'.format(library), re.I)
  data = url.read()
  m = library_re.search(data)
  if not m:
    return 0

  _, _, end_part = m.group(1).rpartition('-')
  version, _, _ = end_part.partition('.')

  return int(version)


def GetOleIOVersion():
  """Returns the version number for the current OleFileIO version.

  Returns:
    Current version number of OleFileIO_PL as a float or 0.0 if there is
    an error in determining the version number.
  """
  url = urllib2.urlopen('https://bitbucket.org/decalage/olefileio_pl/src/')
  library_re = re.compile(r'decalage/olefileio_pl/src/([0-9a-fA-F]+)/')

  if url.code != 200:
    return 0.0

  cur_code = ''
  while not cur_code:
    line = url.readline()
    if not line:
      break
    m = library_re.search(line)
    if m:
      cur_code = m.group(1)


  url_version =  urllib2.urlopen((
      'https://bitbucket.org/decalage/olefileio_pl/src/{}/OleFileIO_PL/'
      'OleFileIO_PL.py').format(
          cur_code))

  line = url_version.readline()
  version = ''
  while line:
    if '__version__' in line:
      entries = line.split('&#')
      if len(entries) == 3:
        _, version = entries[1].split(';')
        break
    line = url_version.readline()

  if not version:
    return 0.0

  return float(version)


if __name__ == '__main__':
  print 'Loading libraries'
  parser_libraries = map(__import__, LIBRARIES)

  for library in parser_libraries:
    name = 'lib{}'.format(library.__name__[2:])
    installed_version = int(library.get_version())
    available_version = CheckVersion(name)

    if installed_version != available_version:
      print '[{}] Version mismatch: installed {}, available: {}'.format(
          name, installed_version, available_version)
    else:
      print '[{}] OK'.format(name)

  latest_ole_version = GetOleIOVersion()
  installed_ole_version = float(OleFileIO_PL.__version__)
  if installed_ole_version != latest_ole_version:
    print '[{}] Version mismatch: installed {}, available: {}'.format(
        'OleFileIO_PL', installed_ole_version, latest_ole_version)
  else:
    print '[OleFileIO_PL] OK'

