#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
import os
import os.path
import sys

if len(sys.argv) != 3:
    print "Usage: ./json2git.py law.json path/to/git/repo"
    sys.exit(-1)

law = json.load(file(sys.argv[1]))

paths = os.path.dirname(sys.argv[1]).split('/')
cat = paths[-2]
output = '%s/%s.md' % (cat, paths[-1])
print 'Generating', output

os.chdir(sys.argv[2])
if not os.path.exists(cat):
    os.makedirs(cat)
#os.system('git init')


content = None
for rev in law['revision']:
    if content is None:
        content = rev['content']
    else:
        for index, obj in rev['content'].iteritems():
            content[index] = obj

    with codecs.open(output, 'w', 'utf-8') as out:
        keylist = content.keys()
        keylist.sort(key=float)
        for index in keylist:
            print >>out, u"* %s %s\n" % (content[index]['num'], content[index]['article'])
            if 'reason' in content[index]:
                print >>out, u"> 釋：%s\n" % (content[index]['reason'])

    os.system('git add %s' % output)

    date = rev['date']
    if int(date[:date.index('.')]) < 1970:
        date = '1970.1.1'
    os.system('git commit --date "%sT23:00:00" -m "%s %s"' % (date.encode('utf-8'), output[:-3], rev['date'].encode('utf-8')))