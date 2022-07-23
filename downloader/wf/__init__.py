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
import csv

@small_task
def download_single_file(
    url: str,
    outname: Optional[str],
    outpath: Optional[LatchDir],
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
    #return LatchFile(path, outfile)

@small_task
def download_multiple(
    url: str,
    outname: Optional[str],
    outpath: Optional[LatchDir],
    ) -> LatchDir:

    if url:
        urls = [line.rstrip() for line in url.split(",")]
    else:
        print("ERROR: No urls specified")

    if outname:
        outnames = [line.rstrip() for line in outname.split(",")]
    else:
        outnames = [line.split('/')[-1] for line in urls]
    #elif url_file:
    #    urls=[]
    #    with open(url_file.local_path, 'r') as f:
    #        urls = [line.rstrip() for line in f]


    for url, name in zip(urls, outnames):
        r = requests.get(url, stream=True, allow_redirects=True)
        if r.status_code != 200:
            r.raise_for_status()
            raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
        file_size = int(r.headers.get('Content-Length', 0))
        block_size = 1024
        local_dir = '/root/multiple_files/'
        print(f"Started downloading {name} ...")
        path = pathlib.Path(f'{local_dir}/{name}').expanduser().resolve()
        desc = "(Unknown total file size)" if file_size == 0 else ""
        r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
        with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as f:
                shutil.copyfileobj(r_raw, f)
        print(f"{name} was successfully downloaded, moving to latch filesystem ...")
    return LatchDir(local_dir, outpath.remote_path)

@workflow
def Downloader(
    url: str,
    outpath: LatchDir,
    outname: Optional[str],
    )->LatchDir:

    """ Simple file downloader for the Latch Console which doesn't require locally downloading files. Code was built with inspiration from https://stackoverflow.com/a/63831344 and https://stackoverflow.com/a/37573701

    ## Downloader

    This workflow allows to download files directly inside the Latch console, bypassing the need to upload data from local sources.

    ## Input format:
    Input can be a single url or multiple comma-separated urls; the same goes for the filenames (optional).

    ----

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
            URL of the file, or alternatively multiple comma-separated URLs
            __metadata__:
            display_name: URL of the file, or alternatively multiple comma-separated URLs

        outname:
            Name of the downloaded file(s) (if multiple filenames, separate them with comma)
            __metadata__:
            display_name: Name of the file(s) (default is the original filenames)

        outpath:
            Directory where the file(s) will be saved
            __metadata__:
            display_name: Directory where the file(s) will be saved
    """
    return(download_multiple(url=url, outname=outname, outpath=outpath))
