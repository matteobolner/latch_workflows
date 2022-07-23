""" A demonstration of a latch workflow constructed with full parameter parity
to nf-core/rnaseq.
"""

import csv
import subprocess
from enum import Enum
from pathlib import Path
from typing import List, Union

from latch import large_task, medium_task, small_task, workflow
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

#        genome:
#          Reference genome to use.
#            __metadata__:
#            display_name: Reference genome to use.
#        step:
#          Step of the workflow to start from
#          __metadata__:
#            display_name: Step of the workflow to start from


#class starting_steps(Enum):
#    mapping = "mapping"
#    prepare_recalibration = "prepare_recalibration"
#    recalibrate = "recalibrate"
#    variant_calling = "variant_calling"
#    annotate = "annotate"
#    ControlFREEC = "ControlFREEC"
#    preparecalibration = "preparecalibration"



#####PROBLEM WITH NOT WORKING MIGHT BE DUE TO SELECTING AN ALREADY EXISTING OUTPUT DIR
#####CHANGE FORMAT OF GENOME TO BGZIP FOR SAMTOOLS
@small_task
def nf_sarek_task(
#    starting_step: Union[starting_steps, None] = None,
    input_file: LatchFile,
    step: str,
    genome_file: LatchFile,
    output_dir: str,
) -> LatchDir:

    local_output="/root/test"
    remote_dir = f"latch:///{output_dir}/"

    nextflow_cmd = [
        "nextflow",
        "run",
        "nf-core/sarek",
        "--input",
        input_file.local_path,
        "--step=",
        step,
        "--igenomes_ignore=true",
        "--no_intervals=true",
        "--genome=custom",
        "--fasta",
        genome_file.local_path,
        #"schema_ignore_params='genomes'",
        #"--genome=smallGRCh37",
        #"--genomes_base = 'https://raw.githubusercontent.com/nf-core/test-datasets/sarek/reference'",
        #"snpeff_db='WBcel235.86'",
        #"--species=caenorhabditis_elegans",
        #"schema_ignore_params = 'genomes,input_paths,input'",
        "--max_cpus=4",
        "--max_memory=4.GB",
        "--outdir",
        str(local_output)
    ]
    subprocess.run(nextflow_cmd)
    return LatchDir(str(local_output), remote_dir)

_params = locals()
_flags = {
    "step": lambda x: ["--step", str(x)] if x is not None else [],
    "tools": lambda x: ["--tools", str(x)] if x is not None else [],
    "no_intervals": lambda x: ["--no_intervals"] if x is True else [],
    "nucleotides_per_second": lambda x: ["--nucleotides_per_second", str(x)] if x is not None else [],
    "skip_qc": lambda x: ["--skip_qc", str(x)] if x is not None else [],
    "target_bed": lambda x: ["--target_bed", str(x)] if x is not None else [],
    "trim_fastq": lambda x: ["--trim_fastq", str(x)] if x is True else [],
    "clip_r1": lambda x: ["--clip_r1", str(x)] if x is not None else [],
    "clip_r2": lambda x: n["--clip_r2", str(x)] if x is not None else [],



@small_task
def test_task(
    input_file: LatchFile,
    output_dir: str,
) -> LatchDir:

    local_output="/root/test"
    remote_dir = f"latch:///{output_dir}/"

    nextflow_cmd = [
        "nextflow",
        "run",
        "nf-core/sarek",
        "-profile",
        "conda",
        "input_file",
        str(input_file),
        "--outdir",
        str(local_output)
    ]
    subprocess.run(nextflow_cmd)
    return LatchDir(str(local_output), remote_dir)


@workflow
def nf_sarek_wf(
    input_file: LatchFile,
    step: str,
    genome_file: LatchFile,
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
        input_file:
          Input tsv
          __metadata__:
            display_name: Input tsv

        step:
          Starting step of the pipeline
          __metadata__:
            display_name: Starting step of the pipeline

        genome_file:
          Genome file in fasta format
          __metadata__:
            display_name: Genome file in fasta format

        output_dir:
          The location of your outputs.
          __metadata__:
            display_name: Output Directory

    """
    return(nf_sarek_task(input_file=input_file, step=step, genome_file=genome_file, output_dir=output_dir))
    #return(test_task(output_dir=output_dir))

#if __name__ == "__main__":
#    nf_sarek_wf(output_dir="/root/sarek_output/")
