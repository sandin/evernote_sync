from typing import Union, Optional, Any

from evernote.edam.notestore import NoteStore
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.userstore import UserStore
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient

# source: https://dev.evernote.com/doc/reference/Limits.html
EDAM_RELATED_MAX_NOTES = 25


def get_note_store(client, note_store_url, network_error_retry_count=3):
    if client.china:
        user_agent = "YXScript Windows/603139;"
    else:
        user_agent = "ENScript Windows/309091;"

    return Store(
        client_class=NoteStore.Client,
        store_url=note_store_url,
        token=client.token,
        user_agent=user_agent,
        network_error_retry_count=network_error_retry_count,
    )


def find_all_notes_in_notebook(client, note_store, notebook):
    notes = []
    offset = 0
    total_notes = offset + 1
    while offset < total_notes:
        #print("findNotes, notebook.guid=%s, offset=%d, maxNotes=%d" % (notebook.guid, offset, EDAM_RELATED_MAX_NOTES))
        note_list = note_store.findNotes(client.token, filter=NoteFilter(notebookGuid=notebook.guid), offset=offset, maxNotes=EDAM_RELATED_MAX_NOTES)
        total_notes = note_list.totalNotes
        offset += len(note_list.notes)
        notes += note_list.notes
    return notes


# source: https://github.com/vzhd1701/evernote-backup/blob/master/evernote_backup/evernote_client.py
class Store(object):
    def __init__(
        self,
        client_class: Union[UserStore.Client, NoteStore.Client],
        store_url: str,
        user_agent: str,
        network_error_retry_count: int,
        token: Optional[str] = None,
    ):
        self.token = token
        self.user_agent = user_agent
        self.network_error_retry_count = network_error_retry_count

        self._client = self._get_thrift_client(client_class, store_url)

    def __getattr__(self, name: str) -> Any:
        target_method = getattr(self._client, name)

        if not callable(target_method):
            return target_method
        return target_method

    def _get_thrift_client(
        self,
        client_class: Union[UserStore.Client, NoteStore.Client],
        url: str,
    ) -> Union[UserStore.Client, NoteStore.Client]:
        http_client = THttpClient.THttpClient(url)
        http_client.setCustomHeaders(
            {
                "User-Agent": self.user_agent,
                "x-feature-version": 3,
                "accept": "application/x-thrift",
                "cache-control": "no-cache",
            }
        )

        thrift_protocol = TBinaryProtocol.TBinaryProtocol(http_client)
        return client_class(thrift_protocol)