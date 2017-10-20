import os
from hashlib import md5

DEFAULT_LIMIT = 5 * 1024 * 1024


def md5sum(file_name, limit=None):
    hash_md5 = md5()
    with open(file_name, 'rb') as f:
        if limit:
            hash_md5.update(f.read(limit))
        else:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
    return hash_md5.hexdigest()


class CollisionError(Exception):
    pass


def dedup(dir):
    hash_dict = {}
    duplications = {}
    for subdir, _, files in os.walk(dir):
        for file in files:
            full_name = os.path.join(subdir, file)
            short_md5 = md5sum(full_name, limit=DEFAULT_LIMIT)
            if short_md5 in hash_dict:
                original_full_md5 = md5sum(hash_dict[short_md5], limit=None)
                full_md5 = md5sum(full_name)
                if original_full_md5 != full_md5:
                    raise CollisionError('{} and {} has same short md5'
                                         .format(hash_dict[full_md5], full_name))
                if short_md5 in duplications:
                    duplications[short_md5].append(full_name)
                else:
                    duplications[short_md5] = [hash_dict[short_md5], full_name]
            else:
                hash_dict[short_md5] = full_name

    for _, value in duplications.items():
        print(value)
        print('\n')


if __name__ == '__main__':
    dedup('D:\\ms_tmp\\rc_retail')
