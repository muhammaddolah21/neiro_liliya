#!/bin/bash
# Универсальный скрипт для запуска инференса, оценки и сохранения результатов для UniLM
# Пример для одной downstream-задачи (можно повторять для других)

# 1. Запуск инференса (пример, путь и параметры подставьте свои)
echo "[Step 1] Inference..."
python scripts/run_seq2seq.py --config configs/config_unilm.yaml --mode predict --input data/squad/dev.src --output predictions.txt

# 2. Оценка метрик (пример для SQuAD/QA)
echo "[Step 2] Evaluate metrics..."
python scripts/evaluate_metrics.py --pred predictions.txt --ref data/squad/dev.tgt > metrics.log

# 3. Сохранение результатов в таблицу (пример для всех метрик)
for metric in ROUGE-1 ROUGE-2 ROUGE-L BLEU METEOR "Exact Match" F1; do
    value=$(grep "$metric" metrics.log | awk '{print $2}')
    python scripts/save_result.py --task QA --dataset SQuAD --metric "$metric" --value "$value"
done

echo "[Done] Results saved to results.csv"
