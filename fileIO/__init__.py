
from .filestorage import FileStorage

storage = FileStorage()

if not storage.objects:
    storage.reload()
