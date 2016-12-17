#!/usr/bin/python

"""
USAGE:
    $ pyhton csv-to-md.py new-sigs.csv _signatures
"""

import sys
import unidecode
import re
import os
import json

def nearest_ascii(ustring):
    """ Given an encoded string that may contain UTF-8 or Latin-1 high
    bytes, try to convert it completely ASCII. This is suitable for
    filenames and author lists. """
    if not isinstance(ustring,unicode):
        try:
            ustring = ustring.decode('utf-8')
        except:
            try:
                ustring = ustring.decode("iso-8859-1")
            except:
                raise ValueError(ustring)
    # return unicodedata.normalize('NFKD', ustring).encode('ascii','ignore')
    return unidecode.unidecode(ustring)

def sanitize_for_filename(string):
    string = nearest_ascii(string)
    string = string.replace(" ", "_")
    string = re.compile(r"[^-a-zA-Z_0-9]").subn("",string)[0]
    string = string.lower()
    return string

if __name__ == "__main__":
    csv_filename = sys.argv[1]
    output_folder = sys.argv[2]

    for line in open(csv_filename):
        assert '<' not in line
        assert '>' not in line
        assert '"' not in line
        assert '\\' not in line
        line = line.decode("utf-8")
        name, title, affiliation, link = line.strip().split(";")
        output_filename = os.path.join(output_folder, sanitize_for_filename(name) + ".md")
        print "Output", output_filename

        template = ["---"]
        template.append("  name: \"%s\"" % name)
        if link:
            template.append("  link: \"%s\"" % link)
        if title:
            template.append("  title: \"%s\"" % title)
        if affiliation:
            template.append("  affiliation: \"%s\"" % affiliation)
        template.append("---")

        with open(output_filename, "w") as f:
            f.write("\n".join(template).encode('utf-8'))
