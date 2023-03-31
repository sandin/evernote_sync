import argparse
import os
import json
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore

from evernote_sync.evernote_client import get_note_store, find_all_notes_in_notebook


def parse_config_file(filename):
    default_config = {
        "token": "",
        "noteStoreUrl": "",
        "sanbox": False,
        "china": False
    }
    if not os.path.exists(filename):
        print("Error: config file is not exists")
        return None
    with open(filename, "r") as f:
        try:
            config = json.load(f)
            if "token" in config and "noteStoreUrl" in config:
                return {**default_config, **config}
        except json.JSONDecodeError as e:
            print("Error: bad config file", e)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config file", required=True)
    args = parser.parse_args()

    configs = parse_config_file(args.config)
    if configs is None:
        return

    client = EvernoteClient(token=configs["token"], sandbox=configs["sandbox"], china=configs["china"])

    note_store = get_note_store(client, configs["noteStoreUrl"])  # type: NoteStore.Client
    notebooks = note_store.listNotebooks(client.token)
    print("Found %d notebooks" % len(notebooks))
    for notebook in notebooks:
        print("* ", notebook.name)
        notes = find_all_notes_in_notebook(client, note_store, notebook)
        for note in notes:
            print("  ** ", note.title)

