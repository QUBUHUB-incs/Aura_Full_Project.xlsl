import requests

# Heartbeat URL
url = "https://ping.checklyhq.com/8171862b-7c9e-461f-92c3-87a515ae5971"

# A GET request to the Heartbeat
response = requests.get(url, timeout=5)
