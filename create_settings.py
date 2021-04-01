import requests
import yaml


labels = [{
        "name": "awaiting update",
        "color": "#2BE1C4",
        "description": "Waiting for someone to check and confirm the issue is still relevant",
    }, {
        "name": "meta",
        "color": "#0847F0",
        "description": "Issue with this issue tracker",
    }, {
        "name": "metadata issue",
        "color": "#785D1F",
        "description": "Issue with a publisher’s metadata on the IATI registry",
    }, {
        "name": "data issue",
        "color": "#D73A4A",
        "description": "Issue with a publisher’s IATI data",
    }
]
j = requests.get("https://iatiregistry.org/publisher/download/json").json()
for x in j:
    desc = "Issue with data from " + x["Publisher"]
    if len(desc) > 100:
        desc = desc[:97] + "[…]"
    name = "publisher: " + x["Datasets Link"].rsplit("/", 1)[-1]
    labels.append({"name": name, "description": desc})
labels = {"labels": labels}
with open(".github/settings.yml", "w") as f:
    yaml.dump(labels, f)
