# Recipe Q&A Assistant with RAG - Presentation Outline
## 10-15 Minute Project Presentation

---

## Slide 1: Title Slide
**Conversational Recipe Q&A Assistant with RAG**

- Student Name
- Course: Natural Language Processing
- Date: November 24, 2025
- Technologies: TF-IDF + Claude 3 Haiku

*Visual*: Logo or image of the system in action

---

## Slide 2: Problem Statement & Motivation

**The Problem:**
- Users want to find recipes using natural language
- Traditional search requires exact keywords
- No conversational interaction or follow-up clarifications

**Our Solution:**
- Conversational assistant using RAG (Retrieval-Augmented Generation)
- Natural language queries: "Show me a quick vegetarian pasta"
- Follow-up support: "with chicken instead", "healthier"

*Visual*: Before/After comparison showing keyword search vs natural language

**Speaking Notes** (1-2 min):
- Explain frustration with traditional recipe search
- Introduce RAG as combining retrieval + LLM generation
- Preview the conversational nature

---

## Slide 3: What is RAG?

**Retrieval-Augmented Generation (RAG):**

1. **Retrieval**: Find relevant information from database
2. **Augmentation**: Add context to user query
3. **Generation**: LLM generates natural answer using context

**Why RAG?**
- ✓ Grounded in real data (no hallucination)
- ✓ Up-to-date information (our recipe database)
- ✓ Cost-effective (small model + focused retrieval)
- ✓ Interpretable (can see retrieved recipes)

*Visual*: Flowchart showing: User Query → Retrieval → Context + Query → LLM → Answer

**Speaking Notes** (1-2 min):
- Explain each step of RAG pipeline
- Emphasize grounding prevents hallucination
- Compare to pure LLM (would make up recipes)

---

## Slide 4: Dataset

**HUMMUS Recipe Database**
- Original: 507,335 recipes
- Project subset: **1,000 recipes** (sampled)

**Key Fields:**
- Title, Tags, Ingredients
- Duration (minutes)
- Calories
- Health scores

**Preprocessing:**
- Lowercased text
- Combined title + tags + ingredients → searchable text
- Cleaned and standardized format

*Visual*: Table showing sample recipe entries with fields

**Speaking Notes** (1 min):
- Mention dataset source
- Explain why we sampled 1,000 (class project scale)
- Show preprocessing steps

---

## Slide 5: System Architecture

**Three Main Components:**

1. **TF-IDF Retrieval Module**
   - 5,000 features, 1-2 word n-grams
   - Cosine similarity matching
   - Returns top-5 most relevant recipes

2. **RAG Pipeline**
   - Claude 3 Haiku (Anthropic)
   - Prompt template with system + context + query
   - Generates 1-3 sentence natural answers

3. **Conversation Handler**
   - Tracks last query
   - Detects clarifications ("shorter", "with chicken")
   - Combines follow-ups with previous query

*Visual*: Architecture diagram with three boxes and arrows

**Speaking Notes** (2 min):
- Walk through each component
- Explain TF-IDF choice (simple, fast, effective)
- Mention Claude Haiku cost-effectiveness

---

## Slide 6: Prompt Engineering

**System Prompt Design:**
```
You are a helpful recipe assistant. Answer user questions
using ONLY the information in the CONTEXT below.

Guidelines:
- Provide concise answers (1-3 sentences)
- Mention specific recipe titles when relevant
- If context doesn't help, say so
- Use friendly, conversational tone
```

**Context Format:**
```
CONTEXT (Retrieved Recipes):
1. Creamy Spinach Penne
   Tags: vegetarian, pasta, italian
   Ingredients: penne, spinach, cream, garlic...
   Duration: 25 min | Calories: 385
[... top-5 recipes ...]

USER QUESTION: Show me a quick vegetarian pasta
```

*Visual*: Side-by-side showing template structure

**Speaking Notes** (1-2 min):
- Emphasize "ONLY the information in CONTEXT" constraint
- Show how context is formatted for LLM
- Mention conciseness requirement (1-3 sentences)

---

## Slide 7: Live Demo (Interactive)

**Example Interactions:**

**Query 1: Basic Search**
```
User: Show me a quick vegetarian pasta recipe
System: I recommend Creamy Spinach Penne (385 cal, 25 min).
        It's both healthy and fast to prepare!
```

**Query 2: Follow-up Clarification**
```
User: with chicken instead
System: [Detects clarification]
System: For chicken pasta, try Chicken Alfredo Penne
        (520 cal, 35 min)...
```

**Query 3: Constraint-based**
```
User: List recipes under 30 minutes
System: Quick Veggie Stir Fry (15 min, 280 cal),
        Simple Egg Scramble (10 min, 250 cal)...
```

*Visual*: Screenshots or live terminal demo

**Speaking Notes** (2-3 min):
- Run 2-3 live queries if time permits
- Otherwise show pre-captured screenshots
- Emphasize natural language and conversation flow

---

## Slide 8: Evaluation Results

### Retrieval Performance

| Metric | Score | Interpretation |
|--------|-------|----------------|
| **NDCG@3** | **0.814** | Excellent - relevant recipes ranked high |
| **Recall@3** | **0.869** | Excellent - captures 86.9% of relevant recipes |

**Test Set:**
- 20 diverse queries
- Various types: ingredients, time, health, categories
- Heuristic relevance labeling

*Visual*: Bar chart showing NDCG and Recall scores

**Speaking Notes** (1-2 min):
- Explain NDCG (ranking quality with position discounting)
- Explain Recall (coverage of relevant results)
- Emphasize "Excellent" performance level

---

## Slide 9: Baseline Comparison

**Two Approaches Compared:**

**Baseline (Template-only):**
```
"Based on your search, I found: Recipe A, Recipe B, and Recipe C.
Recipe A has 350 calories and takes 30 minutes."
```
- ✗ Generic, rigid format
- ✗ No context understanding
- ✗ Limited to recipe titles
- ✓ Fast, no API cost

**LLM-RAG (Claude):**
```
"For a quick vegetarian pasta option, I'd recommend Creamy Spinach
Penne (385 calories, 25 min). It's both healthy and fast to prepare."
```
- ✓ Natural, conversational language
- ✓ Understands query intent ("quick" → mentions speed)
- ✓ Selects relevant details
- ✓ Explains reasoning
- Cost: ~$0.001/query

*Visual*: Side-by-side comparison with highlighting

**Speaking Notes** (2 min):
- Show same query answered both ways
- Emphasize dramatic quality difference
- Mention minimal cost ($0.001/query)

---

## Slide 10: Cost Analysis

**Claude 3 Haiku Pricing:**
- Input tokens: $0.25 per 1M tokens
- Output tokens: $1.25 per 1M tokens

**Our Usage:**
- Average query cost: **~$0.001** (one-tenth of a cent)
- 20 test queries: **~$0.02**
- $5 credit covers: **~5,000 queries**

**Conclusion:**
- Highly cost-effective for educational and small-scale use
- Minimal cost for dramatic quality improvement over templates

*Visual*: Cost breakdown table or chart

**Speaking Notes** (1 min):
- Emphasize affordability
- Compare to potential benefits
- Mention scalability considerations

---

## Slide 11: Key Findings

**What Works Well:**
1. TF-IDF retrieval is excellent for recipe search (NDCG: 0.814)
2. LLM provides natural, contextual answers
3. Simple conversation handling enables follow-ups
4. System is cost-effective and reproducible

**Limitations:**
1. Limited dataset (1,000 recipes)
2. Keyword-based retrieval (misses semantic similarity)
3. Shallow conversation (only last query tracked)
4. Heuristic evaluation (no human ratings)

**What We Learned:**
- RAG effectively combines strengths of retrieval + generation
- Prompt engineering is critical for quality and grounding
- Simple systems can achieve excellent results

*Visual*: Two columns (Strengths | Limitations)

**Speaking Notes** (1-2 min):
- Balance achievements and limitations
- Show awareness of trade-offs
- Emphasize learning outcomes

---

## Slide 12: Future Improvements

**Short-term Enhancements:**
1. Expand to 5,000-10,000 recipes
2. Add more dietary filters (gluten-free, keto, etc.)
3. Human evaluation with relevance ratings (1-5 scale)

**Technical Upgrades:**
1. **Hybrid Retrieval**: TF-IDF + Sentence embeddings
   - Combines keyword matching + semantic understanding
2. **Multi-turn Conversation**: Track full conversation history
3. **User Preferences**: Remember dietary restrictions and favorites
4. **Visual Search**: Add recipe image understanding

**Deployment:**
1. Web interface or mobile app
2. Integration with meal planning apps
3. Voice assistant compatibility

*Visual*: Roadmap or timeline showing improvements

**Speaking Notes** (1 min):
- Prioritize improvements
- Mention technical feasibility
- Connect to real-world applications

---

## Slide 13: Conclusion

**Project Achievements:**
- ✓ Implemented full RAG pipeline (retrieval + generation)
- ✓ Achieved excellent retrieval performance (NDCG: 0.814)
- ✓ Demonstrated LLM value over baseline templates
- ✓ Created conversational interface with clarifications
- ✓ Cost-effective solution (~$0.001/query)

**Key Takeaway:**
Combining traditional IR with modern LLMs creates powerful, grounded, and cost-effective conversational systems.

**Applications Beyond Recipes:**
- Product recommendations
- Document Q&A (legal, medical)
- Customer support
- Educational tutoring

*Visual*: Summary checklist with checkmarks

**Speaking Notes** (1 min):
- Recap main achievements
- Emphasize broader applicability of RAG
- Connect project to real-world use cases

---

## Slide 14: Questions?

**Demo & Code Available:**
- GitHub repository: [if applicable]
- Jupyter notebook: `notebooks/recipe_qa_demo.ipynb`
- Full evaluation: `evaluation/` directory

**Contact:**
- [Your email]
- [Office hours or contact method]

**Thank you!**

*Visual*: Contact information and QR code to repository

**Speaking Notes**:
- Open floor for questions
- Offer to show specific code sections
- Mention availability for follow-up discussions

---

## Appendix Slides (Backup)

### A1: Technical Details - TF-IDF Configuration
- Max features: 5,000
- N-gram range: 1-2
- Stop words: English
- Vectorizer: scikit-learn TfidfVectorizer

### A2: Sample Interaction Log (Full)
- Complete 8-dialogue examples
- Shows variety of query types
- Demonstrates conversation flow

### A3: Evaluation Methodology
- NDCG calculation formula
- Recall calculation formula
- Relevance labeling approach

### A4: Code Walkthrough
- Key functions: `retrieve_recipes()`, `answer_query()`
- Prompt template details
- Conversation handler logic

---

## Presentation Tips

**Timing Breakdown (Total: 12-14 minutes):**
- Introduction & Problem (Slides 1-2): 2 min
- RAG & Dataset (Slides 3-4): 2 min
- Architecture & Design (Slides 5-6): 3 min
- Demo (Slide 7): 2-3 min
- Evaluation & Results (Slides 8-9): 3 min
- Conclusion & Future Work (Slides 10-13): 2 min
- Q&A: Remaining time

**Delivery Tips:**
- Rehearse live demo to avoid technical issues
- Have backup screenshots if live demo fails
- Emphasize visual elements (architecture diagram, comparison charts)
- Keep technical details accessible to non-experts
- Practice smooth transitions between slides
- Anticipate questions about:
  - Why TF-IDF over embeddings?
  - Cost at scale?
  - How to improve retrieval?
  - Prompt engineering process?

**Visual Design:**
- Use consistent color scheme
- Large, readable fonts (minimum 18pt)
- Limit text per slide (bullet points, not paragraphs)
- Include relevant charts/diagrams on every slide
- Use examples and comparisons to illustrate concepts

---

*Presentation outline ready for slide creation*
*Estimated time: 12-14 minutes + Q&A*
