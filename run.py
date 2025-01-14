import argparse
from IPython.terminal.embed import InteractiveShellEmbed

from buffer import buffer
import yaml

PARSER = argparse.ArgumentParser(description='Send tweets to buffer')
PARSER.add_argument('--image-path', help="Path where relative images can be found")
PARSER.add_argument('--config', help="Path where config is kept")
args = PARSER.parse_args()

if args.config:
    with open(args.config, "utf-8") as f:
        config = yaml.safe_load(f)
else:
    config = {}

config = dict(config, **dict(args._get_kwargs())) #pylint: disable=protected-access

b = buffer.Buffer(image_path=config["image_path"])
b.login()
ipshell = InteractiveShellEmbed()
ipshell(b=b)
