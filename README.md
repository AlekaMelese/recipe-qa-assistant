# Recipe Q&A Assistant with RAG

A conversational question-answering assistant for recipe queries using Retrieval-Augmented Generation (RAG). Combines TF-IDF retrieval with Claude 3 Haiku for natural, contextually relevant answers.

![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-complete-success)

## 🎯 Project Overview

This project implements a conversational recipe assistant that:
- ✅ Understands natural language queries ("Show me a quick vegetarian pasta")
- ✅ Supports follow-up clarifications ("with chicken instead", "healthier")
- ✅ Retrieves relevant recipes using TF-IDF (NDCG@3: 0.814, Recall@3: 0.869)
- ✅ Generates natural answers using Claude 3 Haiku
- ✅ Costs ~$0.001 per query (highly affordable)

## 📊 Key Results

| Metric | Score | Interpretation |
|--------|-------|----------------|
| NDCG@3 | 0.814 | Excellent retrieval quality |
| Recall@3 | 0.869 | 86.9% relevant recipe coverage |
| Cost/Query | $0.001 | Highly cost-effective |

## Project Structure

```
Project/
├── data/
│   └── recipes_subset.json          # 1000 sampled recipes
├── src/
│   ├── prepare_data.py              # Data preprocessing script
│   ├── retrieval.py                 # TF-IDF retrieval module
│   └── rag_pipeline.py              # RAG system (retrieval + LLM)
├── notebooks/
│   └── recipe_qa_demo.ipynb         # Interactive demo notebook
├── evaluation/
│   └── test_qa_pairs.json           # 20 test Q&A pairs
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Setup Instructions

### 1. Activate Conda Environment

```bash
conda activate /scratch/aayalew25/Aleka/alekapy
```

### 2. Navigate to Project Directory

```bash
cd /scratch/aayalew25/Food/FoodNew/Project
```

### 3. Install Additional Dependencies (if needed)

The `anthropic` and `openai` packages are already installed. If you need to reinstall:

```bash
pip install anthropic openai
```

## Usage

### Step 1: Prepare Data (Already Done!)

```bash
cd src
python prepare_data.py
```

This creates `data/recipes_subset.json` with 1000 recipes.

### Step 2: Test Retrieval System

```bash
cd src
python retrieval.py
```

This tests the TF-IDF retrieval with sample queries.

### Step 3: Set API Key

Choose your LLM provider and set the API key:

**Option A: Anthropic (Claude) - Recommended**
```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key-here'
```

**Option B: OpenAI (GPT)**
```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

### Step 4: Test RAG System

```bash
cd src
python rag_pipeline.py
```

This runs the full RAG pipeline with sample queries.

### Step 5: Use Jupyter Notebook (Recommended)

```bash
cd notebooks
jupyter notebook recipe_qa_demo.ipynb
```

The notebook provides an interactive interface for:
- Testing retrieval
- Running RAG queries
- Viewing results
- Generating evaluation data

## How It Works

### 1. Retrieval Module (`retrieval.py`)

- Uses **TF-IDF** (Term Frequency-Inverse Document Frequency)
- Indexes recipes by: title + tags + ingredients
- Returns top-k most relevant recipes based on cosine similarity

### 2. RAG Pipeline (`rag_pipeline.py`)

The RAG system follows this workflow:

1. **Retrieve**: Find top-k relevant recipes using TF-IDF
2. **Format**: Create context from retrieved recipes
3. **Generate**: Send query + context to LLM for answer generation

### 3. Prompt Template

```
System: You are a helpful recipe assistant. Answer using ONLY
        the recipes in the CONTEXT.

Context: [Retrieved recipes with details]

User Query: [User's question]
```

## Example Queries

- "Show me a quick vegetarian pasta recipe"
- "List two low-calorie dinners"
- "What's a healthy breakfast option?"
- "Suggest a chocolate dessert"
- "Give me a high-protein meal"

## API Providers

### Anthropic (Claude)

- Model: `claude-3-haiku-20240307` (fast and affordable)
- API Key: Set `ANTHROPIC_API_KEY`
- Cost: ~$0.25 per 1M input tokens

### OpenAI (GPT)

- Model: `gpt-3.5-turbo`
- API Key: Set `OPENAI_API_KEY`
- Cost: ~$0.50 per 1M input tokens

## Evaluation

### Test Q&A Pairs

Located in `evaluation/test_qa_pairs.json`:
- 20 manually created test queries
- Expected characteristics for each query
- Use for retrieval and answer quality evaluation

### Metrics

**Retrieval Evaluation:**
- NDCG@3 (Normalized Discounted Cumulative Gain)
- Recall@3

**Answer Quality:**
- Human ratings (1-5 scale)
- Relevance to query
- Groundedness in retrieved recipes

## Quick Start

```bash
# 1. Activate environment
conda activate /scratch/aayalew25/Aleka/alekapy

# 2. Go to project
cd /scratch/aayalew25/Food/FoodNew/Project/src

# 3. Set API key
export ANTHROPIC_API_KEY='your-key'

# 4. Run RAG system
python rag_pipeline.py
```

## Troubleshooting

### Missing API Key

```
ValueError: ANTHROPIC_API_KEY not found
```

**Solution:** Set the environment variable:
```bash
export ANTHROPIC_API_KEY='your-key'
```

### Import Errors

```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:** Install the package:
```bash
pip install anthropic
```

### File Not Found

```
FileNotFoundError: recipes_subset.json
```

**Solution:** Run data preparation:
```bash
cd src
python prepare_data.py
```

## Deliverables Checklist

- [x] Data preprocessing script
- [x] Retrieval module (TF-IDF)
- [x] RAG pipeline (retrieval + LLM)
- [x] 20 test Q&A pairs
- [x] Interactive notebook
- [x] Conversation handling with clarifications
- [x] Evaluation results (NDCG: 0.814, Recall: 0.869)
- [x] Baseline vs LLM-RAG comparison
- [x] Sample interaction logs (8 examples + live demo)
- [x] 2-3 page report (PROJECT_REPORT.txt)
- [x] Presentation slides outline (PRESENTATION_OUTLINE.md)

## 📖 Additional Documentation

- **[PROJECT_REPORT.txt](PROJECT_REPORT.txt)** - Full 2-3 page academic report
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical summary of all components
- **[PRESENTATION_OUTLINE.md](PRESENTATION_OUTLINE.md)** - 10-15 minute presentation outline
- **[evaluation/](evaluation/)** - All evaluation results, metrics, and sample interactions

## 📧 Contact

For questions or feedback:
- Email: melese1820@gmail.com
- GitHub: (https://github.com/AlekaMelese)

## 📄 License

MIT License - Feel free to use this project for educational purposes.

## 🙏 Acknowledgments

- HUMMUS Recipe Database for the dataset
- Anthropic for Claude 3 Haiku API
- Course instructors (Mehrdad Rostami and Mohammad Aliannejadi)

---

**Built with ❤️ using Python, TF-IDF, and Claude 3 Haiku**

**Academic NLP Project - 2025**
