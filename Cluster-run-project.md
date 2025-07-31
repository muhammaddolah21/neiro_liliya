# Cluster Run Guide for UniLM Fine-Tuning Project

## 1. Debug Mode (Интерактивная отладка)

1. Создайте виртуальное окружение:
   ```bash
   python3 -m venv ~/virtualenvs/unilm_project
   ```
2. Активируйте окружение:
   ```bash
   source ~/virtualenvs/unilm_project/bin/activate
   ```
3. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/muhammaddolah21/neiro_liliya.git
   cd neiro_liliya
   ```
4. Установите зависимости:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Проверьте запуск на малом датасете:
   ```bash
   python data/squad/prepare_squad.py
   # или другой скрипт подготовки/обучения
   ```

## 2. Основной запуск (Batch Mode)

### Bash-скрипт для запуска (run_unilm_project.sh):
```bash
#!/bin/bash
# Переход в папку проекта
cd ~/projects/neiro_liliya
# Активация окружения
source ~/virtualenvs/unilm_project/bin/activate
# Установка зависимостей (если нужно)
pip install --upgrade pip
pip install -r requirements.txt
# Подготовка данных (пример)
python data/squad/prepare_squad.py
# Запуск обучения/инференса (пример)
python scripts/run_seq2seq.py --config configs/config_unilm.yaml
# Оценка метрик (пример)
python scripts/evaluate_metrics.py --pred predictions.txt --ref references.txt
```

### HTCondor .job-файл (unilm_project.job):
```
Universe        = vanilla
Executable      = /nethome/yourusername/scripts/run_unilm_project.sh
Log             = /nethome/yourusername/logs/unilm_project/run.$(ClusterId).log
Output          = /nethome/yourusername/logs/unilm_project/run.$(ClusterId).out
Error           = /nethome/yourusername/logs/unilm_project/run.$(ClusterId).err
request_cpus    = 4
request_memory  = 16GB
request_gpus    = 1
should_transfer_files = YES
queue
```

## 3. Советы
- Все пути и имена файлов можно менять под вашу структуру.
- Для автоматической оценки метрик используйте отдельный скрипт (evaluate_metrics.py), который считает ROUGE, BLEU, METEOR, EM, F1 и др.
- Для каждого даунстрим-таска используйте свой конфиг и свои данные.

## 4. Запуск
1. Сделайте bash-скрипт исполняемым:
   ```bash
   chmod +x ~/scripts/run_unilm_project.sh
   ```
2. Отправьте задачу в очередь:
   ```bash
   condor_submit ~/jobs/unilm_project.job
   ```

---

Если потребуется — добавлю шаблоны для SLURM, PBS или других систем. Для вопросов по автоматической оценке метрик и подготовке данных — пишите!
