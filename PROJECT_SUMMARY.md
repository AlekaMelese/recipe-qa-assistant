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
- **Performance**:
  - NDCG@3: **0.814** (Excellent)
  - Recall@3: **0.869** (Excellent)
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

#### Retrieval Metrics
- **Test Queries**: 20 diverse questions
- **NDCG@3**: 0.814
- **Recall@3**: 0.869
- **File**: `Project/evaluation/retrieval_metrics.json`

#### Baseline Comparison
- **Baseline**: Template-only responses (no LLM)
- **LLM-RAG**: Claude-generated responses
- **Result**: LLM-RAG significantly better in:
  - Natural language quality
  - Context understanding
  - Relevant details (calories, health, timing)
  - Reasoning and explanation
- **Files**:
  - `Project/evaluation/baseline_comparison.txt`
  - `Project/evaluation/baseline_comparison.json`

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
│   ├── retrieval_metrics.json           # NDCG/Recall scores
│   ├── baseline_comparison.txt/.json    # Baseline comparison
│   └── sample_interaction_log.txt/.json # Sample dialogues
├── requirements.txt                     # Dependencies
├── README.md                            # Usage instructions
└── PROJECT_SUMMARY.md                   # This file
```

## Key Results

### Retrieval Performance
| Metric | Score | Interpretation |
|--------|-------|----------------|
| NDCG@3 | 0.814 | Excellent - Retrieval is highly effective |
| Recall@3 | 0.869 | Excellent - Most relevant recipes retrieved |

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
- ✗ Small API cost (~$0.001/query)

**Conclusion**: LLM-RAG provides dramatically better user experience for minimal cost.

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
python evaluate_retrieval.py
python baseline_comparison.py
python generate_interaction_log.py
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



*Generated: November 24, 2025*
*Model: Claude 3 Haiku via Anthropic API*
*Retrieval: TF-IDF with scikit-learn*
