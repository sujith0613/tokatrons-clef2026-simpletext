# Tokatrons at CLEF 2026 SimpleText Task 1 — Full Paper Details

## 1. Paper Metadata

- **Title**: Tokatrons at CLEF 2026 SimpleText Task 1: Plan-Guided BART and Zero-Shot LLM Approaches to Biomedical Text Simplification
- **Venue**: CLEF 2026 Working Notes (CEUR-WS)
- **Task**: SimpleText Task 1 — Sentence-level biomedical text simplification
- **Team**: Tokatrons
- **Affiliation**: Sri Sivasubramaniya Nagar College of Engineering, Chennai

## 2. Author List

1. Sujith M (lead author, implementation, training, inference)
2. Varghese K James (co-author, analysis, paper writing)
3. Sree Krishna S (co-author, data processing, evaluation)
4. Prabavathy Balasundaram (advisor, supervision)

Affiliation for all: Department of Computer Science and Engineering, Sri Sivasubramaniya Nagar College of Engineering, Chennai, India

## 3. Abstract (Draft)

This paper presents the Tokatrons team's participation in CLEF 2026 SimpleText Task 1, focusing on the automated simplification of biomedical texts at the sentence level. We explore three distinct approaches: (1) a fine-tuned BART-based sequence-to-sequence model with plan-guided training using explicit simplification operation labels; (2) a zero-shot large language model approach using LLaMA-3.1-8B with domain-specific prompting; and (3) a zero-shot approach using the more efficient LLaMA-4-Scout model. Our experiments reveal a significant trade-off between simplification quality and computational cost. The plan-guided BART model achieved an official test SARI score of 34.30, demonstrating the effectiveness of incorporating explicit plan labels into the training process. The zero-shot LLaMA-3.1-8B model achieved a superior validation SARI of 36.29, but its computational requirements (48,000+ Groq API calls) made it impractical for full test-set inference within our budget constraints. In contrast, the more efficient LLaMA-4-Scout model, while faster and cheaper, achieved only 17.92 SARI on the official test set, substantially underperforming both BART and LLaMA-8B. Our findings highlight that fine-tuned medium-sized models with structured training strategies remain competitive alternatives to large language models for text simplification tasks, especially when computational resources are constrained. We release our code, trained models, and plan-label dataset for reproducibility.

## 4. Dataset Details

### Source
- **Cochrane-auto**: Derived from Cochrane systematic reviews
- **Training pairs**: 11,510 (sentence, simplification) pairs
- **Validation set**: ~9,160 sentences (used for LLaMA-8B evaluation)
- **Official test set**: 48,809 sentences (official blind test set)

### Simplification Operation Labels (Plan Labels)
Generated using the alignment-based classifier from the SimpleText organizers' framework:

| Label     | Count   | Percentage |
|-----------|---------|------------|
| Rephrase  | 5,212   | 45.3%      |
| Delete    | 4,064   | 35.3%      |
| Copy      | 967     | 8.4%       |
| Merge     | 748     | 6.5%       |
| Split     | 519     | 4.5%       |

Labels are used as special tokens prepended to source sentences during plan-guided training (e.g., `<rephrase>`, `<delete>`, `<copy>`, `<merge>`, `<split>`).

### Planning Baseline
Target texts from which plan labels are derived:
- Full target available: 7,225 pairs (62.8%)
- Copy-only target: 967 pairs (8.4%) — label assigned `copy`
- Empty target: 3,318 pairs (28.8%) — label assigned `delete` (since the simplification removes the source content)

## 5. Model Architectures

### 5.1 BART (Fine-tuned, Plan-Guided)
- **Base model**: `facebook/bart-large-cnn` (~400M parameters)
- **Architecture**: Standard encoder-decoder transformer
- **Plan-guided variant**: Embedding layer extended with 5 special plan tokens (`<rephrase>`, `<delete>`, `<copy>`, `<merge>`, `<split>`)
- **Training device**: NVIDIA T4 GPU (16GB VRAM, Google Colab)
- **Inference device**: CPU (test set) — led to KeyboardInterrupt crash at checkpoint 20,704/48,809

#### Training Hyperparameters (v1 — first 3 epochs)
- Optimizer: AdamW
- Learning rate: 3e-5
- Weight decay: 0.01
- Epochs: 3
- Warmup ratio: 0.1
- Batch size: 8 (gradient accumulation steps: 2)
- Max source length: 512
- Max target length: 128
- FP16: True (mixed precision)
- Gradient clipping: 1.0
- Label smoothing: 0.1
- Random seed: 42

#### Plan-Guided Training (v2 — additional 2 epochs)
- Same hyperparameters as v1
- Added special tokens to tokenizer
- Resized token embeddings
- Training resumed from v1 checkpoint (`/content/drive/MyDrive/simpletext/bart_finetuned_simpletext`)
- Final model saved to: `/content/drive/MyDrive/simpletext/plan_guided_bart_simpletext`

#### Inference Hyperparameters (Grid Search)
Best configuration found via grid search on validation:
- num_beams: 2
- length_penalty: 1.0
- no_repeat_ngram_size: 0
- max_length: 128
- min_length: 1
- early_stopping: True

This configuration achieved **oracle SARI 35.86** on validation (upper bound of inference tuning).

### 5.2 LLaMA-3.1-8B (Zero-Shot)
- **Model**: `llama-3.1-8b-instant` (via Groq API)
- **Parameters**: ~8B
- **Inference**: Zero-shot, no fine-tuning
- **Prompt strategy**: Domain-specific system + user prompt
- **Validation**: 9,160 sentences (subset, due to API rate limiting)
- **Test**: NOT submitted — budget insufficient for 48,809 sentences at Groq API rates

#### Prompt Template
```
System: You are a helpful assistant that simplifies complex biomedical sentences for a general audience. Break down complex medical terminology into simpler language while preserving the core meaning. Make the text accessible to readers without specialized medical knowledge.

User: {source_sentence}
```

#### Inference Configuration
- Temperature: 0.3 (increased to 0.7 if output identical to source — retry logic)
- Top-p: 0.9
- Max tokens: 128
- Groq API key: [REDACTED — replaced with placeholder in notebooks]
- **WARNING**: API key is exposed in notebook — must be revoked before publication
- API throughput: limited by Groq free-tier rate limits

### 5.3 LLaMA-4-Scout (Zero-Shot, Efficient)
- **Model**: LLaMA-4-Scout (via Groq API)
- **Parameters**: ~17B (mixture of experts)
- **Inference**: Zero-shot, 10 parallel workers
- **Test**: Submitted to CodaBench (48,809 sentences)
- **Rationale**: Chosen for faster/cheaper API calls compared to LLaMA-8B

#### Inference Configuration
- Temperature: 0.3
- Top-p: 0.9
- Max tokens: 128
- Parallel workers: 10 (threading-based concurrent Groq API calls)
- Total runtime: ~3 hours on Colab T4 + Groq API

## 6. Label Classifier (RoBERTa-base)

- **Purpose**: Predict simplification operation label at inference time for plan-guided BART
- **Model**: `roberta-base` (~125M parameters)
- **Training**: Fine-tuned on the plan-label dataset (11,510 training samples)
- **Training device**: T4 GPU (Google Colab)
- **Inference device**: CPU (test set)
- **Accuracy**: ~52% (5-class classification — key bottleneck in pipeline)

#### Training Hyperparameters (Label Classifier)
- Optimizer: AdamW
- Learning rate: 2e-5
- Epochs: 3
- Batch size: 16
- Max sequence length: 256
- Warmup steps: 500

#### Label Mapping
```
{0: '<copy>', 1: '<delete>', 2: '<merge>', 3: '<rephrase>', 4: '<split>'}
```

## 7. Evaluation Results

### 7.1 Validation Set Results

| Metric             | BART v2 (Plan-Guided) | LLaMA-3.1-8B (Zero-Shot) |
|--------------------|-----------------------|---------------------------|
| SARI               | 33.23                 | 36.29                     |
| BLEU               | 6.89                  | 2.21                      |
| BERTScore          | 0.634                 | 0.610                     |
| FKGL               | 16.00                 | 11.31                     |
| Compression Ratio  | 2.85                  | 1.18                      |
| Deletion Proportion| 0.073                 | 0.337                     |
| Identical to Source| 0.005                 | 0.000                     |

Note: LLaMA-8B evaluated on 9,160 validation sentences (not the full validation set due to Groq API rate limits).

### 7.2 Official Test Set Results (CodaBench)

| Submission                          | SARI  | BLEU  | BERTScore | FKGL | Compression | Readability | Timestamp            |
|-------------------------------------|-------|-------|-----------|------|-------------|-------------|----------------------|
| tokatrons_task11_BART_20261.zip     | 34.30 | 2.10  | 0.622     | 16.35| 2.18        | 6.12        | 2026-06-01 22:45:06  |
| tokatrons_task11_LLM.zip            | 17.92 | 2.29  | 0.510     | 12.03| 1.00        | 4.72        | 2026-06-01 23:35:16  |
| tokatrons_task11_LLaMA8B_val.zip    | —     | —     | —         | —    | —           | —           | 2026-05-31 21:48:12  |

Note: LLaMA-8B submission failed (status code 421 on CodaBench). Only BART v2 (34.30) and LLaMA-4-Scout (17.92) have official test scores.

### 7.3 SARI Progression Over Training

Mentioned in SimpleText_StatusReport.docx:
- BART v1 (epoch 1–3): Final SARI **26.37** (standard fine-tune, no plan tokens)
- BART v2 (epoch 4–5, plan-guided): SARI improves to **33.23** with predicted plan labels
- Oracle validation SARI (gold labels + best inference config): **35.86**
- Official test SARI (BART v2): **34.30**

### 7.4 CodaBench Submission History

From CodaBench console (scraped):
1. **`tokatrons_task11_BART_20261.zip`** — Status: Finished, SARI: 34.30, Submitted: 2026-06-01 22:33:40, Finished: 2026-06-01 22:45:06
2. **`tokatrons_task11_LLM.zip`** — Status: Finished, SARI: 17.92, Submitted: 2026-06-01 23:25:18, Finished: 2026-06-01 23:35:16
3. **`tokatrons_task11_LLaMA8B_val.zip`** — Status: Created, Submitted: 2026-05-31 21:48:12 (failed — status code 421)

## 8. Error Analysis

### 8.1 BART v2 Failures
- **Over-compression**: FKGL 16.00 (worse than source FKGL 13.03) — model produces dense, jargon-heavy output
- **Plan classifier bottleneck**: RoBERTa label classifier only 52% accurate — wrong plan labels lead to incorrect simplification operations
- **Identical output**: 0.5% of outputs identical to source (model sometimes copies when it should simplify)
- **Low deletion**: Only 7.3% deletion proportion — model retains information it should remove
- **Training/inference mismatch**: Plan-guided training uses gold labels, but inference uses predicted labels

### 8.2 LLaMA-8B Failures
- **Low BLEU**: Only 2.21 (too aggressive with paraphrasing vs. source)
- **Low BERTScore**: 0.610 (semantic drift — model adds information not in source)
- **Over-deletion**: 33.7% of tokens deleted (model removes too much information)
- **API cost prohibitive**: ~$0.27/1M tokens input, ~$1.10/1M tokens output (Groq paid tier estimates) — 48,809 sentences × avg 120 tokens ≈ 5.9M tokens → $1.59–$6.49 per full test pass
- **Rate limited**: Free-tier Groq allows ~30 requests/minute — ~27 hours for full test set
- **Temperature sensitivity**: 0.3 good for most, but some sentences require 0.7 to avoid copying

### 8.3 LLaMA-4-Scout Failures
- **Poor SARI**: 17.92 (worst of all approaches)
- **Poor BERTScore**: 0.510 (significant semantic drift)
- **Compression ratio**: 1.00 (essentially no simplification — output length ~= input length)
- **Model too general**: LLaMA-4-Scout is optimized for general chat, not domain-specific simplification
- **MoE routing**: Mixture-of-experts architecture may route biomedical tokens to suboptimal experts

## 9. Three-Act Narrative Structure

### Act 1: BART Fine-Tuning Hits a Ceiling
- Start with BART-large-cnn as baseline
- Fine-tune 3 epochs → SARI improves steadily
- Add plan-guided training (2 more epochs) → further improvement
- Peak: **BART v2 validation SARI 33.23**, official test SARI **34.30**
- Best inference tuning gives oracle SARI **35.86** (upper bound)
- Limitation: FKGL 16.00 (does not actually simplify readability), plan classifier 52% accuracy

### Act 2: Zero-Shot LLaMA-8B Beats BART
- Switch to LLaMA-3.1-8B via Groq API
- Zero-shot with domain-specific prompting
- Validation SARI **36.29** — beats BART's oracle 35.86!
- FKGL **11.31** — genuinely simplifies readability from source 13.03
- Problem: Budget insufficient for 48,809 test sentences
- CodaBench submission attempt fails (status 421)

### Act 3: LLaMA-4-Scout (The Pragmatic Bet That Failed)
- Switch to LLaMA-4-Scout for speed and cost
- 10 parallel workers, ~3 hours total
- Official test SARI: **17.92** — catastrophic underperformance
- Lesson: Bigger/faster is not better; domain alignment matters more

## 10. Key Conclusions

1. **Plan-guided BART is the most practical solution**: Achieved 34.30 SARI on official test, fine-tuned on free Colab T4 GPU, no API costs.

2. **LLaMA-8B is the best-quality solution**: Validation SARI 36.29 beats BART by +3.06 points, but API cost and rate limits prevented full test submission.

3. **LLaMA-4-Scout is not suitable**: 17.92 SARI is well below both alternatives; MoE architecture may not transfer well to biomedical text simplification.

4. **FKGL is a critical failure mode**: BART degrades readability (16.00 from 13.03) while LLaMA-8B improves it (11.31). Future work must directly optimize for readability metrics.

5. **Plan classifier accuracy is the bottleneck**: The 52% RoBERTa classifier means nearly half of plan labels are wrong, cascading into incorrect BART outputs.

6. **Cost-quality tradeoff is steep**: LLaMA-8B costs $0 (Groq free tier) to $1.59-$6.49 (paid) per test pass; BART costs only inference compute (~$0.01 on CPU for ~1-2 hours).

## 11. Code and Model Reproducibility

### Notebooks Location
All notebooks in `colab files/`:

| File | Purpose |
|------|---------|
| `BART_Training.ipynb` | BART v1 (3 epochs) + v2 plan-guided (2 epochs) training, validation, inference |
| `LLaMA8B_Evaluation.ipynb` | Master setup + Groq LLaMA-3.1-8B validation pipeline + metrics comparison |
| `LLaMA8B_Submission.ipynb` | LLaMA-8B full submission (9,160 sentences via Groq API) |
| `LLaMA4Scout_Submission.ipynb` | LLaMA-4-Scout test inference with 10 parallel workers (48,809 sentences) |
| `BART_TestInference.ipynb` | BART test set inference on CPU (crashed at ~21K/48,809) |

### Trained Model Weights (Google Drive)
- `/content/drive/MyDrive/simpletext/bart_finetuned_simpletext` — BART v1 checkpoint
- `/content/drive/MyDrive/simpletext/plan_guided_bart_simpletext` — BART v2 plan-guided checkpoint
- `/content/drive/MyDrive/simpletext/label_classifier` — RoBERTa label classifier

### Data Files
- `/content/drive/MyDrive/simpletext/train.json` — Training set (11,510 pairs with plan labels)
- `/content/drive/MyDrive/simpletext/val.json` — Validation set (~1,130 pairs)
- `/content/drive/MyDrive/simpletext/test.json` — Test set (48,809 sentences)

### Dependencies
```python
# Core
transformers==4.44.0
torch==2.3.0
datasets==2.19.0

# Evaluation
sacrebleu==2.4.0
bert_score==0.3.13
textstat==0.7.3

# Inference
groq==0.9.0

# Utilities
pandas==2.1.4
numpy==1.25.2
tqdm==4.66.1
accelerate==0.30.0
```

### Security Note
The Groq API key was exposed in plaintext in `Untitled0 (1).ipynb` and `Untitled10.ipynb`. It has been replaced with a placeholder. The key must be revoked at console.groq.com before any public release of the code.

## 12. Tables for the Paper

### Table 1: Dataset Plan Label Distribution
```
Label       Count    Percentage
Rephrase    5,212    45.3%
Delete      4,064    35.3%
Copy          967     8.4%
Merge         748     6.5%
Split         519     4.5%
Total      11,510   100.0%
```

### Table 2: Validation Set Comparison
```
Metric              BART v2    LLaMA-8B
SARI                33.23      36.29
BLEU                 6.89       2.21
BERTScore            0.634      0.610
FKGL                16.00      11.31
Compression Ratio    2.85       1.18
Deletion Prop.       0.073      0.337
Identical to Source  0.005      0.000
```

### Table 3: Official Test Set (CodaBench)
```
Submission              SARI    BLEU   BERTScore  FKGL   Comp.   Read.
BART v2                 34.30   2.10   0.622      16.35  2.18    6.12
LLaMA-4-Scout           17.92   2.29   0.510      12.03  1.00    4.72
```

### Table 4: Inference Tuning Grid Search (BART v2)
```
num_beams   length_penalty   no_repeat_ngram   SARI (oracle)
1           0.6              0                 34.12
2           1.0              0                 35.86  ← best
3           1.0              2                 35.21
4           1.0              3                 34.98
5           0.8              0                 34.67
```

### Table 5: Groq API Cost Estimates for Full Test Set
```
Model              Cost per 1M inp.   Cost per 1M outp.   Est. total cost (48,809 sents)
LLaMA-3.1-8B       $0.27              $1.10               $1.59–$6.49
LLaMA-4-Scout      $0.15              $0.60               $0.88–$3.54
```
