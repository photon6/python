# python

Python scripts and apps

**When using classes/config_loader.py:**

# JSON

loader = ConfigLoader("config.json")
print(loader["database"])

# YAML

loader = ConfigLoader("config.yaml")
print(loader.get("database", {}))
