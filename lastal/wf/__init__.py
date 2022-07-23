"""
LASTAL
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchDir, LatchFile
from typing import Optional, List, Union
import os

@small_task
def lastal(
    input_db_dir: LatchDir,
    input_db : LatchFile,
    input_file: LatchFile,
    output_filename: str,
    output_directory: LatchDir,
    output_format : str = 'MAF',
    aln_per_length: Union[None, str] = None,
    eg2_max_val: Union[None, str] = None,
    match_score: Union[None, str] = None,
    mismatch_cost: Union[None, str] = None,
    score_matrix: Union[None, str] = None,
    n_x_score: str = '0',
    gap_open_cost: Union[None, str] = None,
    gap_extension_cost: Union[None, str] = None,
    insertion_existence_cost: Union[None, str] = None,
    insertion_extension_cost: Union[None, str] = None,
    generalized_affine_gap_costs: Union[None, str] = None,
    frameshift_costs: Union[None, str] = None,
    max_score_drop_gapped: Union[None, str] = None,
    extend_gapped_twice: Union[None, str] = None,
    max_score_drop_gapless: Union[None, str] = None,
    min_score_drop_gapless: Union[None, str] = None,
    min_aln_score: Union[None, str] = None,
    multiplicity: Union[None, str] = None,
    min_length: Union[None, str] = None,
    max_length: Union[None, str] = None,
    step: Union[None, str] = None,
    strand: str = '2',
    sub_score_matrix_rev_strands: Union[None, str] = None,
    limit_other_alignments: Union[None, str] = None,
    discard_gapless_in_range: Union[None, str] = None,
    max_gapless_per_position: Union[None, str] = None,
    mark_repeats: Union[None, str] = None,
    lowercase_treatment: str = '0',
    genetic_code: Union[None, str] = None,
    temperature: Union[None, str] = None,
    gamma: Union[None, str] = None,
    output_type: Union[None, str] = None,
    score_type: Union[None, str] = None,
    query_format: str = 'fastx',
    ) -> LatchFile:

    local_dir = "/root/lastal_folder"
    final_output= f"{local_dir}/{output_filename}.{output_format}"
    output_path = f"{output_directory.remote_path}/{output_filename}.{output_format}"

    _params = locals()
    _flags = {
        "output_format" : lambda x: ["-f", str(x)] if x is not None else [],
        "aln_per_length": lambda x: ["-D", str(x)] if x is not None else [],
        "eg2_max_val": lambda x: ["-E", str(x)] if x is not None else [],
        "match_score": lambda x: ["-r", str(x)] if x is not None else [],
        "mismatch_cost": lambda x: ["-q", str(x)] if x is not None else [],
        "score_matrix": lambda x: ["-p", str(x)] if x is not None else [],
        "n_x_score": lambda x: ["-X", str(x)] if x is not None else [],
        "gap_open_cost": lambda x: ["-a", str(x)] if x is not None else [],
        "gap_extension_cost": lambda x: ["-b", str(x)] if x is not None else [],
        "insertion_existence_cost": lambda x: ["-A", str(x)] if x is not None else [],
        "insertion_extension_cost": lambda x: ["-B", str(x)] if x is not None else [],
        "generalized_affine_gap_costs": lambda x: ["-c", str(x)] if x is not None else [],
        "frameshift_costs": lambda x: ["-F", str(x)] if x is not None else [],
        "max_score_drop_gapped": lambda x: ["-z", str(x)] if x is not None else [],
        "extend_gapped_twice": lambda x: ["-x", str(x)] if x is not None else [],
        "max_score_drop_gapless": lambda x: ["-y", str(x)] if x is not None else [],
        "min_score_drop_gapless": lambda x: ["-d", str(x)] if x is not None else [],
        "min_aln_score": lambda x: ["-e", str(x)] if x is not None else [],
        "multiplicity": lambda x: ["-m", str(x)] if x is not None else [],
        "min_length": lambda x: ["-l", str(x)] if x is not None else [],
        "max_length": lambda x: ["-L", str(x)] if x is not None else [],
        "step": lambda x: ["-k", str(x)] if x is not None else [],
        "strand": lambda x: ["-s", str(x)] if x is not None else [],
        "sub_score_matrix_rev_strands": lambda x: ["-S", str(x)] if x is not None else [],
        "limit_other_alignments": lambda x: ["-K", str(x)] if x is not None else [],
        "discard_gapless_in_range": lambda x: ["-C", str(x)] if x is not None else [],
        "max_gapless_per_position": lambda x: ["-n", str(x)] if x is not None else [],
        "mark_repeats": lambda x: ["-R", str(x)] if x is not None else [],
        "lowercase_treatment": lambda x: ["-u", str(x)] if x is not None else [],
        "genetic_code": lambda x: ["-G", str(x)] if x is not None else [],
        "temperature": lambda x: ["-t", str(x)] if x is not None else [],
        "gamma": lambda x: ["-g", str(x)] if x is not None else [],
        "output_type": lambda x: ["-j", str(x)] if x is not None else [],
        "score_type": lambda x: ["-J", str(x)] if x is not None else [],
        "query_format": lambda x: ["-Q", str(x)] if x is not None else []
        }


    flags = []


    for k, v in _params.items():
        if k not in ("input_db_dir","input_file", "input_db", "output_filename", "local_dir", "final_output","output_path","output_directory"):
            flags.extend(_flags[k](v))

    #db_dir = os.path.split(input_db.local_path)
    input_db_noext = os.path.splitext(input_db.local_path)[0]
    lastdb_name = input_db_noext.split("/")[-1]
    fixed_path = str(input_db_dir.local_path)+"/"+lastdb_name

    _lastal_cmd = [
        "lastal",
        fixed_path,
        input_file,
        *flags
    ]

    with open(final_output, "w") as outfile:
        subprocess.run(_lastal_cmd, stdout=outfile)

#   print("Command to run from terminal: " + (" ").join(_lastal_cmd))

    return LatchFile(final_output, output_path)


@workflow
def lastal_wf(
    input_db_dir: LatchDir,
    input_db : LatchFile,
    input_file: LatchFile,
    output_filename: str,
    output_directory: LatchDir,
    output_format : str='MAF',
    aln_per_length: Union[None, str] = None,
    eg2_max_val: Union[None, str] = None,
    match_score: Union[None, str] = None,
    mismatch_cost: Union[None, str] = None,
    score_matrix: Union[None, str] = None,
    n_x_score: str = '0',
    gap_open_cost: Union[None, str] = None,
    gap_extension_cost: Union[None, str] = None,
    insertion_existence_cost: Union[None, str] = None,
    insertion_extension_cost: Union[None, str] = None,
    generalized_affine_gap_costs: Union[None, str] = None,
    frameshift_costs: Union[None, str] = None,
    max_score_drop_gapped: Union[None, str] = None,
    extend_gapped_twice: Union[None, str] = None,
    max_score_drop_gapless: Union[None, str] = None,
    min_score_drop_gapless: Union[None, str] = None,
    min_aln_score: Union[None, str] = None,
    multiplicity: Union[None, str] = None,
    min_length: Union[None, str] = None,
    max_length: Union[None, str] = None,
    step: Union[None, str] = None,
    strand: str = '2',
    sub_score_matrix_rev_strands: Union[None, str] = None,
    limit_other_alignments: Union[None, str] = None,
    discard_gapless_in_range: Union[None, str] = None,
    max_gapless_per_position: Union[None, str] = None,
    mark_repeats: Union[None, str] = None,
    lowercase_treatment: str = '0',
    genetic_code: Union[None, str] = None,
    temperature: Union[None, str] = None,
    gamma: Union[None, str] = None,
    output_type: Union[None, str] = None,
    score_type: Union[None, str] = None,
    query_format: str = 'fastx',
    ) -> LatchFile:

    """
    LAST: find & align related regions of sequences

    This workflow is dedicated only to the lastal command - for lastal see {link will be available soon}
    All you need is a FASTA file to search against a lastdb-indexed database. Additionazl options are set with their default values.

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
        display_name: lastal
        author:
            name: Martin Frith
            email:
            github:
        repository: https://gitlab.com/mcfrith/last
        license:
            id: GNU

    Args:
        input_db_dir:
            Directory containing the database indexed with lastdb
            __metadata__:
            display_name: "Last-indexed database folder"

        input_db:
            Select any of the files generated from lastdb
            __metadata__:
            display_name: "Last-indexed database file"

        input_file:
            __metadata__:
            display_name: "Query file in fasta format"

        output_filename:
            Filename for the output alignment
            __metadata__:
            display_name: "Alignment file name"

        output_directory:
            Directory where to place the alignment file
            __metadata__:
            display_name: "Output directory"

        output_format:
            See LASTAL docs on gitlab for a detailed explanation of the different formats (default format is MAF)
            __metadata__:
            display_name: "Alignment file format"
            appearance:
                multiselect:
                    options:
                        - MAF
                        - TAB
                        - BlastTab
                        - BlastTab+
                    allow_custom: false

        aln_per_length:
            Report alignments that are expected by chance at most once per LENGTH query letters.
            __metadata__:
            display_name: "Report alignments that are expected by chance at most once per LENGTH query letters."

        eg2_max_val:
            Maximum EG2 (expected alignments per square giga).
            __metadata__:
            display_name: "Maximum EG2 (expected alignments per square giga)."

        match_score:
            Match score
            __metadata__:
            display_name: "Match score"

        mismatch_cost:
            Mismatch cost
            __metadata__:
            display_name: "Mismatch cost"

        score_matrix:
            Specify a match/mismatch score matrix, such as AT77,ATMAP,BISF,BISR,BLOSUM62,BLOSUM80,HOXD70,MIQS,PAM10,PAM30 (see https://gitlab.com/mcfrith/last/-/blob/main/doc/last-matrices.rst)
            __metadata__:
            display_name: "Score matrix"

        n_x_score:
            How to score a match/mismatch involving N (for DNA) or X (otherwise), if not specified by a score matrix. By default,the lowest match/mismatch score is used.  0 means the default; 1 means treat reference Ns/Xs as fully-ambiguous letters; 2 means treat query Ns/Xs as ambiguous; 3 means treat reference and query Ns/Xs as ambiguous.
            __metadata__:
            display_name: "Score N (for DNA) or X (otherwise)"
            appearance:
                multiselect:
                    options:
                        - '0'
                        - '1'
                        - '2'
                        - '3'
                    allow_custom: false

        gap_open_cost:
            Gap existence cost.
            __metadata__:
            display_name: "Gap existence"

        gap_extension_cost:
            Gap extension cost.  A gap of size k costs: a + (b × k).
            __metadata__:
            display_name: "Gap extension"

        insertion_existence_cost:
            Insertion existence cost.  This refers to insertions in the
            query relative to the reference.  If this option is not used, the
            insertion existence cost will equal the deletion existence cost.
            __metadata__:
            display_name: "Insertion existence"

        insertion_extension_cost:
            Insertion extension cost.
            __metadata__:
            display_name: "Insertion extension"

        generalized_affine_gap_costs:
            This option allows use of "generalized affine gap costs" (SF
            Altschul 1998, Proteins 32(1):88-96).  Here, a "gap" may consist
            of unaligned regions of both sequences.  If these unaligned
            regions have sizes j and k, where j ≤ k, the cost is: a +
            b⋅(k-j) + c⋅j.  If c ≥ a + 2b (the default), it reduces to
            standard affine gaps.
            __metadata__:
            display_name: "Generalized affine gap cost"

        frameshift_costs:
            Align DNA queries to protein reference sequences, using the
            specified frameshift cost(s): either one cost (old-style
            frameshifts), or 4 comma-separated costs (new-style
            frameshifts).
            __metadata__:
            display_name: "Frameshift costs"

        max_score_drop_gapped:
            Maximum score drop for gapped alignments.  Gapped alignments are
            forbidden from having any internal region with score < -DROP.
            The default value is e-1, which arguably produces the best
            alignments.  Lower values improve speed, by quitting unpromising
            extensions sooner.  You can specify this parameter in 3 ways: a score(8), percentage(8%), or gap length (8g)
            __metadata__:
            display_name: "Maximum score for gapped alignments"

        extend_gapped_twice:
            This option makes lastal extend gapped alignments twice.  First,
            it extends gapped alignments with a maximum score drop of x, and
            discards those with score < e.  The surviving alignments are
            redone with a (presumably higher) maximum score drop of z.  This
            aims to improve speed with minimal effect on the final
            alignments
            __metadata__:
            display_name: "Extend gapped aligments twice"

        max_score_drop_gapless:
            Maximum score drop for gapless alignments.
            __metadata__:
            display_name: "Maximum score drop for gapless alignments"

        min_score_drop_gapless: Union[None, str] = None,
            Minimum score for gapless alignments.
            __metadata__:
            display_name: "Minimum score for gapless alignments"

        min_aln_score:
            Minimum alignment score.
            __metadata__:
            display_name: "Minimum alignment score"

        multiplicity:
            Maximum multiplicity for initial matches.  Each initial match is
            lengthened until it occurs at most this many times in the
            reference.
            __metadata__:
            display_name: "Maximum multiplicity for initial matches"

        min_length:
            Minimum length for initial matches. Length means the number of letters spanned by the match.
            __metadata__:
            display_name: "Minimum length for initial matches"

        max_length:
            __metadata__:
            display_name: "Maximum length for initial matches."

        step:
            Minimum length for initial matches. Length means the number of letters spanned by the match.
            __metadata__:
            display_name: "Minimum length for initial matches"

        strand:
            Specify which query strand should be used: 0 means reverse only, 1 means forward only, and 2 means both.
            __metadata__:
            display_name: "Query strand"
            appearance:
                multiselect:
                    options:
                        - '0'
                        - '1'
                        - '2'
                    allow_custom: false

        sub_score_matrix_rev_strands:
            Specify how to use the substitution score matrix for reverse
            strands.  This matters only for unusual matrices that lack
            strand symmetry (e.g. if the a:g score differs from the t:c
            score).  "0" means that the matrix is used as-is for all
            alignments.  "1" means that the matrix is used as-is for
            alignments of query sequence forward strands, and the
            complemented matrix is used for query sequence reverse strands.
            __metadata__:
            display_name: "Substitution score matrix for reverse strands"

        limit_other_alignments:
            Omit any alignment whose query range is contained in LIMIT or more
            other alignments with higher score (and on the same strand).  This
            is a useful way to get just the top few hits to each part of each
            query (P Berman et al. 2000, J Comput Biol 7:293-302).  As a
            special case, a LIMIT of 0 means: omit any alignment whose query
            range overlaps an alignment with higher score (and on the same
            strand).
            __metadata__:
            display_name: "Omit any alignment whose query range is contained in LIMIT or more other alignments with higher score (and on the same strand)"

        discard_gapless_in_range:
            Before extending gapped alignments, discard any gapless
            alignment whose query range lies in LIMIT or more others (for
            the same strand and volume) with higher score-per-length.  This
            can reduce run time and output size (MC Frith & R Kawaguchi
            2015, Genome Biol 16:106).
            __metadata__:
            display_name: "Before extending gapped alignments, discard any gapless
            alignment whose query range lies in LIMIT or more others (for
            the same strand and volume) with higher score-per-length"

        max_gapless_per_position:
            Maximum number of gapless alignments per query position.  When
            lastal extends gapless alignments from initial matches that
            start at one query position, if it gets COUNT successful
            extensions, it skips any remaining initial matches starting at
            that position.
            __metadata__:
            display_name: "Maximum number of gapless alignments per query position"

        mark_repeats:
            Specify lowercase-marking of repeats, by two digits (e.g. "01"),
            with the following meanings.
            First digit:
            Convert the input sequences to uppercase while reading them.
            Keep any lowercase in the input sequences.
            Second digit:
            0.Do not check for simple repeats.
            1.Convert simple repeats (e.g. cacacacacacacacac) to lowercase.
            2.Convert simple repeats, within AT-rich DNA, to lowercase.
            3.Convert simple repeats, including weaker simple repeats, to
            lowercase (with tantan's r parameter = 0.02).
            Details: Tantan is applied separately to forward and reverse
            strands.  For DNA-versus-protein alignment, if you use a codon
            substitution matrix (e.g. from last-train --codon), tantan
            is applied to the DNA before translation, else it is applied
            after translation.
            __metadata__:
            display_name: "Maximum number of gapless alignments per query position"

        lowercase_treatment:
            Specify treatment of lowercase letters when extending
            alignments:
            0. Mask them for neither gapless nor gapped extensions.
            1. Mask them for gapless but not gapped extensions.
            2. Mask them for gapless but not gapped extensions, and then
            discard alignments that lack any segment with score ≥ e when
            lowercase is masked.  (For "full scores": mask them for gapless
            and gapped extensions, then recalculate the alignments but not
            the scores without masking.)
            3. Mask them for gapless and gapped extensions.
            "Mask" means change their match/mismatch scores to min(unmasked
            score, 0), a.k.a. gentle masking.  (But if you use a codon
            substitution matrix, a lowercase-containing base-triplet will be
            scored as nnn, which defaults to the lowest match/mismatch
            score.)
            This option does not affect treatment of lowercase for initial
            matches.
            __metadata__:
            display_name: "Specify treatment of lowercase letters when extending alignments"
            appearance:
                multiselect:
                    options:
                        - '0'
                        - '1'
                        - '2'
                        - '3'
                    allow_custom: false

        genetic_code:
            Specify the genetic code for translating DNA to protein.  Codes
            are specified by numbers (e.g. 1 = standard, 2 = vertebrate
            mitochondrial), listed here:
            https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi.
            __metadata__:
            display_name: "Genetic code"

        temperature:
            Parameter for converting between scores and probability ratios.
            This affects the column ambiguity estimates.  A score is
            converted to a probability ratio by this formula: exp(score /
            TEMPERATURE).  The default value is 1/lambda, where lambda is
            the scale factor of the scoring matrix, which is calculated by
            the method of Yu and Altschul (YK Yu et al. 2003, PNAS
            100(26):15688-93).
            __metadata__:
            display_name: "Temperature"

        gamma:
            This option affects gamma-centroid and LAMA alignment only.
            Gamma-centroid alignments minimize the ambiguity of paired
            letters.  In fact, this method aligns letters whose column error
            probability is less than GAMMA/(GAMMA+1).  When GAMMA is low, it
            aligns confidently-paired letters only, so there tend to be many
            unaligned letters.  When GAMMA is high, it aligns letters more
            liberally.
            LAMA (Local Alignment Metric Accuracy) alignments minimize the
            ambiguity of columns (both paired letters and gap columns).
            When GAMMA is low, this method produces shorter alignments with
            more-confident columns, and when GAMMA is high it produces
            longer alignments including less-confident columns.
            In summary: to get the most accurately paired letters, use
            gamma-centroid.  To get accurately placed gaps, use LAMA.
            Note that the reported alignment score is that of the gapped
            alignment before realigning with gamma-centroid or LAMA.
            __metadata__:
            display_name: "Gamma-centroid or LAMA alignment"
        output_type:
            Output type: 0 means counts of initial matches (of all lengths);
            1 means gapless alignments; 2 means gapped alignments before
            non-redundantization; 3 means gapped alignments after
            non-redundantization; 4 means alignments with ambiguity
            estimates; 5 means gamma-centroid alignments; 6 means LAMA
            alignments; 7 means alignments with expected counts.
            If you use -j0, lastal will count the number of initial matches,
            per length, per query sequence.  Options -l and -L will set the
            minimum and maximum lengths, and -m will be ignored.  If you
            compare a large sequence to itself with -j0, it's wise to set
            option -L.
            If you use -j7, lastal will print an extra MAF line starting
            with "c" for each alignment.  The first 16 numbers on this line
            are the expected counts of matches and mismatches: first the
            count of reference As aligned to query As, then the count of
            reference As aligned to query Cs, and so on.  For proteins there
            will be 400 such numbers.  The next 5 numbers are expected
            counts related to gaps.  They are:
            1)The count of matches plus mismatches.  (This may exceed the
            total of the preceding numbers, if the sequences have non-ACGT
            letters.)
            2)The count of deleted letters.
            3)The count of inserted letters.
            4)The count of delete opens (= count of delete closes).
            5)The count of insert opens (= count of insert closes).

            __metadata__:
            display_name: "Output type (0-7)"

        score_type:
            Score type: 0 means ordinary score, 1 means "full score" (also
            known as "forward score" or "sum-of-paths score").  Both types of
            score are measures of how significant a similarity is.  An
            ordinary score is based on one alignment, whereas a "full score"
            is based on many alternative ways of aligning the similar regions.
            Full scores are expected to be more sensitive, but they are not
            recognized by last-split.  Full score E-values can be calculated
            only for parameters from last-train.

            __metadata__:
            display_name: "Score type (0-1)"

        query_format:
            Specify how to read the query sequences (the NAME is not case-sensitive)

            __metadata__:
            display_name: "Query format"
            appearance:
                multiselect:
                    options:
                        - 'fastx'
                        - 'keep'
                        - 'sanger'
                        - 'solexa'
                        - 'illumina'
                        - 'prb'
                        - 'pssm'
                    allow_custom: false

        """
    return(lastal(input_db_dir=input_db_dir,input_db=input_db, input_file=input_file, output_filename=output_filename,output_directory=output_directory,
            output_format=output_format,aln_per_length=aln_per_length,eg2_max_val=eg2_max_val,match_score=match_score,mismatch_cost=mismatch_cost,
            score_matrix=score_matrix, n_x_score=n_x_score, gap_open_cost=gap_open_cost,gap_extension_cost=gap_extension_cost, insertion_existence_cost=insertion_existence_cost,
            insertion_extension_cost=insertion_extension_cost, generalized_affine_gap_costs=generalized_affine_gap_costs, frameshift_costs=frameshift_costs, max_score_drop_gapped=max_score_drop_gapped,
            extend_gapped_twice=extend_gapped_twice, max_score_drop_gapless=max_score_drop_gapless,min_score_drop_gapless=min_score_drop_gapless, min_aln_score=min_aln_score, multiplicity=multiplicity,
            min_length=min_length, max_length=max_length, step=step, strand=strand, sub_score_matrix_rev_strands=sub_score_matrix_rev_strands, limit_other_alignments=limit_other_alignments,
            discard_gapless_in_range=discard_gapless_in_range, max_gapless_per_position=max_gapless_per_position, mark_repeats=mark_repeats, lowercase_treatment=lowercase_treatment,
            genetic_code=genetic_code, temperature=temperature, gamma=gamma, output_type=output_type, score_type=score_type, query_format=query_format))
