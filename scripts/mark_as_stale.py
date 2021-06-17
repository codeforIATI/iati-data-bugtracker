from datetime import date, timedelta
from os import getenv

from github import Github

days_until_stale = 30
today = date.today()
stale_before = today - timedelta(days=days_until_stale)
exempt_labels = ['meta', 'evergreen']

g = Github(getenv('GITHUB_TOKEN'))
repo = g.get_repo(getenv('GITHUB_REPOSITORY'))

issues = repo.get_issues(sort='updated', direction='asc')
for issue in issues:
    issue_labels = [label.name for label in issue.labels]
    if any([label in issue_labels for label in exempt_labels]):
        continue
    if issue.updated_at.date() <= stale_before:
        # issue is stale
        issue.add_to_labels('awaiting update')
        update_message = """Hello! There has been no activity on this issue in the last 30 days. I wonder if it has now been resolved?

If you’re reading this, would you mind checking to see if the issue is still applicable?

* If it has been resolved, please add a message to that effect, and (if you’re able to) close it.
* If the problem still applies, please add a message to let us know. I’ll remove the "awaiting update" label, and will check in again next month.

Thank you!"""
        issue.create_comment(update_message)
    else:
        # because of the sort order, as soon as we see a more
        # recently updated issue, we can stop
        break
