# github-tools

## clone-repos.py

A simple script to clone a user's or an organization's public and private repositories. Requires a [personal API token](https://github.com/blog/1509-personal-api-tokens).

### Cloning your own repositories

	$> clone-repos.py --token <personal-api-token> --outdir </path/to/github-clone> [ list of repos to skip ]

### Cloning an origanization's repositories

	$> clone-repos.py --token <personal-api-token> --organization <org> --outdir </path/to/github-clone> [ list of repos to skip ]

### See also

* https://github.com/blog/1509-personal-api-tokens
