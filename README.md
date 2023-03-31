# Evernote Sync

Sync all notes in **markdown** format between **local files** and evernote.

> NOTE: only supports yinxiang in China


## Usage

```
$ > evernote_sync --local_dir ~/your/local/markdown_dir --config config.json
```

config file:
```json
{
  "token": "YOUR_EVERNOTE_DEV_TOKEN",
  "noteStoreUrl": "YOUR_EVERNOTE_NOTE_STORE_URL",
  "sandbox": false,
  "china": true
}
```