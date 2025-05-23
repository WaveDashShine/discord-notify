### Installation:
- better to set up an virtual env first then run:
```commandline
pip install -r requirements.txt
```
Run with virtual environment in terminal
- if using pycharm then venv should be in repo root:
```
<path to repo>/venv/bin/python discord_notifier.py
```

### tests

```
<path to repo>/venv/bin/pytest tests/
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
  interval: 45 min
  # punctuation marks may not be as expected '
  manhwa:
    - title 1
    - title 2
```

### debug

- see debug log under `debug/debug.log`
- `manhwa_checker/main.py` is runnable separately and uses headed chromium playwright by default