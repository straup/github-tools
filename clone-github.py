#!/usr/bin/env python

import os
import os.path
import json
import urllib2
import commands
import optparse

def clone_github(user, clonedir):

    repos = "http://github.com/api/v2/json/repos/show/%s" % user

    rsp = urllib2.urlopen(repos)
    data = json.loads(rsp.read())

    os.chdir(clonedir)

    for r in data['repositories'] :

        rdir = os.path.join(clonedir, r['name'])

        if os.path.exists(rdir):
            os.chdir(rdir)

            cmd = "git pull origin master"
        else:
            os.chdir(clonedir)
            cmd = "git clone git://github.com/%s/%s.git" % (user, r['name'])

        # Aren't there python git libraries for doing this?

        (status, output) = commands.getstatusoutput(cmd)
        print "%s : %s" % (cmd, status)

if __name__ == '__main__' :

    parser = optparse.OptionParser()
    parser.add_option("-c", "--clonedir", dest="clonedir", help="The path where your Github account will be cloned")
    parser.add_option("-u", "--user", dest="user", help="Your Github username")

    (opts, args) = parser.parse_args()

    user = opts.user
    clonedir = opts.clonedir

    clone_github(user, clonedir)
