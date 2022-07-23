""" Beast
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
def beast_and_treeannotator_task(
    input_xml: LatchFile,
    output_dir: str,
    burnin: int,
    target_tree: Optional[LatchFile],
    burnin_type: str = 'states',
    node_heights: str = 'keep',
) -> LatchDir:

    local_output="/root/beast_output"
    remote_dir = f"latch:///{output_dir}/"


    beast_cmd = [
        "beast",
        "-threads 8",
        input_xml.local_path
    ]

    subprocess.run(beast_cmd)

    xml_filename = os.path.splitext(input_xml.remote_path)[0].split("/")[-1]
    for i in ['ops','log','trees']:
        subprocess.run(["mv",f"{xml_filename}.{i}", "/root/beast_output/"])

    if burnin_type=='states':
        burnin_type_str=''
    else:
        burnin_type_str='Trees'

    if target_tree:
        treeannotator_cmd = [
            "treeannotator",
            f"-burnin{str(burnin_type_str)}",
            str(burnin),
            "-heights",
            str(node_heights),
            "-target",
            target_tree.local_path,
            f"/root/beast_output/{xml_filename}.trees",
            f"/root/beast_output/{xml_filename}.tree"
            ]
    else:
        treeannotator_cmd = [
            "treeannotator",
            f"-burnin{str(burnin_type_str)}",
            str(burnin),
            "-heights",
            str(node_heights),
            f"/root/beast_output/{xml_filename}.trees",
            f"/root/beast_output/{xml_filename}.tree"
            ]
    subprocess.run(treeannotator_cmd)

    return LatchDir(str(local_output), remote_dir)

    #heights an option of 'keep' (default), 'median', 'mean' or 'ca'
    #burnin the number of states or trees to be considered as 'burn-in'
    #limit the minimum posterior probability for a node to be annotated
    #input_tree specifies a user target tree to be annotated
    #-forceDiscrete forces integer traits to be treated as discrete traits.
    #-hpd2D specifies a (vector of comma seperated) HPD proportion(s)

@workflow
def beast_and_treeannotator(
    input_xml: LatchFile,
    output_dir: str,
    burnin: int,
    target_tree: Optional[LatchFile],
    burnin_type: str = 'states',
    node_heights: str = 'keep',
    ) -> LatchDir:
    """ BEAST
    BEAST is a cross-platform program for Bayesian analysis of molecular sequences using MCMC.<br/>
    It is entirely orientated towards rooted, time-measured phylogenies inferred using strict or relaxed molecular clock models.<br/>
    It can be used as a method of reconstructing phylogenies but is also a framework for testing evolutionary hypotheses without conditioning on a single tree topology.<br/>
    BEAST uses MCMC to average over tree space, so that each tree is weighted proportional to its posterior probability.<br/>
    The latch.bio implementation includes the BEAST and TREEANNOTATOR programs; the input file needed is an XML file that can be generated using BEAUTI's GUI (can be downloaded from https://github.com/beast-dev/beast-mcmc/releases/tag/v1.10.4 . <br/>
    TREEANNOTATOR takes as input the output trees from BEAST and obtains a single maximum clade credibilty (MCC) tree.

    __metadata__:
        display_name: Beast
        author:
            name:
            email:
            github: https://github.com/beast-dev/beast-mcmc
        repository:
        license:
            id: GPLv3

    Args:
        input_xml:
            XML file generated with BEAUTI
            __metadata__:
            display_name: Input XML

        output_dir:
          Output directory name
          __metadata__:
            display_name: Output directory name

        burnin_type:
            TREEANNOTATOR - Type of burnin: states or trees (default states)
            __metadata__:
                display_name: Burnin type
                appearance:
                    multiselect:
                        options:
                            - states
                            - trees
                        allow_custom: false
        burnin:
            TREEANNOTATOR - Number of states (or trees) to be considered as 'burn-in'
            __metadata__:
                display_name: Burnin

        node_heights:
            TREEANNOTATOR - This option allows you to select how the node heights are summarised on the target tree. You can choose to keep the heights that the target tree has, or rescale it to reflect the posterior mean/median node heights for the clades contained in the target tree.
            __metadata__:
                display_name: Node heights
                appearance:
                    multiselect:
                        options:
                            - keep
                            - median
                            - mean
                            - ca
                        allow_custom: false
              _tmp:
                hidden: true

        target_tree:
            TREEANNOTATOR - If you select this option then the tree statistics will be summarized on a user-specified tree.
            __metadata__:
                display_name: Target tree


    """
    return(beast_and_treeannotator_task(input_xml=input_xml, output_dir=output_dir, burnin_type=burnin_type, burnin=burnin, node_heights=node_heights, target_tree=target_tree))



#TREEANNOTATOR OPTIONS
#    -heights an option of 'keep' (default), 'median', 'mean' or 'ca'
#    -burnin the number of states to be considered as 'burn-in'
#    -burninTrees the number of trees to be considered as 'burn-in'
#    -limit the minimum posterior probability for a node to be annotated
#    -target specifies a user target tree to be annotated
#    -help option to print this message
#    -forceDiscrete forces integer traits to be treated as discrete traits.
#    -hpd2D specifies a (vector of comma seperated) HPD proportion(s)


#BEAST OPTIONS
#    -verbose Give verbose XML parsing messages
#    -warnings Show warning messages about BEAST XML file
#    -strict Fail on non-conforming BEAST XML file
#    -window Provide a console window
#    -options Display an options dialog
#    -working Change working directory to input file's directory
#    -seed Specify a random number generator seed
#    -prefix Specify a prefix for all output log filenames
#    -overwrite Allow overwriting of log files
#    -errors Specify maximum number of numerical errors before stopping
#    -threads The number of computational threads to use (default auto)
#    -java Use Java only, no native implementations
#    -tests The number of full evaluation tests to perform (default 1000)
#    -threshold Full evaluation test threshold (default 0.1)
#    -adaptation_off Don't adapt operator sizes
#    -adaptation_target Target acceptance rate for adaptive operators (default 0.234)
#    -beagle Use BEAGLE library if available (default on)
#    -beagle_info BEAGLE: show information on available resources
#    -beagle_order BEAGLE: set order of resource use
#    -beagle_instances BEAGLE: divide site patterns amongst instances
#    -beagle_multipartition BEAGLE: use multipartition extensions if available (default auto)
#    -beagle_CPU BEAGLE: use CPU instance
#    -beagle_GPU BEAGLE: use GPU instance if available
#    -beagle_SSE BEAGLE: use SSE extensions if available
#    -beagle_SSE_off BEAGLE: turn off use of SSE extensions
#    -beagle_threading_off BEAGLE: turn off auto threading for a CPU instance
#    -beagle_thread_count BEAGLE: manually set number of threads for a CPU instance
#    -beagle_cuda BEAGLE: use CUDA parallization if available
#    -beagle_opencl BEAGLE: use OpenCL parallization if available
#    -beagle_single BEAGLE: use single precision if available
#    -beagle_double BEAGLE: use double precision if available
#    -beagle_async BEAGLE: use asynchronous kernels if available
#    -beagle_scaling BEAGLE: specify scaling scheme to use
#    -beagle_delay_scaling_off BEAGLE: don't wait until underflow for scaling option
#    -beagle_rescale BEAGLE: frequency of rescaling (dynamic scaling only)
#    -mpi Use MPI rank to label output
#    -particles Specify a folder of particle start states
#    -mc3_chains number of chains
#    -mc3_delta temperature increment parameter
#    -mc3_temperatures a comma-separated list of the hot chain temperatures
#    -mc3_swap frequency at which chains temperatures will be swapped
#    -citations_file Specify a filename to write a citation list to
