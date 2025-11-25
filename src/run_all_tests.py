"""
Run all 20 test Q&A pairs and save results
"""

import json
import os
from rag_pipeline import RecipeRAG

# Initialize RAG system with API key from environment variable
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("Error: ANTHROPIC_API_KEY environment variable not set.")
    print("Please set it using: export ANTHROPIC_API_KEY='your-api-key'")
    exit(1)

rag = RecipeRAG(llm_provider="anthropic", api_key=api_key)

# Load test Q&A pairs
with open('../evaluation/test_qa_pairs.json', 'r') as f:
    test_pairs = json.load(f)

print("\n" + "="*70)
print("Running All 20 Test Q&A Pairs")
print("="*70)

# Run all tests
results = []
for i, test in enumerate(test_pairs, 1):
    query = test['query']

    print(f"\n[{i}/20] Testing: {query}")
    print("-"*70)

    try:
        result = rag.answer_query(query, k=5, verbose=False)
        results.append(result)

        print(f"✓ Answer: {result['answer'][:150]}...")

    except Exception as e:
        print(f"✗ Error: {e}")
        results.append({
            "query": query,
            "error": str(e)
        })

print("\n" + "="*70)
print(f"Completed {len(results)}/20 tests")
print("="*70)

# Save results
output_file = '../evaluation/test_results.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n✓ Results saved to: {output_file}")

# Print summary
print("\n" + "="*70)
print("Summary of Results")
print("="*70)

for i, result in enumerate(results, 1):
    if 'error' not in result:
        print(f"{i}. {result['query']}")
        print(f"   Retrieved: {result['num_recipes_retrieved']} recipes")
        print(f"   Answer: {result['answer'][:100]}...")
        print()
