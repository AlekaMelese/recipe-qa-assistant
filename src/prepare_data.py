"""
Data Preparation Script
Samples and preprocesses recipe data for RAG Q&A system
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path

# Configuration
RECIPES_PATH = "../../Final/Recipes.csv"
OUTPUT_PATH = "../data/recipes_subset.json"
SAMPLE_SIZE = 1000  # Number of recipes to sample (small subset for class project)

def load_and_sample_recipes(recipes_path, sample_size=5000):
    """Load recipes CSV and sample a subset"""
    print(f"Loading recipes from {recipes_path}...")

    # Read CSV
    df = pd.read_csv(recipes_path)
    print(f"Total recipes loaded: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # Sample recipes
    if len(df) > sample_size:
        df_sample = df.sample(n=sample_size, random_state=42)
        print(f"Sampled {sample_size} recipes")
    else:
        df_sample = df
        print(f"Using all {len(df)} recipes")

    return df_sample

def preprocess_recipes(df):
    """Clean and preprocess recipe data"""
    print("\nPreprocessing recipes...")

    # Select key fields based on project requirements
    # recipe_id, title, tags, ingredients, duration, calories, protein, sugars, sodium, health scores

    key_fields = []
    available_cols = df.columns.tolist()

    # Map common field names
    field_mapping = {
        'recipe_id': ['recipe_id', 'RecipeId', 'id'],
        'title': ['title', 'Name', 'RecipeName'],
        'tags': ['tags', 'Tags', 'RecipeCategory'],
        'ingredients': ['ingredients', 'Ingredients', 'RecipeIngredientParts'],
        'duration': ['duration', 'TotalTime', 'CookTime', 'PrepTime'],
        'calories': ['calories', 'Calories', 'calories [cal]'],
        'protein': ['protein', 'Protein', 'ProteinContent'],
        'sugars': ['sugars', 'Sugar', 'SugarContent'],
        'sodium': ['sodium', 'Sodium', 'SodiumContent'],
    }

    # Find matching columns
    selected_cols = {}
    for field, possible_names in field_mapping.items():
        for name in possible_names:
            if name in available_cols:
                selected_cols[field] = name
                break

    print(f"Selected columns: {selected_cols}")

    # Extract and rename columns
    df_processed = pd.DataFrame()
    for standard_name, actual_name in selected_cols.items():
        df_processed[standard_name] = df[actual_name]

    # Clean text fields (lowercase, strip whitespace)
    text_fields = ['title', 'tags', 'ingredients']
    for field in text_fields:
        if field in df_processed.columns:
            df_processed[field] = df_processed[field].fillna('').astype(str).str.lower().str.strip()

    # Handle numeric fields
    numeric_fields = ['calories', 'protein', 'sugars', 'sodium', 'duration']
    for field in numeric_fields:
        if field in df_processed.columns:
            df_processed[field] = pd.to_numeric(df_processed[field], errors='coerce')

    # Calculate composite health score if available
    if 'calories' in df_processed.columns:
        # Simple health categorization based on calories
        df_processed['health_category'] = pd.cut(
            df_processed['calories'],
            bins=[0, 200, 400, 600, float('inf')],
            labels=['low_calorie', 'moderate', 'high_calorie', 'very_high_calorie']
        )

    # Remove rows with missing essential data
    essential_cols = ['recipe_id', 'title']
    df_processed = df_processed.dropna(subset=[col for col in essential_cols if col in df_processed.columns])

    print(f"Recipes after preprocessing: {len(df_processed)}")
    print(f"Final columns: {list(df_processed.columns)}")

    return df_processed

def create_recipe_text(row):
    """Create searchable text representation for each recipe"""
    # Combine title, tags, and ingredients into one text field
    parts = []

    if 'title' in row and pd.notna(row['title']):
        parts.append(str(row['title']))

    if 'tags' in row and pd.notna(row['tags']):
        parts.append(str(row['tags']))

    if 'ingredients' in row and pd.notna(row['ingredients']):
        parts.append(str(row['ingredients']))

    return " ".join(parts)

def save_recipes(df, output_path):
    """Save processed recipes to JSON"""
    print(f"\nSaving recipes to {output_path}...")

    # Add searchable text field
    df['searchable_text'] = df.apply(create_recipe_text, axis=1)

    # Convert to list of dictionaries
    recipes = df.to_dict('records')

    # Save as JSON
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=2, default=str)

    print(f"✓ Saved {len(recipes)} recipes to {output_path}")

    # Print sample recipe
    print("\nSample recipe:")
    print(json.dumps(recipes[0], indent=2, default=str))

    return recipes

def main():
    """Main data preparation pipeline"""
    print("="*60)
    print("Recipe Data Preparation for RAG Q&A System")
    print("="*60)

    # Step 1: Load and sample
    df = load_and_sample_recipes(RECIPES_PATH, SAMPLE_SIZE)

    # Step 2: Preprocess
    df_processed = preprocess_recipes(df)

    # Step 3: Save
    recipes = save_recipes(df_processed, OUTPUT_PATH)

    print("\n" + "="*60)
    print("✓ Data preparation complete!")
    print(f"✓ Output: {OUTPUT_PATH}")
    print(f"✓ Total recipes: {len(recipes)}")
    print("="*60)

if __name__ == "__main__":
    main()
