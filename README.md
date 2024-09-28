# Bio-RE-GPT

This repository is the official implementation of Bio-RE-GPT, a baseline model for [Bio-RFX](https://github.com/Tschal-rsa/bio-rfx).

**Bio-RFX: Refining Biomedical Extraction via Advanced Relation Classification and Structural Constraints**

## Setup

1. Python 3.11 (recommended)
2. `openai` (set your API key in `$OPENAI_API_KEY`)

## Datasets

Preprocessed datasets (in data/):

1. DrugVar
2. DrugVar-500
3. DrugVar-200
4. DrugProt
5. DrugProt-500
6. DrugProt-200
7. BC5CDR
8. CRAFT

## Prompting

```bash
python main.py DrugVar
```

The default model is `gpt-4`. If you want to try out `gpt-3.5-turbo`, please run:

```bash
python main.py DrugVar --model gpt-3.5-turbo
```

