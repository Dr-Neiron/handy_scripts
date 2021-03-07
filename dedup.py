import os
import pickle
import shutil
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


# def create_hash(directory):
#     hash_dict = dict()
#     duplications = dict()
#     for subdir, _, files in os.walk(directory):
#         for file in files:
#             full_name = os.path.join(subdir, file)
#             short_md5 = md5sum(full_name, limit=DEFAULT_LIMIT)
#             if short_md5 in hash_dict:
#                 original_full_md5 = md5sum(hash_dict[short_md5], limit=None)
#                 full_md5 = md5sum(full_name)
#                 if original_full_md5 != full_md5:
#                     raise CollisionError('{} and {} has same short md5'
#                                          .format(hash_dict[full_md5], full_name))
#                 if short_md5 in duplications:
#                     duplications[short_md5].append(full_name)
#                 else:
#                     duplications[short_md5] = [hash_dict[short_md5], full_name]

def find_unique(directory):
    with open('all_photo.pkl', 'rb') as f:
        photo_dict = pickle.load(f)
    with open('all_video.pkl', 'rb') as f:
        video_dict = pickle.load(f)

    print(len(photo_dict))
    print(len(video_dict))

    rev_photo = dict()
    rev_video = dict()

    for hash, filename in photo_dict.items():
        rev_photo[os.path.basename(filename)] = hash
    for hash, filename in video_dict.items():
        rev_video[os.path.basename(filename)] = hash

    for subdir, _, files in os.walk(directory):
        for filename in files:
            full_name = os.path.join(subdir, filename)
            short_md5 = md5sum(full_name, limit=DEFAULT_LIMIT)
            if (short_md5 not in photo_dict) and (short_md5 not in video_dict):
                if (filename not in rev_photo) and (filename not in rev_video):
                    shutil.copyfile(full_name, os.path.join('F:\\tmp2\\unique', filename))
                    print(full_name + ' !! no such name')
                else:
                    shutil.copyfile(full_name, os.path.join('F:\\tmp2\\hash', filename))
                    print(full_name + ' name exist, but hash is unique')



def dedup(dir):
    hash_dict = dict()
    duplications = dict()
    dir_duplications = list()
    for subdir, _, files in os.walk(dir):
        is_duplicating_dir = True
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
                is_duplicating_dir = False
        if is_duplicating_dir:
            dir_duplications.append(subdir)

    with open('all_photo.pkl', 'wb') as p:
        pickle.dump(hash_dict, p)
    for d in dir_duplications:
        print(d)
    print('------')
    for _, value in duplications.items():
        print(value)
        print('\n')


if __name__ == '__main__':
    # dedup('F:\\all_photo')
    find_unique('F:\\tmp')
    print('Done.')
