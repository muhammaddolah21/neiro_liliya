#!/bin/bash
# Универсальный pipeline для запуска fine-tuning, инференса и оценки UniLM на всех downstream задачах
# Пример использования: bash run_pipeline.sh --task qa --dataset squad --mode qa

set -e

# Аргументы командной строки
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --task) TASK="$2"; shift ;;
    --dataset) DATASET="$2"; shift ;;
    --mode) MODE="$2"; shift ;;
    --split) SPLIT="$2"; shift ;;
    --config) CONFIG="$2"; shift ;;
    --checkpoint) CHECKPOINT="$2"; shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
  shift
done

# Значения по умолчанию
TASK=${TASK:-qa}
DATASET=${DATASET:-squad}
MODE=${MODE:-qa}
SPLIT=${SPLIT:-all}
CONFIG=${CONFIG:-configs/config_unilm.yaml}
CHECKPOINT=${CHECKPOINT:-"pretrained/unilm-base-cased.pt"}

# 1. Подготовка данных
if [[ "$DATASET" == "squad" ]]; then
  echo "Preparing SQuAD..."
  python data/squad/prepare_squad.py --mode $MODE --split $SPLIT
elif [[ "$DATASET" == "cnn_dm" ]]; then
  echo "Preparing CNN/DM..."
  python data/cnn_dm/prepare_cnndm.py --split $SPLIT
elif [[ "$DATASET" == "duc" ]]; then
  echo "Preparing DUC..."
  python data/duc/prepare_duc.py --split $SPLIT
else
  echo "Unknown dataset: $DATASET"; exit 1
fi

# 2. Fine-tuning (пример для run_seq2seq.py)
echo "Starting fine-tuning..."
python scripts/run_seq2seq.py \
  --config $CONFIG \
  --task $TASK \
  --dataset $DATASET \
  --mode $MODE \
  --checkpoint $CHECKPOINT

# 3. Инференс (пример)
echo "Running inference..."
python scripts/decode_seq2seq.py \
  --config $CONFIG \
  --task $TASK \
  --dataset $DATASET \
  --mode $MODE

# 4. Оценка метрик
echo "Evaluating metrics..."
python scripts/evaluate_metrics.py \
  --task $TASK \
  --dataset $DATASET \
  --mode $MODE

# 5. Сохранение результатов
echo "Saving results..."
python scripts/save_result.py \
  --task $TASK \
  --dataset $DATASET \
  --mode $MODE

echo "Pipeline finished!"
