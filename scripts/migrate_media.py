import os
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otaku.settings')

import django


def main():
    django.setup()

    from django.conf import settings
    from django.core.files import File
    from django.core.files.storage import default_storage

    if not settings.AWS_STORAGE_BUCKET_NAME:
        raise RuntimeError('Configure AWS_STORAGE_BUCKET_NAME before migrating media.')

    media_root = Path(settings.MEDIA_ROOT)
    if not media_root.is_dir():
        raise FileNotFoundError(f'Media directory does not exist: {media_root}')

    uploaded = 0
    skipped = 0

    for source_path in media_root.rglob('*'):
        if not source_path.is_file():
            continue

        storage_name = source_path.relative_to(media_root).as_posix()
        if default_storage.exists(storage_name):
            skipped += 1
            continue

        with source_path.open('rb') as source_file:
            default_storage.save(storage_name, File(source_file, name=storage_name))
        uploaded += 1

    print(f'Media migration complete: {uploaded} uploaded, {skipped} already present.')


if __name__ == '__main__':
    main()
