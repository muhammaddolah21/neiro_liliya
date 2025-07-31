# UniLM Fine-tuning Pipeline (Reproducible, for University)

## Описание

Воспроизведение пайплайна fine-tuning для UniLM по статье:
[Unified Language Model Pre-training for Natural Language Understanding and Generation](https://arxiv.org/abs/1905.03197)

Исходный код UniLM: [https://github.com/microsoft/unilm](https://github.com/microsoft/unilm)

- Используется готовая (pretrained) модель UniLM
- Fine-tuning на всех downstream задачах из статьи: Summarization, Question Generation, Question Answering
- Используются те же датасеты: CNN/DM, SQuAD, DUC
- Все этапы автоматизированы: подготовка данных, обучение, инференс, оценка, сохранение результатов
- Результаты оформляются в таблицу, как в статье
- Поддержка запуска на кластере (HTCondor)

---

## Структура проекта

```
configs/           # yaml-конфиги экспериментов
scripts/           # скрипты для подготовки, оценки, сохранения результатов
models/            # код модели, чекпоинты
run_pipeline.sh    # универсальный bash-скрипт для запуска пайплайна
Cluster-run-project.md # инструкция для кластера
README.md          # этот файл

# Данные
/data/squad/       # SQuAD (QA, QG)
/data/cnn_dm/      # CNN/DM (summarization)
/data/duc/         # DUC (summarization)
```

---

## Быстрый старт

1. **Подготовьте окружение**
   - Python 3.10+
   - Установите зависимости: `pip install -r requirements.txt`

2. **Запустите пайплайн**
   ```bash
   bash run_pipeline.sh --task qa --dataset squad --mode qa
   bash run_pipeline.sh --task summarization --dataset cnn_dm
   bash run_pipeline.sh --task summarization --dataset duc
   bash run_pipeline.sh --task qg --dataset squad --mode qg
   ```
   Все результаты будут автоматически сохранены в results.csv

3. **Запуск на кластере**
   - См. инструкцию в `Cluster-run-project.md`

---

## Ссылки
- [Статья UniLM (arXiv)](https://arxiv.org/abs/1905.03197)
- [GitHub UniLM](https://github.com/microsoft/unilm)

---

## Контакты
- Автор пайплайна: Lili, Андрей
- Для вопросов и поддержки: [ваш email или Telegram]
