#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Evan Gaustad
#
# This file is part of packer-triage.
#
# packer-triage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# packer-triage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with packer-triage.  If not, see <https://www.gnu.org/licenses/>.

from exiftool import ExifTool
from pprint import pprint

# http://smarnach.github.io/pyexiftool/#
# sudo apt install libimage-exiftool-perl

class Exif_Engine:
    def __init__(self):
        self.file_details = {}

    def analyze(self, file_path):
        with ExifTool() as et:
            metadata = et.get_metadata(file_path)

        result = {key:value for key, value in metadata.items() if key not in ['SourceFile', 'File:Directory']}
        self.file_details = result

        return result

    def summarize_results(self):
        return self.file_details


if __name__ == "__main__":
    exif_instance = Exif_Engine()
    pprint(exif_instance.analyze('/home/analyst/packed_exes/unpacked_exe/bitsadmin.exe'))
