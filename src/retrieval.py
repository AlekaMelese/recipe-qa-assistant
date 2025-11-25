"""
Retrieval Module - TF-IDF based recipe retrieval
Implements retrieve_recipes(query, k) function
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path


class RecipeRetriever:
    """TF-IDF based recipe retrieval system"""

    def __init__(self, recipes_path="../data/recipes_subset.json"):
        """
        Initialize retriever with recipe data

        Args:
            recipes_path: Path to JSON file with recipe data
        """
        self.recipes_path = recipes_path
        self.recipes = []
        self.vectorizer = None
        self.tfidf_matrix = None

        # Load recipes
        self._load_recipes()

        # Build TF-IDF index
        self._build_index()

    def _load_recipes(self):
        """Load recipes from JSON file"""
        print(f"Loading recipes from {self.recipes_path}...")

        with open(self.recipes_path, 'r', encoding='utf-8') as f:
            self.recipes = json.load(f)

        print(f"✓ Loaded {len(self.recipes)} recipes")

    def _build_index(self):
        """Build TF-IDF index for recipe retrieval"""
        print("Building TF-IDF index...")

        # Extract searchable text from all recipes
        documents = [recipe.get('searchable_text', '') for recipe in self.recipes]

        # Create TF-IDF vectorizer
        # Using word-level features with 1-2 word n-grams
        self.vectorizer = TfidfVectorizer(
            max_features=5000,  # Limit vocabulary size
            ngram_range=(1, 2),  # Use unigrams and bigrams
            stop_words='english',  # Remove common English words
            lowercase=True,
            min_df=2,  # Ignore terms that appear in less than 2 documents
        )

        # Fit and transform documents to TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)

        print(f"✓ Built TF-IDF index with {self.tfidf_matrix.shape[1]} features")

    def retrieve_recipes(self, query, k=5):
        """
        Retrieve top-k most relevant recipes for a query

        Args:
            query (str): User query (e.g., "quick vegetarian pasta")
            k (int): Number of recipes to retrieve

        Returns:
            list: Top-k recipes with similarity scores
        """
        # Transform query to TF-IDF vector
        query_vector = self.vectorizer.transform([query.lower()])

        # Calculate cosine similarity between query and all recipes
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # Get top-k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]

        # Retrieve recipes with scores
        results = []
        for idx in top_k_indices:
            recipe = self.recipes[idx].copy()
            recipe['relevance_score'] = float(similarities[idx])
            results.append(recipe)

        return results

    def format_recipe_for_display(self, recipe):
        """Format recipe for nice display"""
        output = []
        output.append(f"Title: {recipe.get('title', 'N/A')}")

        if 'tags' in recipe and recipe['tags']:
            output.append(f"Tags: {recipe['tags']}")

        if 'duration' in recipe and recipe['duration']:
            output.append(f"Duration: {recipe['duration']} minutes")

        if 'calories' in recipe and recipe['calories']:
            output.append(f"Calories: {recipe['calories']:.1f} cal")

        if 'health_category' in recipe and recipe['health_category']:
            output.append(f"Health: {recipe['health_category']}")

        if 'relevance_score' in recipe:
            output.append(f"Relevance: {recipe['relevance_score']:.3f}")

        return "\n".join(output)

    def search(self, query, k=5, verbose=True):
        """
        Search for recipes and print results

        Args:
            query (str): User query
            k (int): Number of results
            verbose (bool): Print results

        Returns:
            list: Retrieved recipes
        """
        results = self.retrieve_recipes(query, k)

        if verbose:
            print(f"\nQuery: '{query}'")
            print(f"Found {len(results)} recipes:\n")
            print("="*60)

            for i, recipe in enumerate(results, 1):
                print(f"\n{i}. {self.format_recipe_for_display(recipe)}")
                print("-"*60)

        return results


def retrieve_recipes(query, k=5, recipes_path="../data/recipes_subset.json"):
    """
    Standalone function to retrieve recipes (for easy import)

    Args:
        query (str): User query
        k (int): Number of recipes to retrieve
        recipes_path (str): Path to recipe data

    Returns:
        list: Top-k relevant recipes
    """
    retriever = RecipeRetriever(recipes_path)
    return retriever.retrieve_recipes(query, k)


# Test the retrieval system
if __name__ == "__main__":
    print("="*60)
    print("Testing Recipe Retrieval System")
    print("="*60)

    # Initialize retriever
    retriever = RecipeRetriever()

    # Test queries
    test_queries = [
        "quick vegetarian pasta",
        "low calorie dinner",
        "chocolate dessert",
        "healthy breakfast",
    ]

    for query in test_queries:
        print("\n" + "="*60)
        retriever.search(query, k=3)

    print("\n" + "="*60)
    print("✓ Retrieval system test complete!")
    print("="*60)
