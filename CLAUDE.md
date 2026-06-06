# Tokatrons CLEF 2026 SimpleText Task 1 — Paper Project

## Quick Overview
This project contains a research-publishing-grade CLEF 2026 Working Notes paper for SimpleText Task 1 (biomedical text simplification). The Team Tokatrons (Sri Sivasubramaniya Nagar College of Engineering, Chennai) explored three approaches: plan-guided BART (34.30 SARI), zero-shot LLaMA-3.1-8B (36.29 val), and zero-shot LLaMA-4-Scout (17.92 — failed). Paper follows three-act narrative: BART ceiling → LLaMA-8B surpasses but can't scale → LLaMA-4-Scout fails.

## File Structure
```
cleftask/
├── CLAUDE.md              ← THIS FILE — entry point for new agents
├── report.md              ← Complete paper details (models, results, tables, error analysis)
├── preferences.md         ← Title, authors, template, narrative decisions
├── memory.md              ← Session tracking, decision log, action items
├── .gitignore
├── paper/
│   ├── paper.tex          ← LaTeX paper (10 sections, 645 lines)
│   └── paper.bib          ← 18 references (all real, verified citations)
├── sources/
│   └── (original PDFs, DOCX, notebooks, ZIP)
│   └── colab files/
│       ├── BART_Training.ipynb
│       ├── LLaMA8B_Evaluation.ipynb
│       ├── LLaMA8B_Submission.ipynb
│       ├── LLaMA4Scout_Submission.ipynb
│       ├── BART_TestInference.ipynb
│       ├── README.md
│       ├── dataset_statistics.ipynb    ← run in Colab for §4 stats
│       └── qualitative_examples.py    ← extract examples for §8
├── doc/
│   ├── related_work_analysis.txt
│   └── author_review_list.md
└── tokatrons_task11_LLaMA8B_val/
    └── tokatrons_task11_LLaMA8B_val.json    ← LLaMA-8B validation output
```

## Key Facts (Condensed)
- **Primary result**: BART v2 plan-guided → **34.30 SARI** (official test, main submission)
- **BART v1 (standard FT)**: **26.37 SARI** (validation) — formerly unreported
- **Best validation**: LLaMA-3.1-8B zero-shot → **36.29 SARI** (not submitted — API cost)
- **Failed**: LLaMA-4-Scout zero-shot → **17.92 SARI** (MoE misalignment)
- **Label classifier**: **RoBERTa** (NOT DistilBERT — 3-stage evolution: DistilBERT → RoBERTa → DeBERTa)
- **Classifier accuracy**: 52.6% flat accuracy (barely above 45.3% majority-class baseline)
- **Training seed**: 42
- **Source FKGL**: 13.03 (computed on 9,160-sentence validation set)
- **Validation set**: 9,160 sentences (SimpleText 2025 test set, reused as 2026 validation split)
- **Test set**: 48,809 sentences
- **Team order**: Sujith M (1st), Sree Krishna S (2nd), Varghese K James (3rd), Prabavathy Balasundaram (advisor)
- **Venue**: CLEF 2026 Working Notes (CEUR-WS, ceurart.cls template)
- **License**: CC BY 4.0 (required), includes Generative AI disclosure
- **Hardcoded rephrase hypothesis**: Test SARI (34.30) > validation SARI (33.23) explained by eliminating 48% classifier error cascade + greedy decoding boost — added to §8.1

## Paper Structure (10 sections)
1. Introduction
2. Related Work (UZH Pandas, USM AIIR, DS@GT, encoder-decoder vs decoder-only)
3. Task Description
4. Dataset (Cochrane-auto, 11,510 pairs, plan label distribution)
5. Methods (BART plan-guided, LLaMA-8B, LLaMA-4-Scout)
6. Experimental Setup
7. Results (v1: 26.37, v2: 33.23, LLaMA-8B: 36.29 val; test: 34.30 vs 17.92)
8. Error Analysis (FKGL degradation, plan classifier bottleneck, hardcoded rephrase hypothesis, MoE failure)
9. Discussion (architectural analysis, three-act narrative, cost-quality, prior work)
10. Conclusion

## Where to Find Detailed Info
| Topic | File |
|-------|------|
| Full paper details (hyperparams, tables, scores) | `report.md` |
| Preferences (title, template, author order) | `preferences.md` |
| Session history, decisions, action items | `memory.md` |
| Winning paper research + real citations | `doc/related_work_analysis.txt` |
| Author clarification items | `doc/author_review_list.md` |
| LaTeX paper | `paper/paper.tex` |
| Bibliography | `paper/paper.bib` |
| GitHub repository | https://github.com/sujith0613/tokatrons-clef2026-simpletext |

## GitHub Repo
- **URL**: https://github.com/sujith0613/tokatrons-clef2026-simpletext
- Created with `gh repo create`, pushed from local `E:\Desktop\SSN\cleftask`
- Contains paper, notebooks, validation outputs, docs — 26 files in initial commit

## Current State
- Paper written: 10 sections, ~645 lines, research publishing grade
- All known factual issues fixed: author order, classifier (RoBERTa), v1 SARI, seed, FKGL provenance, CPU→T4 GPU, LLaMA-4 model string, hardcoded rephrase hypothesis, error cascade wording, FRE metric, repo URL
- Dataset statistics added to §4.1: token lengths, vocab sizes, compression ratio, empty targets
- Real citations from published proceedings (Michail+2024, Largey+2024, Marturi+2025)
- API keys sanitized (4 real keys replaced with placeholder across 2 notebooks)
- GitHub repo created and pushed with 2 commits

## Pending Action Items
1. ~~**Run `dataset_statistics.ipynb`** in Colab on training data → report stats for §4~~ ✅ DONE
2. **Run `qualitative_examples.py`** on merged JSONL output → insert LaTeX table into §8
3. **Revoke old Groq API keys** at console.groq.com (4 real keys were exposed across 2 notebooks — user must revoke all)
4. Install TeX distribution (MiKTeX/TinyTeX) and compile `paper/paper.tex` to verify
5. Sanitize Google Drive mount paths in notebooks for GitHub release
6. Final proofread and address any reviewer feedback
7. Register paper on CEUR-WS submission system before deadline
8. Get ORCIDs from teammates' papers and update author block
