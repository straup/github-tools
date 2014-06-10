# github-tools

## clone-repos.py

A 5-minute script to clone/pull all a user's (public) repos (in read-only mode) to a local directory. Needs auth-y hooks for private repositories. This is basically just a safe guard and has no bells. Or whistles.

	$> clone-repos.py --token <personal-api-token> --outdir </path/to/github-clone> [ list of repos to skip ]

### See also

* https://github.com/blog/1509-personal-api-tokens
