import sys
import re
from os import getenv

from github import Github
from github.GithubException import UnknownObjectException

issue_number = int(sys.argv[1])

g = Github(getenv('GITHUB_TOKEN'))
repo = g.get_repo(getenv('GITHUB_REPOSITORY'))

issue = repo.get_issue(issue_number)
lines = re.split(r'[\n\r]+', issue.body)
for idx, line in enumerate(lines):
    if line == '### IATI registry identifier for the publisher':
        label = 'publisher: ' + lines[idx + 1]
        try:
            repo.get_label(label)
        except UnknownObjectException:
            print(f'Failed to add label "{label}" to issue {issue.number}')
            # Give up
            break
        print(f'Adding label "{label}" to issue {issue.number}')
        issue.add_to_labels(label)
        # we're done
        break
