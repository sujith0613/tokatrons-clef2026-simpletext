# Tokatrons at CLEF 2026 SimpleText Task 1

**Plan-Guided BART and Zero-Shot LLM Approaches to Biomedical Text Simplification**

CLEF 2026 Working Note — SimpleText Lab: Task 1.1 (Sentence-level Text Simplification)

**Authors:** Sujith M, Sree Krishna S, Varghese K James, Prabavathy Balasundaram

*Sri Sivasubramaniya SSN College of Engineering, Chennai, India*

## Abstract

This paper presents the Tokatrons team submissions to the CLEF 2026 SimpleText Task 1. We investigate three approaches: (1) a fine-tuned BART model with plan-guided training (34.30 SARI), (2) zero-shot LLaMA-3.1-8B via Groq API (36.29 SARI on validation), and (3) zero-shot LLaMA-4-Scout-17B via Groq API (17.92 SARI). Our best BART model achieves competitive performance through structured training strategies.

## Repository Structure

```
paper/               — Camera-ready working note (LaTeX sources + PDF)
notebooks/           — Colab notebooks for training, inference, and submission
  ├── SimplyText.ipynb              — Plan-guided BART training + evaluation
  ├── FInalSubmissionSimpleText.ipynb — LLaMA-4-Scout zero-shot submission
  └── BartFinalTestSet.ipynb       — BART plan-guided inference
```

## Trained Models (Hugging Face Hub)

All models are hosted at `https://huggingface.co/winner0613`:

| Model | Description | Link |
|---|---|---|
| BART v1 — standard fine-tune | `tokatrons-bart-cochrane-11` (26.37 SARI) | [HF Hub](https://huggingface.co/winner0613/tokatrons-bart-cochrane-11) |
| BART v2 — plan-guided | `tokatrons-bart-plan-guided` **(34.30 SARI, main submission)** | [HF Hub](https://huggingface.co/winner0613/tokatrons-bart-plan-guided) |
| BART v3 — plan-guided extended | `tokatrons-bart-plan-guided-v3` (continued training) | [HF Hub](https://huggingface.co/winner0613/tokatrons-bart-plan-guided-v3) |
| RoBERTa plan classifier | `tokatrons-roberta-plan-classifier` (52% accuracy) | [HF Hub](https://huggingface.co/winner0613/tokatrons-roberta-plan-classifier) |
| DeBERTa-v3 plan classifier | `tokatrons-deberta-plan-classifier` (51.5%, experimental) | [HF Hub](https://huggingface.co/winner0613/tokatrons-deberta-plan-classifier) |
| DistilBERT plan classifier | `tokatrons-distilbert-plan-classifier` (initial attempt) | [HF Hub](https://huggingface.co/winner0613/tokatrons-distilbert-plan-classifier) |
| Balanced RoBERTa classifier | `tokatrons-roberta-balanced-classifier` (51.5%, experimental) | [HF Hub](https://huggingface.co/winner0613/tokatrons-roberta-balanced-classifier) |

## Citation

```bibtex
@inproceedings{tokatrons2026simpletext,
  title={SSN Tokatrons at the {CLEF} 2026 {SimpleText} Track: {Plan-Guided} {BART} and {Zero-Shot} {LLM} Approaches to Biomedical Text Simplification},
  author={Sujith, M. and Sree Krishna, S. and Varghese K. James and Prabavathy, B.},
  booktitle={CLEF 2026 Working Notes},
  year={2026},
  publisher={CEUR-WS.org}
}
```
