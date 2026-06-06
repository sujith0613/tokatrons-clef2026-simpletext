# Memory — Session Tracking

## Latest Session (2026-06-06)
**Objective**: Finalize paper — fix remaining issues, add hardcoded rephrase hypothesis, create Colab scripts for dataset stats and qualitative examples.

### Changes Made
- **paper/paper.tex**: 
  - Author order: Sujith M → Sree Krishna S → Varghese K James → Prabavathy Balasundaram
  - CPU → T4 GPU in §6 ($\S$6)
  - LLaMA-4 model string: `meta-llama/llama-4-scout-17b-16e-instruct` ($\S$5.3)
  - Hardcoded rephrase hypothesis + greedy decoding insight added to $\S$8.1 BART Failure Modes
- **doc/related_work_analysis.txt**: Added $\S$3.5 Hardcoded Rephrase Hypothesis section
- **doc/author_review_list.md**: Updated with all resolved items, added items 8-9 action items
- **sources/colab files/dataset_statistics.ipynb**: New Colab script for training set statistics
- **sources/colab files/qualitative_examples.py**: New extraction script for qualitative comparison table

### Key Discoveries
- Test SARI (34.30) > validation SARI (33.23) explained by hardcoded rephrase hypothesis: eliminating 48% classifier error cascade + greedy decoding boost
- Gold labels during training, hardcoded rephrase during test = no classifier errors
- This changes the interpretation of the 34.30 test score — not directly comparable to 33.23 validation

### Pending
1. **Run dataset_statistics.ipynb** in Colab on actual training data → report back for $\S$4
2. **Run qualitative_examples.py** on merged JSONL output data → insert LaTeX table into $\S$8
3. **Revoke old Groq API key** at console.groq.com
4. **Install TeX distribution** (MiKTeX/TinyTeX) and compile `paper/paper.tex`
5. Sanitize Google Drive mount paths in notebooks for GitHub release
6. Register paper on CEUR-WS submission system before deadline

### File Inventory
| File | Status | Notes |
|------|--------|-------|
| `paper/paper.tex` | 640 lines, 10 sections | All known issues fixed; 2 pending (dataset stats table, qualitative examples) |
| `paper/paper.bib` | 18 references | All real, verified; LLaMA-4 fixed to blog URL |
| `doc/related_work_analysis.txt` | Updated | $\S$3.5 added (hardcoded rephrase) |
| `doc/author_review_list.md` | Updated | 2 action items remain (items 8, 9) |
| `sources/colab files/README.md` | Created | Notebook documentation |
| `sources/colab files/dataset_statistics.ipynb` | Created | Needs Colab run |
| `sources/colab files/qualitative_examples.py` | Created | Needs Colab run |
| `CLAUDE.md` | Split from memory.md | Canonical entry point |

### Decision Log
- Hardcoded rephrase hypothesis is included as analysis in $\S$8.1, not as established fact
- Greedy decoding noted as secondary contributor to test-validation SARI gap
- Author review list updated with action items 8-9 as "RESOLVED" (scripts created) with user action still required
