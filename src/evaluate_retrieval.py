"""
Evaluation Script for Retrieval Performance
Calculates NDCG@3 and Recall@3 metrics
"""

import json
import numpy as np
from collections import defaultdict

def calculate_ndcg_at_k(relevant_items, retrieved_items, k=3):
    """
    Calculate Normalized Discounted Cumulative Gain at k

    Args:
        relevant_items: Set of relevant recipe IDs
        retrieved_items: List of retrieved recipe IDs (ordered by relevance)
        k: Number of top results to consider

    Returns:
        NDCG@k score (0 to 1)
    """
    # Get top k retrieved items
    retrieved_k = retrieved_items[:k]

    # Calculate DCG (Discounted Cumulative Gain)
    dcg = 0.0
    for i, item_id in enumerate(retrieved_k, 1):
        if item_id in relevant_items:
            # Binary relevance: 1 if relevant, 0 otherwise
            relevance = 1
            dcg += relevance / np.log2(i + 1)

    # Calculate IDCG (Ideal DCG)
    # Ideal ranking would have all relevant items at the top
    num_relevant = min(len(relevant_items), k)
    idcg = sum(1.0 / np.log2(i + 1) for i in range(1, num_relevant + 1))

    # Avoid division by zero
    if idcg == 0:
        return 0.0

    ndcg = dcg / idcg
    return ndcg

def calculate_recall_at_k(relevant_items, retrieved_items, k=3):
    """
    Calculate Recall at k

    Args:
        relevant_items: Set of relevant recipe IDs
        retrieved_items: List of retrieved recipe IDs
        k: Number of top results to consider

    Returns:
        Recall@k score (0 to 1)
    """
    if len(relevant_items) == 0:
        return 0.0

    # Get top k retrieved items
    retrieved_k = set(retrieved_items[:k])

    # Count how many relevant items were retrieved
    retrieved_relevant = len(relevant_items.intersection(retrieved_k))

    # Recall = (retrieved relevant) / (total relevant)
    recall = retrieved_relevant / len(relevant_items)
    return recall

def identify_relevant_recipes(query, recipes, threshold=0.15):
    """
    Identify relevant recipes based on keywords in query

    This is a simple heuristic for demonstration purposes.
    In a real evaluation, you would have manually labeled relevant recipes.

    Args:
        query: User query string
        recipes: List of recipe dictionaries
        threshold: Minimum relevance score to consider relevant

    Returns:
        Set of relevant recipe IDs
    """
    relevant = set()

    # Extract keywords from query (simplified)
    query_lower = query.lower()
    keywords = set(query_lower.split())

    # Remove common words
    stop_words = {'a', 'an', 'the', 'me', 'show', 'give', 'list', 'what', 'is', 'with', 'for'}
    keywords = keywords - stop_words

    for recipe in recipes:
        # Check if recipe matches query keywords
        recipe_text = f"{recipe.get('title', '')} {recipe.get('tags', '')}".lower()

        # Count keyword matches
        matches = sum(1 for kw in keywords if kw in recipe_text)

        # Consider relevant if has keyword matches and above threshold relevance
        if matches > 0 and recipe.get('relevance_score', 0) >= threshold:
            relevant.add(recipe['recipe_id'])

    return relevant

def evaluate_retrieval_performance(results_file='../evaluation/test_results.json', k=3):
    """
    Evaluate retrieval performance on test results

    Args:
        results_file: Path to test results JSON
        k: Number of top results to evaluate

    Returns:
        Dictionary with evaluation metrics
    """
    print("="*70)
    print("Retrieval Performance Evaluation")
    print("="*70)

    # Load test results
    with open(results_file, 'r') as f:
        results = json.load(f)

    print(f"\nLoaded {len(results)} test queries")
    print(f"Evaluating top-{k} retrieval performance...\n")

    # Calculate metrics for each query
    ndcg_scores = []
    recall_scores = []
    query_metrics = []

    for i, result in enumerate(results, 1):
        query = result['query']
        retrieved_recipes = result['retrieved_recipes']

        # Get retrieved recipe IDs (in order)
        retrieved_ids = [r['recipe_id'] for r in retrieved_recipes]

        # Identify relevant recipes (using heuristic)
        relevant_ids = identify_relevant_recipes(query, retrieved_recipes)

        # Calculate metrics
        if len(relevant_ids) > 0:
            ndcg = calculate_ndcg_at_k(relevant_ids, retrieved_ids, k)
            recall = calculate_recall_at_k(relevant_ids, retrieved_ids, k)
        else:
            # If no relevant items identified, skip this query
            continue

        ndcg_scores.append(ndcg)
        recall_scores.append(recall)

        query_metrics.append({
            'query': query,
            'ndcg@3': round(ndcg, 3),
            'recall@3': round(recall, 3),
            'num_relevant': len(relevant_ids),
            'num_retrieved': len(retrieved_ids)
        })

        print(f"{i}. {query[:50]}...")
        print(f"   NDCG@{k}: {ndcg:.3f} | Recall@{k}: {recall:.3f} | Relevant: {len(relevant_ids)}")

    # Calculate average metrics
    avg_ndcg = np.mean(ndcg_scores) if ndcg_scores else 0
    avg_recall = np.mean(recall_scores) if recall_scores else 0

    print("\n" + "="*70)
    print("Summary Statistics")
    print("="*70)
    print(f"Average NDCG@{k}:  {avg_ndcg:.3f}")
    print(f"Average Recall@{k}: {avg_recall:.3f}")
    print(f"Queries evaluated: {len(ndcg_scores)}")
    print("="*70)

    # Save detailed results
    evaluation_results = {
        'summary': {
            'avg_ndcg_at_3': round(avg_ndcg, 3),
            'avg_recall_at_3': round(avg_recall, 3),
            'num_queries': len(ndcg_scores),
            'k': k
        },
        'per_query_metrics': query_metrics
    }

    output_file = '../evaluation/retrieval_metrics.json'
    with open(output_file, 'w') as f:
        json.dump(evaluation_results, f, indent=2)

    print(f"\n✓ Detailed metrics saved to: {output_file}")

    return evaluation_results

def print_interpretation(avg_ndcg, avg_recall):
    """Print interpretation of metrics"""
    print("\n" + "="*70)
    print("Interpretation")
    print("="*70)

    print("\nNDCG@3 (Normalized Discounted Cumulative Gain):")
    if avg_ndcg >= 0.8:
        print("  ✓ Excellent - Retrieval is highly effective")
    elif avg_ndcg >= 0.6:
        print("  ✓ Good - Retrieval performs well")
    elif avg_ndcg >= 0.4:
        print("  ~ Fair - Retrieval is acceptable but could improve")
    else:
        print("  ✗ Poor - Retrieval needs improvement")

    print(f"\n  Score: {avg_ndcg:.3f}/1.0")
    print("  (Higher is better, 1.0 is perfect)")

    print("\nRecall@3:")
    if avg_recall >= 0.8:
        print("  ✓ Excellent - Most relevant recipes are retrieved")
    elif avg_recall >= 0.6:
        print("  ✓ Good - Majority of relevant recipes retrieved")
    elif avg_recall >= 0.4:
        print("  ~ Fair - Some relevant recipes retrieved")
    else:
        print("  ✗ Poor - Few relevant recipes retrieved")

    print(f"\n  Score: {avg_recall:.3f}/1.0")
    print("  (Percentage of relevant recipes found in top 3)")
    print("="*70)

if __name__ == "__main__":
    # Run evaluation
    results = evaluate_retrieval_performance(k=3)

    # Print interpretation
    print_interpretation(
        results['summary']['avg_ndcg_at_3'],
        results['summary']['avg_recall_at_3']
    )

    print("\n✓ Evaluation complete!")
