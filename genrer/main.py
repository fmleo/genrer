import argparse
import pathlib
from genrer.client import Client

parser = argparse.ArgumentParser(
    prog="genrer", description="Update the genres of your tracks powered by last.fm"
)

parser.add_argument("work_dir", type=pathlib.Path)
parser.add_argument("--api_key")
parser.add_argument("--debug_level")

client = Client(**parser.parse_args().__dict__)
