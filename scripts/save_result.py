# Скрипт для автоматической генерации итоговой таблицы метрик (как в статье UniLM)
# Сохраняет результаты в results.csv

import argparse
import csv
from datetime import datetime

# Пример: task, dataset, metric, value, comment

def append_result(task, dataset, metric, value, comment=""):
    with open("results.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), task, dataset, metric, value, comment])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', required=True, help='Downstream task (summarization, QG, QA)')
    parser.add_argument('--dataset', required=True, help='Dataset name')
    parser.add_argument('--metric', required=True, help='Metric name (ROUGE-1, BLEU, EM, F1, etc)')
    parser.add_argument('--value', required=True, help='Metric value')
    parser.add_argument('--comment', default="", help='Optional comment')
    args = parser.parse_args()

    append_result(args.task, args.dataset, args.metric, args.value, args.comment)
    print(f"Result saved: {args.task}, {args.dataset}, {args.metric}, {args.value}")
