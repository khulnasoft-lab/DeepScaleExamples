# This script requires pytorch >= 1.8
# (and nccl >= 2.8.3 if you have 64 or more GPUs).
# Read the tutorial for more details:
# https://www.deepscale.khulnasoft.com/tutorials/onebit-adam/

NUM_NODES=4
NGPU_PER_NODE=8
MODEL_FILE="../../ckpt/bert-large-uncased-whole-word-masking-pytorch_model.bin"
ORIGIN_CONFIG_FILE="../../ckpt/bert-large-uncased-whole-word-masking-config.json"
SQUAD_DIR="../../data"
OUTPUT_DIR=$1
LR=3e-5
SEED=$RANDOM
MASTER_PORT=12345
DROPOUT=0.1

sudo rm -rf ${OUTPUT_DIR}

NGPU=$((NGPU_PER_NODE*NUM_NODES))
EFFECTIVE_BATCH_SIZE=96
MAX_GPU_BATCH_SIZE=3
PER_GPU_BATCH_SIZE=$((EFFECTIVE_BATCH_SIZE/NGPU))
if [[ $PER_GPU_BATCH_SIZE -lt $MAX_GPU_BATCH_SIZE ]]; then
       GRAD_ACCUM_STEPS=1
else
       GRAD_ACCUM_STEPS=$((PER_GPU_BATCH_SIZE/MAX_GPU_BATCH_SIZE))
fi
JOB_NAME="onebit_deepscale_${NGPU}GPUs_${EFFECTIVE_BATCH_SIZE}batch_size"
config_json=deepscale_onebitadam_bsz96_config.json

# NCCL_IB_DISABLE=1 NCCL_SOCKET_IFNAME=eth0 are used to disable infiniband. Remove it if needed.
NCCL_TREE_THRESHOLD=0 NCCL_IB_DISABLE=1 NCCL_SOCKET_IFNAME=eth0 deepscale ../../nvidia_run_squad_deepscale.py \
--bert_model bert-large-uncased \
--do_train \
--do_lower_case \
--predict_batch_size 3 \
--do_predict \
--train_file $SQUAD_DIR/train-v1.1.json \
--predict_file $SQUAD_DIR/dev-v1.1.json \
--train_batch_size $PER_GPU_BATCH_SIZE \
--learning_rate ${LR} \
--num_train_epochs 2.0 \
--max_seq_length 384 \
--doc_stride 128 \
--output_dir $OUTPUT_DIR \
--job_name ${JOB_NAME} \
--gradient_accumulation_steps ${GRAD_ACCUM_STEPS} \
--fp16 \
--deepscale \
--deepscale_transformer_kernel \
--deepscale_config ${config_json} \
--dropout ${DROPOUT} \
--model_file $MODEL_FILE \
--seed ${SEED} \
--ckpt_type HF \
--origin_bert_config_file ${ORIGIN_CONFIG_FILE} \
