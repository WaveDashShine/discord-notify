### Installation:
- better to set up an virtual env first then run:
```commandline
pip install -r requirements.txt
```
Run with virtual environment in terminal
- if using pycharm then venv should be in repo root:
```
<path to repo>/venv/bin/python3 botclient.py
```

### .env file setup
- .env in root directory of repo
```
DISCORD_TOKEN=<bot api token>
DISCORD_CHANNEL_ID=<discord channel to post to>
```

### yaml file setup: manhwa_config.yaml

```yaml
asura:
  url: https://url-of-manhwa-website.com
  interval: 1 hour
  # punctuation marks may not be as expected '
  manhwa:
    - title 1
    - title 2
```

