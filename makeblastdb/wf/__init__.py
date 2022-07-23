"""
makeblastdb
"""

import subprocess
from enum import Enum
from pathlib import Path
from typing import List, Union
from latch import large_task, medium_task, small_task, workflow
from latch.types import LatchDir, LatchFile
from typing import Optional
import os



@small_task
def makeblastdb_task(
    dbtype: str = 'nucl',
    input_type: Optional[str] = None,
    title : Optional[str]= None,
    output_name: Optional[str] = None,
    parse_seqids : bool = True,
    hash_index : bool = False,
    mask_data : Optional[List[LatchFile]] = None,
    mask_id : Optional[List[str]] = None,
    mask_desc: Optional[List[str]] = None,
    gi_mask: bool = True,
    taxid = Optional[str] = None,
    input_fasta: List[LatchFile],
    output_dir: LatchDir,
    gi_mask_name: Optional[str],
    taxid_map = Optional[LatchFile]

) -> LatchDir:

    local_output="/root/blast_db"
    remote_dir = f"latch:///{output_dir}/"

    name = output_name
    if not name and len(input_fasta)==1:
        name = os.path.splitext(input_fasta.remote_path)[0].split("/")[-1]
    else:
        name = 'blast_db'

    mask_data_list = ''
    if mask_data:
        for i in maskdata:
            mask_data_list+=f"{i.local_path},"


    _params = locals()
    _flags = {
        "input_type" : lambda x: ["-input_type", str(x)] if x is not None else [],
        "title" : lambda x: ["-title", str(x)] if x is not None else [],
        "output_name" : lambda x: ["-input_type", str(x)] if x is not None else [],
        "parse_seqids" : lambda x: ["-parse_seqids", str(x)] if x is not False else [],
        "hash_index" : lambda x: ["-hash_index", str(x)] if x is not False else [],
        "mask_data" : lambda x: ["-mask_data", mask_data_list] if x is not None else [],
        "mask_id" : lambda x: ["-mask_id", ",".join(x)] if x is not None else [],
        "mask_desc" : lambda x: ["-mask_desc", ",".join(mask_desc)] if x is not None else [],
        "gi_mask" : lambda x: ["-gi_mask", str(x)] if x is not False else [],
        "gi_mask_name" : lambda x: ["-gi_mask_name", str(x)] if x is not None else [],
        "taxid" : lambda x: ["-taxid", str(x)] if x is not None else [],
        "taxid_map" : lambda x: ["-taxid_map", str(x.local_path)] if x is not None else []
        }


    flags = []

    for k, v in _params.items():
        print(k,v)
        if k not in ("dbtype","in", "out"):
            flags.extend(_flags[k](v))

    local_paths = " ".join([i.local_path for i in input_fasta.split(",")])
    _makeblastdb_cmd = [
        f"cat {local_paths}",
        "|",
        "makeblastdb",
        f"-dbtype {dbtype}",
        f"-out {output_dir.local_path}/{name}",
        *flags
    ]

    subprocess.run(_makeblastdb_cmd)

    return LatchDir(local_output, remote_dir)

@workflow
def makeblastdb_wf(
    dbtype: str = 'nucl',
    input_fasta: LatchFile,
    output_dir: LatchDir,
    input_type: Optional[str] = None,
    title : Optional[str]= None,
    output_name: Optional[str] = None,
    parse_seqids : bool = True,
    hash_index : bool = False,
    mask_data : Optional[List[LatchFile]] = None,
    mask_id : Optional[List[str]] = None,
    mask_desc: Optional[List[str]] = None,
    gi_mask: bool = True,
    gi_mask_name: Optional[str],
    taxid = Optional[str] = None,
    taxid_map = Optional[LatchFile]
    ) -> LatchDir:

    """
    makeblastdb
    The makeblastdb application produces BLAST databases from FASTA files. It is possible to use completely unstructured (or even blank) FASTA definition lines, but this is not the recommended procedure. Assigning a unique identifier to every sequence in the database allows you to retrieve the sequence by identifier and allows you to associate every sequence with a taxonomic node (through the taxid of the sequence). The unique identifier can be a simple string or could be actual accession of the sequence if the sequence comes from a public database (e.g., GenBank). Being able to associate a database sequence with a taxonomic node is especially powerful for the version 5 databases that BLAST can use to limit the search by taxonomy. The identifier should begin right after the “>” sign on the definition line and contain no spaces and the -parse_seqids flag should be used. In general, you should not use a “|” (bar) in your identifier. The “|” (bar) is a reserved character for the NCBI FASTA ID parser and makeblastdb will return an error unless the bar is used in a specific manner described at https://ncbi.github.io/cxx-toolkit/pages/ch_demo#ch_demo.T5
    __metadata__:
        display_name: makeblastdb
        author:
            name:
            email:
            github: https://www.ncbi.nlm.nih.gov/books/NBK279690/
        repository:

    Args:
        dbtype:
            __metadata__:
            display_name: Molecule type of target db (nuclear or protein sequence)
                appearance:
                    multiselect:
                        options:
                            - nucl
                            - prot
                        allow_custom: false
        input_fasta:
          __metadata__:
            display_name: Input file

        output_dir:
            __metadata__:
                display_name: Directory in which the database will be generated

        input_type:
            __metadata__:
                display_name: Type of the input data specified (default is fasta)
                appearance:
                    multiselect:
                        options:
                            - fasta
                            - asn1_bin
                            - asn1_txt
                            - blastdb
                        allow_custom: True
        title:
            The default title is the name of the input file provided
            __metadata__:
                display_name: Title for BLAST database

        output_name
            The default filename is the name of the file provided as input
            __metadata__:
                display_name: Filename of BLAST database to be created

        parse_seqids:
            Option to parse seqid for FASTA input if set, for all other input types seqids are parsed automatically
            __metadata__:
                display_name: Parse seqid

        hash_index:
            Create index of sequence hash values
            __metadata__:
                display_name: Hash index

        mask_data:
            List of input files containing masking data as produced by NCBI masking applications (e.g. dustmasker, segmasker, windowmasker)
            __metadata__:
                display_name: File(s) containing masking data

        mask_id:
            List of strings to uniquely identify the masking algorithm
            Requires:  mask_data
            Incompatible with:  gi_mask
            __metadata__:
                display_name: Masking algorithm id

        mask_desc:
            List of free form strings to describe the masking algorithm details. Requires:  mask_id
            __metadata__:
                display_name: Masking algorithm details
        gi_mask:
            Requires:  parse_seqids
            Incompatible with:  mask_id
            __metadata__:
                display_name: Create GI indexed masking data
        gi_mask_name:
            Requires:  mask_data, gi_mask
            __metadata__:
                display_name: Masking data output files
        taxid:
            Incompatible with Taxonomy ID file
            __metadata__:
                display_name: Taxonomy ID
        taxid_map:
            Text file mapping sequence IDs to taxonomy IDs (Incompatible with taxid)
            Requires parse_seqids
            __metadata__:
                display_name: Taxonomy ID file
    """

    return(makeblastdb_task(
    dbtype=dbtype,input_fasta=input_fasta,output_dir=output_dir,input_type=input_type,
    title=title,output_name=output_name,parse_seqids=parse_seqids,hash_index=hash_index,
    mask_data=mask_data,mask_id=mask_id,mask_desc=mask_desc,gi_mask=gi_mask,gi_mask_name=gi_mask_name
    taxid=taxid,taxid_map=taxid_map)
