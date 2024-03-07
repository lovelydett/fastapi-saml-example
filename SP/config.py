import json

deploy_config: dict = {}

with open("config/deploy_config.json", "r") as f:
    deploy_config = json.load(f)

with open("config/sso_settings.json", "r") as f:
    sso_settings = json.load(f)
    deploy_config["sso_settings"] = sso_settings
