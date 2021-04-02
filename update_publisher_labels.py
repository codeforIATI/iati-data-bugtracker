from os import getenv

import requests
from github import Github


pub_label_prefix = 'publisher: '
pub_labels = []
j = requests.get("https://iatiregistry.org/publisher/download/json").json()
for x in j:
    desc = "Issue relates to " + x["Publisher"]
    if len(desc) > 100:
        desc = desc[:97] + "[…]"
    publisher_id = x["Datasets Link"].rsplit("/", 1)[-1]
    name = pub_label_prefix + publisher_id
    pub_labels.append({"name": name, "description": desc, "color": "ededed"})

pub_labels = {label["name"]: label for label in pub_labels}

g = Github(getenv('GITHUB_TOKEN'))
repo = g.get_repo('codeforiati/iati-data-bugtracker')
repo_labels = list(repo.get_labels())
for repo_label in repo_labels:
    if not repo_label.name.startswith(pub_label_prefix):
        continue
    current_label = pub_labels.get(repo_label.name)
    if not current_label:
        # # NB: We don’t actually remove the publisher here.
        # # That’s because more often than not, the publisher
        # # has disappeared due to some other problem.
        #
        # repo_label.delete()
        #
        # # Instead, we just make a note.
        print('Publisher has gone: "{}"'.format(repo_label.name))
        continue
    new_description = current_label.get('description', repo_label.description)
    new_color = current_label.get('color', repo_label.color)
    if new_description != repo_label.description or \
            new_color != repo_label.color:
        print('Updating label: "{}"'.format(repo_label.name))
        repo_label.edit(repo_label.name, new_color, new_description)

repo_label_names = [x.name for x in repo_labels]
for label_name, label_dict in pub_labels.items():
    if label_name not in repo_label_names:
        print('Creating label: {}'.format(label_name))
        repo.create_label(**label_dict)
