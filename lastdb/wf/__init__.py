"""
LASTDB
"""

import subprocess
from pathlib import Path

from latch import medium_task, workflow
from latch.types import LatchDir, LatchFile
from typing import Optional, List, Union

@medium_task
def lastdb(
    input_file : LatchFile,
    db_name : str,
    output_dir : LatchDir,
    proteinseq : bool = False,
    softmask_lc: bool = False,
    seed_scheme: Union[None, str] = None,
    lowercase: Union[None, str] = None,
    size: Union[None, str] = None,
    strand: Union[None, str] = None,
    sequence_file_type: Union[None, str] = None,
    proteinseq_with_end: Union[None, str] = None,
    spaced_seed_pattern: Union[None, str] = None,
    dna_seed_pattern: Union[None, str] = None,
    alphabet: Union[None, str] = None
    ) -> LatchDir:

    local_dir = "/root/lastdb_folder"
    remote_dir = output_dir.remote_path
    final_output= f"{local_dir}/{db_name}"

    _params = locals()
    _flags = {
        "proteinseq": lambda x: ["-p"] if x is True else [],
        "softmask_lc": lambda x: ["-c"] if x is True else [],
        "seed_scheme": lambda x: ["-u", str(x)] if x is not None else [],
        "lowercase": lambda x: [f"-R{str(x)}"] if x is not None else [],
        "size": lambda x: ["-W", str(x)] if x is not None else [],
        "strand": lambda x: ["-S", str(x)] if x is not None else [],
        "sequence_file_type": lambda x: ["-Q", str(x)] if x is not None else [],
        "proteinseq_with_end": lambda x: ["-q", str(x)] if x is not None else [],
        "spaced_seed_pattern": lambda x: ["-m", str(x)] if x is not None else [],
        "dna_seed_pattern": lambda x: ["-d", str(x)] if x is not None else [],
        "alphabet": lambda x: ["-a", str(x)] if x is not None else []
        }


    flags = []


    for k, v in _params.items():
        if k not in ("input_file", "db_name", "output_dir", "local_dir", "final_output", "remote_dir"):
            flags.extend(_flags[k](v))


    _lastdb_cmd = [
        "lastdb",
        final_output,
        input_file,
        "-P 8",
        *flags,
    ]

    print("Command to run from terminal: " + _lastal_cmd.join(" "))

    subprocess.run(_lastdb_cmd)

    return LatchDir(local_dir, remote_dir)


@workflow
def last_db(
    input_file : LatchFile,
    db_name : str,
    output_dir : LatchDir,
    proteinseq : bool = False,
    softmask_lc: bool = False,
    seed_scheme: Union[None, str] = None,
    lowercase: Union[None, str] = None,
    size: Union[None, str] = None,
    strand: Union[None, str] = None,
    sequence_file_type: Union[None, str] = None,
    proteinseq_with_end: Union[None, str] = None,
    spaced_seed_pattern: Union[None, str] = None,
    dna_seed_pattern: Union[None, str] = None,
    alphabet: Union[None, str] = None
    ) -> LatchDir:

    """
    LAST: find & align related regions of sequences

    This workflow is dedicated only to the lastdb command - for lastal see {link}
    All you need is a FASTA file to index. Additional options are set with their default values.

    LAST is designed for moderately large data (e.g. genomes, DNA reads,
    proteomes).  It's especially good at:

    * Finding DNA-versus-protein related regions, especially protein
    fossils.

    * Unusual data, e.g. AT-rich DNA, because we can fit parameters to
    the data and calculate significance.

    * Sensitive DNA-DNA search, due to fitting, sensitive seeding, and
    calculating significance.

    It can also: indicate the confidence/uncertainty of each column in an
    alignment, and use sequence quality data in a rigorous fashion.

    More details and citation: https://gitlab.com/mcfrith/last/-/blob/main/doc/last-papers.rst
    LAST is distributed under the GNU General Public License, either version 3 of the License, or (at your option) any later version.

    LAST is brought to you by:

    * Computational Omics Research Team, AIRC
    * GSFS, University of Tokyo
    * AIST-Waseda University CBBD-OIL

    __metadata__:
        display_name: lastdb
        author:
            name: Martin Frith
            email:
            github:
        repository: https://gitlab.com/mcfrith/last
        license:
            id: GNU
    Args:
        input_file:
            Reference sequence in fasta format
            __metadata__:
                display_name: "Reference sequence in fasta format"
        output_dir:
            Output directory path
            __metadata__:
                display_name: "Output Directory"
        db_name:
            Name of the output LAST database files
            __metadata__:
                display_name:   Name of the output LAST database files
        proteinseq:
            Protein sequence
            __metadata__:
            Interpret the sequences as proteins.  The default is to interpret them as DNA.

        softmask_lc:
            Soft-mask lowercase letters
            __metadata__:
            Soft-mask lowercase letters.  This means that, when we compare
            these sequences to some other sequences using lastal, lowercase
            letters will be excluded from initial matches.  This will apply
            to lowercase letters in both sets of sequences.
        seed_scheme:
            Specify a seeding scheme
            __metadata__:
              The built-in schemes are described in https://gitlab.com/mcfrith/last/-/blob/main/doc/last-seeds.rst
        lowercase:
            Specify lowercase usage, by two digits
            __metadata__:
            First digit:
            Convert the input sequences to uppercase while reading them.
            Keep any lowercase in the input sequences.
            Second digit:
            Do not check for simple repeats.
            Convert simple repeats (e.g. cacacacacacacacac) to
            lowercase.  This uses tantan, which reliably prevents
            non-homologous alignments, unlike other repeat finders.
            Convert simple DNA repeats to lowercase, with tantan tuned
            for ~80% AT-rich genomes.
            Convert simple repeats, including weaker simple repeats, to
            lowercase (with tantan's r parameter = 0.02).
            The default is -R01 (unless -q is specified, in which case
            the default is -R03).
        size:
            Allow initial matches to start only at positions that are
            "minimum" in any window of SIZE consecutive positions.
            "Minimum" means that the sequence starting here is
            alphabetically earliest
            __metadata__:
            The "alphabetical" order depends on the seed pattern.  The letter order is determined by the
            order of the letter groups, and letters in the same group are
            considered equivalent.
            The fraction of positions that are "minimum" is roughly: 2 / (SIZE + 1).
        strand:
            Specify which strand of the input sequences should be prepared
            for alignment: 0 means reverse only, 1 means forward only, and 2
            means both.
        sequence_file_type:
            Specify how to read the sequences:
            __metadata__:
            fasta, fastx (discard per-base quality data), keep (keep but ignore per-base quality data), fastq-sanger, fastq-solexa, fastq-illumina
        proteinseq_with_end:
            Interpret the sequences as proteins, use a 21-letter alphabet
            with * meaning STOP, and append * to each sequence
        spaced_seed_pattern:
            Specify a spaced seed pattern
        dna_seed_pattern:
            Specify DNA seed patterns
        alphabet:
            Specify your own alphabet
    """
    return(lastdb(input_file=input_file, db_name=db_name, output_dir=output_dir, proteinseq=proteinseq,softmask_lc=softmask_lc,
            seed_scheme=seed_scheme, lowercase=lowercase, size=size,strand=strand,sequence_file_type=sequence_file_type,proteinseq_with_end=proteinseq_with_end,
            spaced_seed_pattern=spaced_seed_pattern,dna_seed_pattern=dna_seed_pattern,alphabet=alphabet))
