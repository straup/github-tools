#!/usr/bin/env python

import os
import os.path
import json
import urllib2
import logging
import subprocess
import types
import requests

class gethub:
    
    def __init__(self):
        pass

    def clone_repo(self, repo, outdir):

        path = os.path.join(outdir, repo['name'])
        logging.info("clone %s to %s" % (repo['name'], path))
        
        if os.path.isdir(path):

            os.chdir(path)

            args = [
                "git",
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
            logging.debug(rsp)

    # to do: clone_organization

    def clone_user(self, token, outdir, skip=[]):

        next = "https://api.github.com/user/repos"

        while next:
            
            url = next
            logging.debug("fetch %s" % url)
            
            try:
                rsp = requests.get(url, auth=(token, ''), stream=True)
            except Exception, e:
                logging.error("Failed to retrieve %s, because %s" % (url, e))
                return False
                
            # Seriously... this is better than plain vanilla pagination?
                
            headers = rsp.headers
            link = headers.get('link', None)
            
            if not link:
                logging.error("Can't find 'link' header")
                return False
                
            rels = link.split(', ')
            links = {}

            for rel in rels:
                rel = rel.split('; ')
                links[rel[1]] = rel[0]
                
                next = links.get('rel="next"', None)

                if next:
                    next = next.replace("<", "")
                    next = next.replace(">", "")
                    logging.debug("next is %s" % next)

                break

            try:
                data = rsp.json()
            except Exception, e:
                logging.error("Failed to parse %s, because %s" % (url, e))
                return False
        
            for repo in data:

                name = repo.get('name', None)

                if not name:
                    continue
                
                if name in skip:
                    continue

                try:
                    self.clone_repo(repo, outdir)
                except Exception, e:
                    logging.error(e)


if __name__ == '__main__':

    import optparse
    parser = optparse.OptionParser()

    # sudo read from config file...

    parser.add_option('--token', dest='token', action='store', help='')
    parser.add_option('--outdir', dest='outdir', action='store', help='')
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="enable chatty logging; default is false", default=False)

    (opts, args) = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not os.path.isdir(opts.outdir):
        logging.error("%s is not a directory" % opts.outdir)
        sys.exit()

    gh = gethub()
    gh.clone_user(opts.token, opts.outdir, args)


