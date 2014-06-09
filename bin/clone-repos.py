#!/usr/bin/env python

import os
import os.path
import json
import urllib
import logging
import subprocess

def clone_repo(repo, outdir):

    path = os.path.join(outdir, repo['name'])
    logging.info("clone %s to %s" % (repo['name'], path))

    if os.path.isdir(path):
        os.chdir(path)

        args = [
            "git"
            "pull",
            "origin",
            "master"
            ]

    else:

        args = [
            "git",
            "clone",
            repo['git_url'],
            path
            ]

    rsp = subprocess.check_call(args)
    print rsp

def clone_list(user, outdir, skip=[]):

    # because, stupid... so insanely stupid
    # https://developer.github.com/v3/#pagination

    next = "https://api.github.com/users/%s/repos" % user

    while next:

        logging.debug("fetch %s" % next)

        try:
            rsp = urllib.urlopen(next)
        except Exception, e:
            logging.error("Failed to retrieve %s, because %s" % (next, e))
            return False

        for k, v in rsp.info().items():

            if k == 'link':

                links = {}
                rels = v.split(', ')
                
                for rel in rels:
                    rel = rel.split('; ')
                    links[rel[1]] = rel[0]
                    
                    next = links.get('rel="next"', None)
                    logging.debug("next is %s" % next)
                    break

                break

        try:
            data = json.load(rsp)
        except Exception, e:
            logging.error("Failed to parse %s, because %s" % (next, e))
            return False
        
        for repo in data:

            if repo['name'] in skip:
                continue

            clone_repo(repo, outdir)


if __name__ == '__main__':

    import sys
    user = sys.argv[1]
    outdir = sys.argv[2]
    skip = sys.argv[3:]

    clone_list(user, outdir, skip)


