#External modules
import hashlib

def get_file_md5(fname, show_prints):
    #Reference: https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    hash_value = hash_md5.hexdigest()
    if show_prints:
        print(f'Hash value generated. Hash {hash_value}')
    return hash_value
