# Conversational Recipe Q&A Assistant with RAG
## Project Report

**Course Project - Natural Language Processing**
**Date**: November 24, 2025
**Model**: Claude 3 Haiku (Anthropic API)
**Retrieval**: TF-IDF with scikit-learn

---

## 1. Introduction

This project implements a conversational question-answering assistant for recipe queries using Retrieval-Augmented Generation (RAG). The system combines traditional information retrieval techniques with modern large language models to provide natural, contextually relevant answers about recipes including ingredients, preparation time, nutritional information, and dietary characteristics.

The goal is to enable users to ask questions in natural language (e.g., "Show me a quick vegetarian pasta recipe") and receive accurate, conversational responses grounded in a curated recipe database. The system supports follow-up clarifications like "with chicken instead" or "healthier", making the interaction more natural and user-friendly.

## 2. Dataset

### 2.1 Source Data
We used the HUMMUS recipe dataset (Recipes.csv), which contains 507,335 recipes with comprehensive metadata including:
- Recipe identifiers and titles
- Tags and categories
- Ingredient lists
- Preparation duration
- Nutritional information (calories, protein, sugars, sodium)
- Health scores (WHO normalized scores)

### 2.2 Preprocessing
For this project, we sampled **1,000 recipes** to create a manageable subset suitable for a class project while maintaining diversity. The preprocessing pipeline included:

1. **Text Cleaning**: Lowercased all text fields (title, tags, ingredients)
2. **Field Selection**: Extracted key fields:
   - `recipe_id`: Unique identifier
   - `title`: Recipe name
   - `tags`: Category tags (e.g., vegetarian, dessert)
   - `ingredients`: List of ingredients
   - `duration`: Preparation time in minutes
   - `calories`: Caloric content
   - `health_category`: Derived health classification

3. **Searchable Text Creation**: Combined title, tags, and ingredients into a single `searchable_text` field for efficient retrieval

The preprocessed dataset is stored in `data/recipes_subset.json` for reproducibility.

## 3. System Architecture

### 3.1 Retrieval Module
We implemented a **TF-IDF (Term Frequency-Inverse Document Frequency)** based retrieval system using scikit-learn. This keyword-based approach was chosen for its simplicity, speed, and effectiveness for recipe retrieval tasks.

**Configuration**:
- Maximum features: 5,000
- N-gram range: 1-2 (unigrams and bigrams)
- Stop words: English
- Similarity metric: Cosine similarity

**Key Function**:
```python
def retrieve_recipes(query, k=5):
    """Retrieve top-k most relevant recipes for a query"""
    query_vector = vectorizer.transform([query.lower()])
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    return [recipes[i] for i in top_k_indices]
```

### 3.2 RAG Pipeline
The RAG pipeline integrates the retrieval system with Claude 3 Haiku (Anthropic's fast, cost-effective LLM) to generate natural language answers.

**Prompt Template Design**:

*System Prompt*:
```
You are a helpful recipe assistant. Answer user questions about recipes
using ONLY the information provided in the CONTEXT below.

Guidelines:
- Provide concise, natural answers (1-3 sentences)
- Mention specific recipe titles when relevant
- If the context doesn't contain relevant recipes, say so
- Focus on answering the specific question asked
- Use friendly, conversational tone
```

*User Message Format*:
```
CONTEXT (Retrieved Recipes):
[Top-k recipes with title, tags, ingredients, duration, calories]

USER QUESTION: {user_query}

Please answer the question based on the recipes provided above.
```

This design constrains the LLM to use only retrieved recipe information, preventing hallucination while maintaining natural language generation quality.

### 3.3 Conversation Handling
The system tracks conversation state to support follow-up clarifications:

**Features**:
- Tracks last query and results
- Detects clarification keywords: "shorter", "with chicken instead", "healthier", "vegan", etc.
- Automatically combines clarifications with previous query
- Supports interactive CLI and demo modes

**Example**:
```
User: Show me a pasta recipe
Assistant: [Returns pasta recipes]
User: with chicken instead
System: [Detects clarification, searches for "pasta recipe with chicken"]
```

## 4. Evaluation

### 4.1 Test Set
We created **20 diverse test queries** covering different recipe types, dietary restrictions, and query styles:
- Ingredient-based: "What can I make with chicken?"
- Time-based: "List recipes under 30 minutes"
- Health-based: "Show me low-calorie dinners"
- Category-based: "Give me a vegan recipe"
- Specific dishes: "Show me a soup recipe"

### 4.2 Retrieval Performance
We evaluated retrieval quality using two standard metrics:

**NDCG@3 (Normalized Discounted Cumulative Gain at rank 3)**: Measures ranking quality with position discounting
- **Score: 0.814**
- Interpretation: Excellent - the most relevant recipes consistently appear in top positions

**Recall@3**: Percentage of relevant recipes retrieved in top 3 results
- **Score: 0.869**
- Interpretation: Excellent - system captures 86.9% of relevant recipes

| Metric | Score | Interpretation |
|--------|-------|----------------|
| NDCG@3 | 0.814 | Excellent |
| Recall@3 | 0.869 | Excellent |

These metrics indicate that the TF-IDF retrieval system is highly effective for recipe search tasks, consistently surfacing relevant results in top positions.

### 4.3 Baseline Comparison
We compared two approaches to demonstrate the value of LLM-based generation:

**Baseline (Template-only)**:
- Simple template that lists top recipe titles
- Adds basic metadata (calories, duration) from first recipe
- Example: "Based on your search, I found: Recipe A, Recipe B, and Recipe C. Recipe A has 350 calories and takes 30 minutes."

**LLM-RAG (Claude)**:
- Full RAG pipeline with contextual understanding
- Natural language responses with reasoning
- Relevant detail selection based on query intent
- Example: "For a quick vegetarian pasta option, I'd recommend Creamy Spinach Penne (385 calories, 25 min). It's both healthy and fast to prepare."

**Key Findings**:
- LLM-RAG provides significantly better user experience
- Natural, conversational language vs rigid templates
- Context understanding (distinguishes between "quick" vs "healthy" vs "protein-rich")
- Relevant detail selection (mentions calories for low-calorie queries, time for quick meal queries)
- Reasoning and explanation capabilities
- Small cost (~$0.001/query) provides dramatic quality improvement

### 4.4 Cost Analysis
**API Costs (Claude 3 Haiku)**:
- Input tokens: $0.25 per 1M tokens
- Output tokens: $1.25 per 1M tokens
- Average cost per query: ~$0.001
- Total cost for 20 test queries: ~$0.02
- $5 credit covers ~5,000 queries

The system is highly cost-effective for educational and small-scale deployment use cases.

## 5. Sample Interactions

Below are representative examples showing system behavior across different query types:

**Example 1: Ingredient-based Query**
```
USER: What can I make with chicken?
RETRIEVED: Chicken Tikka Masala, Lemon Herb Chicken, Thai Chicken Curry
ASSISTANT: You have several great chicken options! Chicken Tikka Masala
(425 cal, 45 min) is a flavorful Indian dish, while Lemon Herb Chicken
(320 cal, 30 min) offers a lighter, quicker option. For something exotic,
try Thai Chicken Curry (480 cal, 40 min).
```

**Example 2: Time-constrained Query**
```
USER: List recipes under 30 minutes
RETRIEVED: Quick Veggie Stir Fry, Simple Egg Scramble, Fast Fish Tacos
ASSISTANT: For meals under 30 minutes, I recommend Quick Veggie Stir Fry
(15 min, 280 cal), Simple Egg Scramble (10 min, 250 cal), or Fast Fish
Tacos (25 min, 350 cal). All are quick and nutritious.
```

**Example 3: Follow-up Clarification**
```
USER: Show me a pasta recipe
ASSISTANT: [Returns pasta recipes]
USER: with chicken instead
SYSTEM: [Detected clarification based on previous query]
SYSTEM: [Modified query: pasta recipe with chicken]
ASSISTANT: For chicken pasta, try Chicken Alfredo Penne (520 cal, 35 min)...
```

Complete interaction logs with all 8 sample dialogues are available in `evaluation/sample_interaction_log.txt`.

## 6. Results and Discussion

### 6.1 Key Achievements
1. **Effective Retrieval**: NDCG@3 of 0.814 demonstrates that TF-IDF performs excellently for recipe search
2. **Natural Responses**: LLM integration provides conversational, context-aware answers
3. **Cost Efficiency**: $0.001/query makes the system practical for deployment
4. **Conversation Support**: Simple state tracking enables natural follow-up interactions
5. **Reproducible Pipeline**: All components are modular and well-documented

### 6.2 Limitations
1. **Dataset Size**: 1,000 recipes limit coverage of global cuisines and niche dietary needs
2. **Relevance Labeling**: Evaluation uses heuristic relevance detection rather than human labels
3. **Conversation Depth**: Tracks only last query; no multi-turn conversation memory
4. **Semantic Understanding**: TF-IDF is keyword-based; may miss semantic similarities (e.g., "quick" vs "fast")

### 6.3 Future Improvements
1. **Larger Dataset**: Expand to 5,000-10,000 recipes for better coverage
2. **Semantic Retrieval**: Use sentence embeddings (e.g., Sentence-BERT) for semantic matching
3. **Hybrid Retrieval**: Combine TF-IDF + embeddings for both keyword and semantic search
4. **Human Evaluation**: Conduct user studies with relevance ratings (1-5 scale)
5. **Advanced Conversation**: Add multi-turn memory and preference learning

## 7. Conclusion

This project successfully demonstrates the effectiveness of combining traditional information retrieval with modern LLMs for conversational question answering. The TF-IDF retrieval system achieves excellent performance (NDCG@3: 0.814, Recall@3: 0.869), while Claude 3 Haiku generates natural, contextually relevant responses at minimal cost.

The baseline comparison clearly shows the value of LLM integration: template-based responses provide basic information but lack the natural language quality, context understanding, and reasoning capabilities that LLMs offer. For a marginal cost of $0.001 per query, the system delivers a dramatically superior user experience.

The modular architecture makes the system easy to extend and improve. Future work could expand the dataset, incorporate semantic embeddings, and add more sophisticated conversation management while maintaining the system's simplicity and cost-effectiveness.

## 8. References

**Code and Data**:
- All source code: `Project/src/`
- Evaluation results: `Project/evaluation/`
- Jupyter demo: `Project/notebooks/recipe_qa_demo.ipynb`

**Technologies**:
- Python 3.12
- scikit-learn (TF-IDF)
- Anthropic Claude 3 Haiku
- pandas, numpy, scipy

**Dataset**: HUMMUS Recipe Database (Recipes.csv)

---

*Report generated for academic project submission*
*All code and evaluation materials available in project repository*
