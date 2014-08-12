#!/usr/bin/env python

import sys
import pprint
import os
import os.path
import json
import urllib2
import logging
import subprocess
import types
import requests

class gethub:
    
    def __init__(self, token, **kwargs):
        self.token = token
        self.exclude = kwargs.get('exclude', [])

    def clone_repo(self, repo, outdir):

        path = os.path.join(outdir, repo['name'])
        logging.info("clone %s to %s" % (repo['name'], path))

        ssh_url = repo['ssh_url']

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
                ssh_url,
                path
            ]
        
        logging.info(" ".join(args))
        rsp = subprocess.check_call(args)

    def clone_user(self, outdir):

        src = "https://api.github.com/user/repos"
        return self.clone_source(src, outdir)

    def clone_organization(self, org, outdir):

        src = "https://api.github.com/orgs/%s/repos" % org
        return self.clone_source(src, outdir)

    def clone_source(self, src, outdir):

        while src:
            
            url = src
            logging.debug("fetch %s" % url)

            try:
                rsp = requests.get(url, auth=(self.token, ''), stream=True)
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

                src = next
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
                
                if name in self.exclude:
                    continue

                try:
                    self.clone_repo(repo, outdir)
                except Exception, e:
                    logging.error(e)
                    
if __name__ == '__main__':

    import optparse
    import ConfigParser

    parser = optparse.OptionParser()

    # sudo read from config file...

    parser.add_option('--token', dest='token', action='store', help='')
    parser.add_option('--config', dest='config', action='store', help='')
    parser.add_option('--outdir', dest='outdir', action='store', help='')
    parser.add_option('--organization', dest='organization', action='store', help='')
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="enable chatty logging; default is false", default=False)

    (opts, to_skip) = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not os.path.isdir(opts.outdir):
        logging.error("%s is not a directory" % opts.outdir)
        sys.exit()

    token = opts.token

    if opts.config:

        if not os.path.exists(opts.config):
            logging.error("%s does not exist" % opts.config)
            sys.exit()

        cfg = ConfigParser.ConfigParser()
        cfg.read(opts.config)
        token = cfg.get('github', 'token')

    gh = gethub(token, exclude=to_skip)

    if opts.organization:
        gh.clone_organization(opts.organization, opts.outdir)
    else:
        gh.clone_user(opts.outdir)

    sys.exit()
