# github-tools

## clone-repos.py

A simple script to clone a user's or an organization's public and private repositories. Requires a [personal API token](https://github.com/blog/1509-personal-api-tokens).

### Cloning your own repositories

	$> clone-repos.py --token <personal-api-token> --outdir </path/to/github-clone> [ list of repos to skip ]

### Cloning an origanization's repositories

	$> clone-repos.py --token <personal-api-token> --organization <org> --outdir </path/to/github-clone> [ list of repos to skip ]

### Using a config file

You can also use a standard .ini file for specifying your personal API token

	$> clone-repos.py --config </path/to/config> --outdir </path/to/github-clone> [ list of repos to skip ]

The config file should contain a `github.token` entry, for example:

	[github]
	token=s00pers33kret
    
### See also

* https://github.com/blog/1509-personal-api-tokens
