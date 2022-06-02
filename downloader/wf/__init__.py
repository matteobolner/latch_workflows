"""
Downloader
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchDir, LatchFile
from typing import Optional

import functools
import pathlib
import shutil
import requests
from tqdm.auto import tqdm


@small_task
def download_task(
    url: str,
    outname: Optional[str],
    outpath: Optional[LatchDir]
    ) -> LatchFile:
    r = requests.get(url, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
    file_size = int(r.headers.get('Content-Length', 0))
    block_size = 1024

    if outname:
        filename=outname
    else:
        filename = url.split('/')[-1]

    tempname = url.split('/')[-1]
    print(f"Started downloading {tempname} ...")

    path = pathlib.Path(f'/root/{filename}').expanduser().resolve()

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
    with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            shutil.copyfileobj(r_raw, f)
    if outpath:
        outfile=f"{outpath.remote_path}/{filename}"
    else:
        outfile=f"latch:///{filename}"
    print(f"{tempname} was successfully downloaded, moving to latch filesystem ...")
    return LatchFile(path, outfile)

    #t = tqdm(total=file_size, unit='iB', unit_scale=True)
    #with open(path, 'wb') as f:
    #    for data in r.iter_content(block_size):
    #        t.update(len(data))
    #        f.write(data)
    #t.close()

    #if file_size != 0 and t.n != file_size:
    #    print("Error! Something went wrong during download.")

    #if outpath:
    #    outfile=f"{outpath.remote_path}/{filename}"
    #else:
    #    outfile=f"latch:///{filename}"
    #print(f"{tempname} was successfully downloaded, moving to latch filesystem ...")
    return LatchFile(path, outfile)



@workflow
def Downloader(
    url: str,
    outname: Optional[str],
    outpath: Optional[LatchDir],
    )->LatchFile:

    """ Simple file downloader for the Latch Console which doesn't require locally downloading files. Code was built with inspiration from https://stackoverflow.com/a/63831344 and https://stackoverflow.com/a/37573701

    __metadata__:
        display_name: Downloader
        author:
            name: Matteo Bolner
            email: matteo.bolner2@unibo.it
            github : https://github.com/matteobolner
        repository: https://github.com/matteobolner/latch_workflows/tree/master/downloader
        license:
            id: GPLv3

    Args:
        url:
            Url of the file
            __metadata__:
            display_name: Url of the file

        outname:
            Name of the file
            __metadata__:
            display_name: Name of the file (default is the original filename)

        outpath:
            Directory where the file will be saved
            __metadata__:
            display_name: Directory where the file will be saved (default is "latch:///filename")

    """
    return(download_task(url=url, outname=outname, outpath=outpath))
