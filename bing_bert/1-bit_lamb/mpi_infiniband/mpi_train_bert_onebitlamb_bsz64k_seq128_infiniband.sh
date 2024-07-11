#!/bin/bash

# If you are able to install pytorch >= 1.8
# (and nccl >= 2.8.3 if you have 64 or more GPUs),
# we highly recommend you to use the NCCL-based 1-bit Lamb
# which has better performance and ease of use
# (see scripts in DeepScaleExamples/bing_bert/1-bit_lamb/nccl
# and read the tutorial for more details:
# https://www.deepscale.khulnasoft.com/tutorials/onebit-lamb/)

# Note: Please use the deepscale launch script for most cases.
# For advanced users, mpirun or other MPI launchers can be used
# with this script as follows.
# mpirun -n 2 [launcher-args] python ${base_dir}/../deepscale_train.py
# As an example, below we include the command we used

base_dir=`pwd`

# Where should we save checkpoints and tensorboard events?
JOB_NAME=onebit_lamb_64k_seq128_mpirun_infiniband
OUTPUT_DIR=${base_dir}/bert_model_outputs

mkdir -p $OUTPUT_DIR

# LD_PRELOAD is used to load a specific nccl version. Remove it if needed.
mpirun -n 128 -ppn 8 -f /tmp/deepscale_mvapich_hostfile -env MV2_SUPPORT_DL=1 -env MV2_USE_GDR=0 -env MV2_USE_CUDA=1 -env MV2_USE_GDRCOPY=0 -env MV2_SMP_USE_CMA=0 -env MV2_DEBUG_SHOW_BACKTRACE=1 python ${base_dir}/../../deepscale_train.py \
--cf ${base_dir}/../../bert_large_lamb.json \
--max_seq_length 128 \
--output_dir $OUTPUT_DIR \
--deepscale_mpi \
--deepscale \
--deepscale_transformer_kernel \
--print_steps 40 \
--lr_schedule "EE" \
--lr_offset 10e-4 \
--job_name $JOB_NAME \
--deepscale_config ${base_dir}/deepscale_bsz64k_onebitlamb_config_seq128_mpi_infiniband.json \
--data_path_prefix /data/bert \
&> ${JOB_NAME}.log
