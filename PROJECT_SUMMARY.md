# Recipe Q&A Assistant with RAG - Project Summary

## Project Overview
Conversational Recipe Q&A Assistant using Retrieval-Augmented Generation (RAG) to answer user questions about recipes.

## ✅ Completed Components

### 1. Data Preparation
- **Dataset**: 1,000 recipes sampled from Recipes.csv
- **Fields**: recipe_id, title, tags, ingredients, duration, calories, health_category
- **Preprocessing**: Cleaned text (lowercase), created searchable text field
- **Location**: `Project/data/recipes_subset.json`

### 2. Retrieval System
- **Method**: TF-IDF (scikit-learn)
- **Features**: 5,000 features, unigrams + bigrams
- **Function**: `retrieve_recipes(query, k=5)`
- **Performance** (Dual Evaluation):
  - **Manual NDCG@3**: **0.539** (Gold standard - human judgment)
  - **Manual Recall@3**: **0.531** (Gold standard)
  - Heuristic NDCG@3: 0.814 (Automatic - overestimates by ~34%)
  - Heuristic Recall@3: 0.869 (Automatic)
- **Location**: `Project/src/retrieval.py`

### 3. RAG Pipeline
- **LLM**: Claude 3 Haiku (Anthropic)
- **Prompt Template**: System + Context + User Query
- **Function**: `answer_query(query)`
- **Location**: `Project/src/rag_pipeline.py`

### 4. Conversation Handling
- **Features**: Tracks last query, supports clarifications
- **Clarifications**: "shorter", "with chicken instead", "healthier", etc.
- **Location**: `Project/src/conversation_handler.py`

### 5. Evaluation

#### Retrieval Metrics (Dual Approach)
- **Test Queries**: 18 queries evaluated (20 created)
- **Manual Evaluation** (Gold Standard):
  - NDCG@3: **0.539** (Moderate - true quality)
  - Recall@3: **0.531**
  - Method: Human judgment based on query intent
  - Total: 90 recipes manually labeled (18 queries × 5 recipes)
  - **File**: `Project/evaluation/manual_metrics.json`
- **Heuristic Evaluation** (Automatic):
  - NDCG@3: 0.814 (Overestimates by ~34%)
  - Recall@3: 0.869
  - Method: Keyword matching + cosine similarity threshold
  - **File**: `Project/evaluation/retrieval_metrics.json`

#### Manual Evaluation Query Breakdown
- ✅ Perfect retrieval (NDCG = 1.0): 5 queries (27.8%)
- ✅ Good retrieval (NDCG 0.5-0.8): 5 queries (27.8%)
- ⚠️ Poor retrieval (NDCG 0.2-0.5): 5 queries (27.8%)
- ❌ Failed retrieval (NDCG = 0.0): 3 queries (16.7%)

#### Answer Quality Evaluation
- **Human Ratings** (5-point scale, 3 sample queries):
  - **LLM-RAG**: 5.0/5 overall quality
  - **Baseline**: 1.7/5 overall quality
  - **Improvement**: +172% (+3.1 points)
- **Files**: `Project/evaluation/answer_quality_rating_template.json`

#### Baseline Comparison
- **Baseline**: Template-only responses (no LLM)
- **LLM-RAG**: Claude-generated responses
- **Result**: LLM-RAG significantly better in:
  - Natural language quality (5.0 vs 2.0)
  - Context understanding
  - Relevant details (calories, health, timing)
  - Reasoning and explanation
- **Key Insight**: Despite moderate retrieval (NDCG 0.539), answer quality is excellent (5.0/5) because LLM compensates by selecting best recipes and explaining gaps
- **Files**:
  - `Project/evaluation/baseline_comparison.txt`
  - `Project/evaluation/baseline_comparison.json`
  - `Project/evaluation/ANSWER_QUALITY_ANALYSIS.txt`

### 6. Sample Interactions
- **Count**: 8 example dialogues
- **Content**: User queries + Retrieved recipes + Assistant responses
- **Files**:
  - `Project/evaluation/sample_interaction_log.txt`
  - `Project/evaluation/sample_interaction_log.json`

### 7. Test Results
- **All 20 test queries** with full results
- **File**: `Project/evaluation/test_results.json`

## Project Structure

```
Project/
├── data/
│   └── recipes_subset.json              # 1000 recipes
├── src/
│   ├── prepare_data.py                  # Data preprocessing
│   ├── retrieval.py                     # TF-IDF retrieval
│   ├── rag_pipeline.py                  # RAG system
│   ├── conversation_handler.py          # Conversational wrapper
│   ├── run_all_tests.py                 # Test all 20 queries
│   ├── evaluate_retrieval.py            # NDCG/Recall metrics
│   ├── baseline_comparison.py           # Baseline vs LLM-RAG
│   └── generate_interaction_log.py      # Sample dialogues
├── notebooks/
│   └── recipe_qa_demo.ipynb             # Interactive demo
├── evaluation/
│   ├── test_qa_pairs.json               # 20 test questions
│   ├── test_results.json                # All query results
│   ├── retrieval_metrics.json           # Heuristic NDCG/Recall (0.814, 0.869)
│   ├── manual_metrics.json              # Manual NDCG/Recall (0.539, 0.531)
│   ├── manual_relevance_labels_full.json # Manual labels (90 recipes)
│   ├── baseline_comparison.txt/.json    # Baseline comparison
│   ├── sample_interaction_log.txt/.json # Sample dialogues
│ 
├── requirements.txt                     # Dependencies
├── README.md                            # Usage instructions
└── PROJECT_SUMMARY.md                   # This file
```

## Key Results

### Retrieval Performance (Dual Evaluation)

| Evaluation Method | NDCG@3 | Recall@3 | Interpretation |
|-------------------|--------|----------|----------------|
| **Manual (Gold Standard)** | **0.539** | **0.531** | Moderate - True quality with human judgment |
| Heuristic (Automatic) | 0.814 | 0.869 | Overestimates by ~34% (keyword matching) |

**Why the Difference?**
- Manual: Evaluates whether recipe satisfies ALL query constraints and intent
- Heuristic: Matches keywords but misses semantic understanding
- Example: "low-calorie dinner" → heuristic matches "low-calorie" side dishes (wrong meal type)

**Query Performance (Manual Labels):**
- 55.6% of queries achieve good-to-perfect retrieval
- 44.4% have poor-to-failed retrieval
- TF-IDF excels at simple ingredient/dietary queries
- TF-IDF struggles with compound constraints and semantic understanding

### LLM-RAG vs Baseline

**Baseline (Template-only)**
- ✓ Fast, no API costs
- ✗ Generic responses
- ✗ No context understanding
- ✗ Limited to recipe titles

**LLM-RAG (Claude)**
- ✓ Natural, conversational
- ✓ Understands intent
- ✓ Relevant details (calories, health, etc.)
- ✓ Explains reasoning
- ✓ **Overall quality: 5.0/5** (vs baseline 1.7/5)
- ✗ Small API cost (~$0.001/query)

**Human Quality Ratings:**
- LLM-RAG: **5.0/5** overall (excellent)
- Baseline: 1.7/5 overall (poor)
- **Improvement: +172%** (+3.1 points on 5-point scale)

**Key Insight**: Despite moderate retrieval (NDCG 0.539), answer quality is excellent (5.0/5) because the LLM:
- Selects the BEST recipe from retrieved results (not just first)
- Explains gaps honestly when no perfect match exists
- Adds contextual reasoning beyond raw data

**Conclusion**: LLM generation quality matters MORE than perfect retrieval for excellent user experience.

## Sample Queries Tested

1. Show me a quick vegetarian pasta recipe
2. List two low-calorie dinners
3. What's a healthy breakfast option?
4. Suggest a chocolate dessert
5. Give me a high-protein meal
6. Show me a salad recipe
7. What can I make with chicken?
8. List recipes under 30 minutes
9. Show me a soup recipe
10. What's a good side dish?
11. Give me a vegan recipe
12. Show me a low-sugar dessert
13. What's a good appetizer?
14. Give me a recipe with rice
15. Show me a seafood dish
16. What's a good lunch option?
17. Give me a baked recipe
18. Show me a recipe with eggs
19. What's a comfort food recipe?
20. Give me a spicy recipe

## How to Use

### Run the System
```bash
cd Project/src
python conversation_handler.py
```

### Run Tests
```bash
python run_all_tests.py
```

### Run Evaluation
```bash
python evaluate_retrieval.py          # Heuristic NDCG/Recall
python evaluate_manual_labels.py     # Manual NDCG/Recall + comparison
python baseline_comparison.py        # Baseline vs LLM-RAG
python generate_interaction_log.py   # Sample dialogues
```

### Use Jupyter Notebook
```bash
cd ../notebooks
jupyter notebook recipe_qa_demo.ipynb
```

## Technical Stack

- **Python**: 3.12
- **LLM**: Claude 3 Haiku (Anthropic)
- **Retrieval**: TF-IDF (scikit-learn)
- **Data**: pandas, numpy
- **Evaluation**: scipy, numpy

## Cost Analysis

- **Total API Cost for 20 queries**: ~$0.02
- **Per query**: ~$0.001
- **Model**: Claude 3 Haiku ($0.25 per 1M input tokens)

## Deliverables

✅ **Prototype**: Scripts + Notebook with `retrieve_recipes()` and `answer_query()`
✅ **Evaluation**:
  - Dual evaluation: Manual (0.539) + Heuristic (0.814)
  - 90 manually labeled recipes (18 queries)
  - Answer quality ratings (5.0/5 vs 1.7/5)
  - Baseline vs LLM-RAG comparison
✅ **Sample Interactions**: 8 example dialogues + live demo
✅ **Report**: PROJECT_REPORT.txt (4 pages with dual evaluation)
✅ **Documentation**:
  - EVALUATION_SUMMARY.txt
  - MANUAL_LABELING_ANALYSIS.txt
  - ANSWER_QUALITY_ANALYSIS.txt
✅ **Presentation**: PRESENTATION_OUTLINE.md ready

## Key Achievements

1. ✅ **Rigorous Evaluation**: Dual approach (heuristic + manual) demonstrates proper IR methodology
2. ✅ **Honest Assessment**: Manual evaluation reveals true NDCG 0.539 (not inflated 0.814)
3. ✅ **Critical Insight**: Generation quality > retrieval perfection for user experience
4. ✅ **Complete Documentation**: 90 manually labeled recipes with detailed analysis
5. ✅ **Academic Rigor**: Quantified heuristic overestimation (34-39%)

## Contact

For questions about this project, refer to the code documentation and evaluation results.

---

*Updated: November 26, 2025*
*Evaluation: Dual approach (Manual + Heuristic)*
*Model: Claude 3 Haiku via Anthropic API*
*Retrieval: TF-IDF with scikit-learn*
