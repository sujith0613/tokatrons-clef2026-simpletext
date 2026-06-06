# Colab Notebooks — Tokatrons CLEF 2026 SimpleText Task 1

Five notebooks used for training, evaluation, and submission. Each notebook now has a Markdown header (cell 0) with its purpose and key details.

---

## Notebook Overview

| # | File | Purpose | Data | Key Scores | Status |
|---|------|---------|------|------------|--------|
| 1 | `BART_Training.ipynb` | BART v1+v2 training, validation, grid search, RoBERTa classifier | Cochrane-auto train (11,510) + val (1,472) | v1: 26.37, v2: 33.23, oracle: 35.86 | ✅ Complete |
| 2 | `LLaMA8B_Submission.ipynb` | LLaMA-3.1-8B generation via Groq API (9,160 sentences) | 2025 test set (2026 val split) | 36.29 (in #3) | ✅ Complete |
| 3 | `LLaMA8B_Evaluation.ipynb` | SARI/BLEU/BERTScore/FKGL comparison: BART v2 vs LLaMA-8B | Same 9,160 sentences | SARI 36.29 vs 33.23 | ✅ Complete |
| 4 | `LLaMA4Scout_Submission.ipynb` | LLaMA-4-Scout generation via Groq API (48,809 sentences, 10 workers) | 2026 official test set | 17.92 (CodaBench) | ✅ Complete |
| 5 | `BART_TestInference.ipynb` | BART v2 inference on test set (CPU, greedy decoding) | 2026 official test set (48,809) | 34.30 (separate run) | ❌ Interrupted |

---

## Data Flow

```
Cochrane-auto (11,510 train + 1,472 val)
  └─→ BART_Training.ipynb
       ├─→ v1: 26.37 SARI (standard fine-tune, 3 epochs)
       └─→ v2: 33.23 SARI (plan-guided, 2 more epochs)
                └─→ Inference tuning → oracle 35.86 SARI

2025 test set (9,160 sentences, reused as 2026 validation)
  ├─→ LLaMA8B_Submission.ipynb → LLaMA8B_Evaluation.ipynb → 36.29 SARI
  └─→ BART_Training.ipynb → 33.23 SARI (v2 with predicted labels)

2026 official test set (48,809 sentences)
  ├─→ BART_TestInference.ipynb → ❌ CRASHED at ~21K (CPU, greedy)
  │     └─→ Submitted via separate run → CodaBench: 34.30 SARI
  └─→ LLaMA4Scout_Submission.ipynb → CodaBench: 17.92 SARI
```

---

## Label Classifier Evolution

The BART pipeline uses a plan label classifier to predict simplification operations. It went through 3 iterations:

| Iteration | Model | Epochs | Best Accuracy | Used? |
|-----------|-------|--------|--------------|-------|
| 1 | DistilBERT | — | — | Initial experiment |
| 2 | **RoBERTa-base** | 5 | **52.6%** (flat, epoch 4) | ✅ Final classifier |
| 3 | DeBERTa | — | — | Exploratory (not used) |

Accuracy is flat (not weighted/macro), computed as `(preds == labels).mean()` on 1,472 validation samples. Random baseline: 45.3% (majority class "rephrase").

---

## Dependencies

### Python Packages
- `transformers==4.44.0` — BART, DistilBERT, RoBERTa, DeBERTa
- `torch==2.3.0` — GPU training
- `datasets==2.19.0` — HuggingFace datasets
- `sacrebleu==2.4.0` — BLEU
- `bert_score==0.3.13` — BERTScore
- `textstat==0.7.3` — FKGL
- `easse` (GitHub: feralvam/easse) — SARI
- `groq==0.9.0` — Groq API client
- `sentencepiece` — tokenization
- `pandas`, `numpy`, `json`, `zipfile` — data handling

### Hardware
- **Training**: NVIDIA T4 GPU (16GB VRAM, Google Colab)
- **LLaMA inference**: Groq API (no local GPU needed)
- **BART test inference**: CPU attempt failed; successful run likely used T4 GPU

### API Keys
- **Groq API**: Required for LLaMA-8B and LLaMA-4-Scout notebooks (`os.environ["GROQ_API_KEY"]`)
- **HuggingFace token**: Required for BART_Training.ipynb (`userdata.get('HF_TOKEN')`)

---

## Execution Order (Recommended)

```
Step 1: BART_Training.ipynb          # Train model + classifier (~5h on T4)
Step 2: LLaMA8B_Submission.ipynb     # Generate LLaMA-8B outputs (~5h API)
Step 3: LLaMA8B_Evaluation.ipynb     # Compare BART vs LLaMA (~10min)
Step 4: LLaMA4Scout_Submission.ipynb # Generate LLaMA-4 outputs (~3h API)
Step 5: BART_TestInference.ipynb     # Run on GPU (not CPU!) (~30min on T4)
```

---

## Google Drive Paths (Sanitize Before Publishing)

Notebooks reference the following Google Drive paths:
- `/content/drive/MyDrive/SimpleText2025/` — main data directory
- `/content/drive/MyDrive/simpletext/` — model checkpoints
- `/content/drive/MyDrive/SimpleText2025/models/` — classifier checkpoints

Replace with local paths or environment variables before GitHub release.
