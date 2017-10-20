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


if __name__ == '__main__':
    print(md5sum(
        'D:\\ms_work\\items\\IOSPLUS-17933 Dynamic Limit unit tests are randomly failing due to timeout on the script execution\\Release_x64\\1log',
        limit=DEFAULT_LIMIT))
