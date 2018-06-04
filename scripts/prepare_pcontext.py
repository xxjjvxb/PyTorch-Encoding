"""Prepare PASCAL Context dataset"""
import os
import shutil
import argparse
import tarfile
from encoding.utils import download, mkdir

_TARGET_DIR = os.path.expanduser('~/.encoding/data')
PASD_URL="https://codalabuser.blob.core.windows.net/public/%s"

def parse_args():
    parser = argparse.ArgumentParser(
        description='Initialize PASCAL Context dataset.',
        epilog='Example: python prepare_pcontext.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--download-dir', default=None, help='dataset directory on disk')
    args = parser.parse_args()
    return args

def download_ade(path, overwrite=False):
    _AUG_DOWNLOAD_URLS = [
        ('http://host.robots.ox.ac.uk/pascal/VOC/voc2010/VOCtrainval_03-May-2010.tar', 'bf9985e9f2b064752bf6bd654d89f017c76c395a'),
        ('https://codalabuser.blob.core.windows.net/public/trainval_merged.json', '169325d9f7e9047537fedca7b04de4dddf10b881')]
    download_dir = os.path.join(path, 'downloads')
    mkdir(download_dir)
    for url, checksum in _AUG_DOWNLOAD_URLS:
        filename = download(url, path=download_dir, overwrite=overwrite, sha1_hash=checksum)
        # extract
        if os.path.splitext(filename)[1] == '.tar':
            with tarfile.open(filename) as tar:
                tar.extractall(path=path)
        else:
            shutil.move(filename, os.path.join(path, 'VOCdevkit/VOC2010/'+os.path.basename(filename)))

if __name__ == '__main__':
    args = parse_args()
    mkdir(os.path.expanduser('~/.encoding/data'))
    if args.download_dir is not None:
        if os.path.isdir(_TARGET_DIR):
            os.remove(_TARGET_DIR)
        # make symlink
        os.symlink(args.download_dir, _TARGET_DIR)
    else:
        download_ade(_TARGET_DIR, overwrite=False)
