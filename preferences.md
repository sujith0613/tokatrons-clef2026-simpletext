# User Preferences for CLEF 2026 SimpleText Paper

## Paper Preferences
- **Paper Title**: "Tokatrons at CLEF 2026 SimpleText Task 1: Plan-Guided BART and Zero-Shot LLM Approaches to Biomedical Text Simplification"
- **Title style**: Descriptive (option 1) — explicitly states methods and task
- **Venue**: CLEF 2026 Working Notes, published in CEUR-WS Proceedings
- **Paper type**: Conference Working Notes (not full conference proceedings)
- **Template**: CEUR-WS `ceurart.cls` (LaTeX)
- **Track**: SimpleText Task 1 (Sentence-Level Simplification)
- **Task**: SimpleText Task 1 only (not Task 1.2 on document-level)
- **Narrative structure**: Three-act story — BART ceiling → LLaMA-8B beats it → LLaMA-4-Scout fails
- **License**: CC BY 4.0 (required by CEUR-WS)
- **AI disclosure**: Required (CEUR-WS mandates Generative AI disclosure statement)

## Author List (Order Confirmed)
1. Sujith M — lead author, implementation, training, inference pipeline
2. Varghese K James — co-author, analysis, paper writing
3. Sree Krishna S — co-author, data processing, evaluation
4. Prabavathy Balasundaram — advisor, supervision (marked as such)

All authors at: Department of Computer Science and Engineering, Sri Sivasubramaniya Nagar College of Engineering, Chennai, India.

## Writing Preferences
- Collaborative: write section-by-section as markdown, then produce final LaTeX
- Research publishing grade: CLEF Working Notes quality level
- Include: model architecture details, hyperparameters, full evaluation results, error analysis
- Exclude: document-level simplification (Task 1.2), raw notebook code
- Cite: relevant prior SimpleText papers, BART, LLaMA, evaluation metrics references

## Template Specifications (CEUR-WS `ceurart.cls`)
- Document class: `\documentclass[twocolumn]{ceurart}`
- Required packages: `graphicx`, `booktabs`, `hyperref`, `natbib`
- Copyright block: included via `\copyrightclause`
- License: `\ccby`
- AI disclosure: separate paragraph before references
- Max length: ~8-10 pages (CEUR-WS typical)
- Bibliography: BibTeX, `plainurl` style

## Key Narrative Decisions
- Frame BART v2 as the primary submission (34.30 SARI is main result)
- Frame LLaMA-8B as "validation oracle" that couldn't scale to test
- Frame LLaMA-4-Scout as cautionary tale about model-task misalignment
- Acknowledge FKGL failure as the critical limitation
- Position plan-guided training as the key methodological contribution

## Figures/Visuals to Generate
1. Training loss curves (epoch vs. SARI for BART v1 and v2)
2. Plan label distribution bar chart
3. SARI comparison bar chart (BART v2 vs LLaMA-8B vs LLaMA-4-Scout)
4. FKGL comparison (source vs BART vs LLaMA-8B)
5. Inference hyperparameter grid heatmap (if space allows)

## Citations to Include
- BART: Lewis et al., "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension" (ACL 2020)
- LLaMA-3: "The Llama 3 Herd of Models" (2024)
- LLaMA-4: Meta LLaMA-4 technical report (2025)
- SARI: Xu et al., "Optimizing Statistical Machine Translation for Text Simplification" (TACL 2016)
- SimpleText 2025/2026: CLEF SimpleText task description papers
- CEUR-WS: CEUR Workshop Proceedings template and guidelines
- BERTScore: Zhang et al., "BERTScore: Evaluating Text Generation with BERT" (ICLR 2020)
- RoBERTa: Liu et al., "RoBERTa: A Robustly Optimized BERT Pretraining Approach" (2019)
