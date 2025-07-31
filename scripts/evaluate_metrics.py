# Универсальный скрипт для автоматической оценки метрик
# Поддерживает ROUGE, BLEU, METEOR, EM, F1 для summarization, QG, QA

import argparse
from collections import Counter
from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f]

def exact_match(pred, ref):
    return int(pred.strip() == ref.strip())

def f1_score(pred, ref):
    pred_tokens = pred.split()
    ref_tokens = ref.split()
    common = Counter(pred_tokens) & Counter(ref_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0
    precision = num_same / len(pred_tokens)
    recall = num_same / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred', required=True, help='Файл с предсказаниями')
    parser.add_argument('--ref', required=True, help='Файл с референсами')
    args = parser.parse_args()

    preds = read_lines(args.pred)
    refs = read_lines(args.ref)
    assert len(preds) == len(refs), 'Число предсказаний и референсов не совпадает!'

    # ROUGE
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge1, rouge2, rougel = [], [], []
    for p, r in zip(preds, refs):
        scores = scorer.score(r, p)
        rouge1.append(scores['rouge1'].fmeasure)
        rouge2.append(scores['rouge2'].fmeasure)
        rougel.append(scores['rougeL'].fmeasure)
    print(f'ROUGE-1: {sum(rouge1)/len(rouge1):.4f}')
    print(f'ROUGE-2: {sum(rouge2)/len(rouge2):.4f}')
    print(f'ROUGE-L: {sum(rougel)/len(rougel):.4f}')

    # BLEU
    bleu = corpus_bleu([[r.split()] for r in refs], [p.split() for p in preds], smoothing_function=SmoothingFunction().method1)
    print(f'BLEU: {bleu:.4f}')

    # METEOR
    meteor = sum(meteor_score([r], p) for p, r in zip(preds, refs)) / len(preds)
    print(f'METEOR: {meteor:.4f}')

    # EM, F1 (для QA)
    em = sum(exact_match(p, r) for p, r in zip(preds, refs)) / len(preds)
    f1 = sum(f1_score(p, r) for p, r in zip(preds, refs)) / len(preds)
    print(f'Exact Match: {em:.4f}')
    print(f'F1: {f1:.4f}')

if __name__ == '__main__':
    main()
