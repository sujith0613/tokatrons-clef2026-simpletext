# Author Review Checklist — Items Needing Clarification

Before final submission, the following items need author input to ensure accuracy.

## Must Clarify

### 1. BART Test Inference (How was 34.30 SARI produced?)
- **Evidence**: `BART_TestInference.ipynb` shows inference crashed at ~21K/48,809 (KeyboardInterrupt).
- **Clarification received**: The 34.30 SARI score was **provided by the CodaBench evaluation platform** (evaluator's website), not computed locally.
- **Clarification received**: Successful run was on **T4 GPU** (not CPU).
- **Remaining question**: How was the successful inference run completed? Was it with or without the RoBERTa classifier? The notebook doesn't record it. The crashed notebook hardcoded `[REPHRASE]` for all sentences — did the successful run do the same?

### 2. BART v1 SARI in Table 2 — RESOLVED
- **Resolution**: v1 SARI (26.37) added to §7.1 prose and §9.2 narrative. Table 2 keeps v2 vs LLaMA-8B only (no full v1 metrics available for all columns). **No action needed.**

### 3. Classifier: DistilBERT vs RoBERTa — RESOLVED
- **Evidence**: `BART_Training.ipynb` reveals 3-stage evolution:
  1. DistilBERT (initial experiment)
  2. **RoBERTa-base** (trained to replace DistilBERT, best accuracy 52.6%)
  3. DeBERTa (exploratory, optional)
- **Final**: RoBERTa is correct. Paper already says RoBERTa. **No action needed.**

### 4. Random Seed — RESOLVED
- Seed 42 confirmed in notebook. Paper already updated. **No action needed.**

### 5. LLaMA-4-Scout Model Version — RESOLVED
- **Exact model**: `meta-llama/llama-4-scout-17b-16e-instruct` confirmed from notebook code.
- Paper updated with exact model string in §5.3. **No action needed.**

### 6. BART submission ZIP generation
- **Clarification received**: The BART v2 predictions were submitted as `tokatrons_task11_BART_20261.zip` to CodaBench. The 34.30 SARI was computed by the CodaBench evaluation platform.
- **Remaining question**: Was there a separate notebook/script that generated `tokatrons_task11_BART_20261.zip` (the final submission ZIP), or was it generated inside `BART_Training.ipynb`? The ZIP notebook was not preserved.

## Clarified Items

### 7. Classifier Accuracy — RESOLVED
- `compute_metrics` in the notebook uses `(preds == labels).mean()` = **flat accuracy**
- Best epoch: **epoch 4 → 52.6%** on 1,472 validation samples
- Random baseline: 45.3% (predict majority class "rephrase")
- Paper says "52% accuracy" — this is correct as flat accuracy

### 8. Dataset Statistics — RESOLVED
- A Colab script (`dataset_statistics.ipynb`) has been created in `sources/colab files/` for computing training set token/char statistics.
- **Action required**: Run the Colab script on the actual SimpleText training data and report outputs for inclusion in §4.

### 9. Qualitative Examples — RESOLVED
- A Python script (`qualitative_examples.py`) has been created in `sources/colab files/` for extracting 3 representative examples (short, medium, long) from system output data.
- **Action required**: Run the script on the merged JSONL data and update `paper.tex` with the resulting LaTeX table.

## Items Already Fixed (No Action Needed)
- ~~LLaMA-4 arXiv ID placeholder~~ → Fixed to Meta blog URL
- ~~Classifier accuracy~~ → Confirmed 52.6% flat accuracy, paper states "52%"
- ~~FKGL provenance~~ → Clarified as "computed on the validation set"
- ~~BART inference timing~~ → Removed unverifiable timing claim
- ~~Random seed~~ → Added seed=42 to hyperparameter table
- ~~v1 SARI~~ → Added to validation results and three-act narrative
- ~~Author order~~ → Swapped: Sujith M, Sree Krishna S, Varghese K James, Prabavathy Balasundaram
- ~~CPU → T4 GPU~~ → Updated §6
- ~~LLaMA-4 model string~~ → Added to §5.3
- ~~Hardcoded rephrase hypothesis~~ → Added to §8.1
