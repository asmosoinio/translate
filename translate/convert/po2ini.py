#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2002-2006 Zuza Software Foundation
# 
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with translate; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


"""script that converts a .po file with translations based on a .pot file
generated from a Mozilla localization .ini back to the .ini (but translated)
Uses the original .ini to do the conversion as this makes sure we don't
leave out any unexpected stuff..."""

from translate.misc import quote
from translate.storage import factory
from translate.storage import ini

class reini:
  def __init__(self, templatefile):
    self.templatefile = templatefile
    self.templatestore = ini.inifile(templatefile)
    self.inputdict = {}

  def convertfile(self, inputstore, includefuzzy=False):
    self.makestoredict(inputstore, includefuzzy)
    for unit in self.templatestore.units:
      for location in unit.getlocations():
        unit.target = self.inputdict[location]
    return str(self.templatestore)

  def makestoredict(self, store, includefuzzy=False):
    # make a dictionary of the translations
    for unit in store.units:
      if includefuzzy or not unit.isfuzzy():
        # there may be more than one entity due to msguniq merge
        for location in unit.getlocations():
          inistring = unit.target
          if len(inistring.strip()) == 0:
            inistring = unit.source
          self.inputdict[location] = inistring

def convertini(inputfile, outputfile, templatefile, includefuzzy=False):
  inputstore = factory.getobject(inputfile)
  if templatefile is None:
    raise ValueError("must have template file for ini files")
  else:
    convertor = reini(templatefile)
  outputstring = convertor.convertfile(inputstore, includefuzzy)
  outputfile.write(outputstring)
  return 1

def main(argv=None):
  # handle command line options
  from translate.convert import convert
  formats = {("po", "ini"): ("ini", convertini)}
  parser = convert.ConvertOptionParser(formats, usetemplates=True, description=__doc__)
  parser.add_fuzzy_option()
  parser.run(argv)

if __name__ == '__main__':
  main()

