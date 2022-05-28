""" A demonstration of a latch workflow constructed with full parameter parity
to nf-core/rnaseq.
"""

import csv
import subprocess
from enum import Enum
from pathlib import Path
from typing import List, Union

from latch import large_task, small_task, workflow
from latch.types import LatchDir, LatchFile

#PARAMETERS:
#IO: input, step, outdir
#MAIN: tools, no_intervals, nucleotides_per_second, sentieon, skip_qc, target_bed
#PREPROCESSING: use_gatk_spark, save_bam_mapped, skip_markduplicates
#VARIANTCALLING: ascat_ploidy, ascat_purity, cf_coeff, cf_contamination_adjustment, cf_contamination, cf_ploidy,
#cf_window, generate_gvcf, no_strelka_bp, pon, pon_index, ignore_soft_clipped_bases, umi, read_structure1, read_structure2
#
#REFERENCEGENOME: genome, ac_loci, ac_loci_gc, bwa, chr_dir, chr_length, dbsnp, dbsnp_index, dict, fasta, fasta_fai, germline_resource,
#germline_resource_index, intervals, known_indels, known_indels_index, mappability, snpeff_db, species, vep_cache_version, save_reference,
#igenomes_base, genomes_base,igenomes_ignore
#
#GENERIC --email
#JOB RESOURCES
#cpus, single_cpu_mem

#UNCOMMON PARAMETERS (HIDDEN)
#--trim_fastq, --clip_r1, --clip_r2, --three_prime_clip_r1, --three_prime_clip_r2, --trim_nextseq, --save_trimmed, --split_fastq,
#--aligner, --markdup_java_options, --annotate_tools, --annotation_cache, --cadd_cache, --cadd_indels, --cadd_indels_tbi, --cadd_wg_snvs,
#--cadd_wg_snvs_tbi, --genesplicer, --snpeff_cache, --vep_cache, --publish_dir_mode, --validate_params, --email_on_fail, --plaintext_email,
#--max_multiqc_email_size, --monochrome_logs, --multiqc_config, --tracedir, --sequencing_center, --show_hidden_params, --max_cpus, --max_memory,
#--max_time, --custom_config_version, --custom_config_base, --hostnames, --config_profile_name, --config_profile_description,
#--config_profile_contact, --config_profile_url




@large_task
def nf_sarek_task(
    output_dir: str,
) -> LatchDir:

    local_output="/root/sarek_output"
    remote_dir = f"latch:///{output_dir}/"

    nextflow_cmd = [
        "nextflow",
        "run",
        "nf-core/sarek",
        "--input",
        "root/test_data/data/tsv/tiny.tsv"
        "--genome",
        "GRCh38"
        "--outdir",
        str(local_output)
    ]
    subprocess.run(nextflow_cmd)

    return LatchDir(str(local_output), remote_dir)


@workflow
def nf_sarek_wf(
    output_dir: str,
) -> LatchDir:
    """A latch workflow wrapping nf-core/rnaseq.

    Write your own markdown documentation here...

    __metadata__:
        display_name: nf-core/sarek
        author:
            name: Nextflow Community
            email:
            github:
        repository:
        license:
            id: MIT

    Args:
        output_dir:
          The location of your outputs.

          __metadata__:
            display_name: Output Directory
    """
    return(nf_sarek_task(output_dir=output_dir))