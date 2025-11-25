"""
Generate Sample Interaction Log
Creates 5-10 example dialogues showing typical queries and system responses
"""

import json

def create_interaction_log():
    """
    Create formatted interaction log from test results
    Shows sample dialogues for report/presentation
    """
    print("="*70)
    print("Generating Sample Interaction Log")
    print("="*70)

    # Load test results
    with open('../evaluation/test_results.json', 'r') as f:
        results = json.load(f)

    # Select 8 representative examples (diverse query types)
    selected_indices = [0, 1, 2, 3, 4, 6, 9, 13]  # Varied queries
    selected_results = [results[i] for i in selected_indices if i < len(results)]

    # Create text log
    log_content = []
    log_content.append("="*70)
    log_content.append("SAMPLE INTERACTION LOG")
    log_content.append("Recipe Q&A Assistant with RAG")
    log_content.append("="*70)
    log_content.append("")
    log_content.append("This log demonstrates typical user interactions with the")
    log_content.append("conversational recipe Q&A assistant.")
    log_content.append("")

    for i, result in enumerate(selected_results, 1):
        log_content.append("="*70)
        log_content.append(f"Interaction {i}")
        log_content.append("="*70)
        log_content.append("")

        # User query
        log_content.append("USER:")
        log_content.append(f"  {result['query']}")
        log_content.append("")

        # Retrieved recipes (top 3)
        log_content.append("SYSTEM RETRIEVAL (Top 3 Recipes):")
        for j, recipe in enumerate(result['retrieved_recipes'][:3], 1):
            log_content.append(f"  {j}. {recipe['title'].title()}")
            log_content.append(f"     Calories: {recipe.get('calories', 'N/A')}, "
                             f"Duration: {recipe.get('duration', 'N/A')} min, "
                             f"Relevance: {recipe.get('relevance_score', 0):.3f}")
        log_content.append("")

        # System answer
        log_content.append("ASSISTANT:")
        log_content.append(f"  {result['answer']}")
        log_content.append("")

    # Add summary statistics
    log_content.append("")
    log_content.append("="*70)
    log_content.append("Summary Statistics")
    log_content.append("="*70)
    log_content.append(f"Total interactions shown: {len(selected_results)}")
    log_content.append(f"Average recipes retrieved per query: 5")
    log_content.append(f"LLM Model: {results[0]['model']}")
    log_content.append(f"Retrieval Method: TF-IDF (scikit-learn)")
    log_content.append("="*70)

    # Save to file
    output_file = '../evaluation/sample_interaction_log.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_content))

    print(f"✓ Created interaction log with {len(selected_results)} examples")
    print(f"✓ Saved to: {output_file}")

    # Also print to console
    print("\n" + '\n'.join(log_content[:50]))  # Print first part
    print("\n... (see full log in file)")

    # Create JSON version for programmatic access
    json_log = {
        "metadata": {
            "total_interactions": len(selected_results),
            "model": results[0]['model'],
            "retrieval_method": "TF-IDF"
        },
        "interactions": []
    }

    for i, result in enumerate(selected_results, 1):
        interaction = {
            "interaction_id": i,
            "user_query": result['query'],
            "retrieved_recipes": [
                {
                    "rank": j,
                    "title": r['title'],
                    "calories": r.get('calories'),
                    "duration": r.get('duration'),
                    "relevance_score": r.get('relevance_score')
                }
                for j, r in enumerate(result['retrieved_recipes'][:3], 1)
            ],
            "assistant_response": result['answer']
        }
        json_log["interactions"].append(interaction)

    output_json = '../evaluation/sample_interaction_log.json'
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(json_log, f, indent=2, default=str)

    print(f"✓ JSON version saved to: {output_json}")

    return selected_results

if __name__ == "__main__":
    create_interaction_log()
    print("\n✓ Sample interaction log generation complete!")
