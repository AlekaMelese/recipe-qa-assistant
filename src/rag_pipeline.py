"""
RAG Pipeline - Retrieval Augmented Generation for Recipe Q&A
Combines retrieval with LLM to answer user questions
"""

import os
import json
from retrieval import RecipeRetriever


class RecipeRAG:
    """RAG system for recipe question answering"""

    def __init__(
        self,
        recipes_path="../data/recipes_subset.json",
        llm_provider="anthropic",  # or "openai"
        model_name=None,
        api_key=None
    ):
        """
        Initialize RAG system

        Args:
            recipes_path: Path to recipe data
            llm_provider: "anthropic" or "openai"
            model_name: Model to use (default: claude-3-haiku for anthropic, gpt-3.5-turbo for openai)
            api_key: API key (or set via environment variable)
        """
        # Initialize retriever
        self.retriever = RecipeRetriever(recipes_path)

        # Set up LLM
        self.llm_provider = llm_provider.lower()
        self.api_key = api_key or self._get_api_key()

        # Set default models
        if model_name is None:
            if self.llm_provider == "anthropic":
                self.model_name = "claude-3-haiku-20240307"
            else:
                self.model_name = "gpt-3.5-turbo"
        else:
            self.model_name = model_name

        # Initialize LLM client


        self._init_llm_client()

        print(f"✓ RAG system initialized with {self.llm_provider} ({self.model_name})")

    def _get_api_key(self):
        """Get API key from environment variables"""
        if self.llm_provider == "anthropic":
            key = os.environ.get("ANTHROPIC_API_KEY")
            if not key:
                raise ValueError(
                    "ANTHROPIC_API_KEY not found. "
                    "Set it via: export ANTHROPIC_API_KEY='your-key'"
                )
        elif self.llm_provider == "openai":
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise ValueError(
                    "OPENAI_API_KEY not found. "
                    "Set it via: export OPENAI_API_KEY='your-key'"
                )
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")

        return key

    def _init_llm_client(self):
        """Initialize LLM client based on provider"""
        if self.llm_provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        elif self.llm_provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")

    def _format_recipes_for_prompt(self, recipes):
        """Format retrieved recipes for LLM context"""
        context_parts = []

        for i, recipe in enumerate(recipes, 1):
            parts = [f"Recipe {i}: {recipe.get('title', 'N/A')}"]

            if recipe.get('tags'):
                parts.append(f"  Tags: {recipe['tags']}")

            if recipe.get('ingredients'):
                # Truncate long ingredient lists
                ingredients = str(recipe['ingredients'])
                if len(ingredients) > 300:
                    ingredients = ingredients[:300] + "..."
                parts.append(f"  Ingredients: {ingredients}")

            if recipe.get('duration'):
                parts.append(f"  Duration: {recipe['duration']} minutes")

            if recipe.get('calories'):
                parts.append(f"  Calories: {recipe['calories']:.1f} cal")

            if recipe.get('health_category'):
                parts.append(f"  Health: {recipe['health_category']}")

            context_parts.append("\n".join(parts))

        return "\n\n".join(context_parts)

    def _create_prompt(self, user_query, retrieved_recipes):
        """Create prompt for LLM"""
        # Format recipes as context
        context = self._format_recipes_for_prompt(retrieved_recipes)

        # System instruction
        system_prompt = """You are a helpful recipe assistant. Answer user questions about recipes using ONLY the information provided in the CONTEXT below.

Guidelines:
- Provide concise, natural answers (1-3 sentences)
- Mention specific recipe titles when relevant
- If the context doesn't contain relevant recipes, say so
- Focus on answering the specific question asked
- Use friendly, conversational tone"""

        # User message with context and question
        user_message = f"""CONTEXT (Retrieved Recipes):
{context}

USER QUESTION: {user_query}

Please answer the question based on the recipes provided above."""

        return system_prompt, user_message

    def _call_llm(self, system_prompt, user_message):
        """Call LLM API and get response"""
        if self.llm_provider == "anthropic":
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            return response.content[0].text

        elif self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model_name,
                max_tokens=500,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content

    def answer_query(self, user_query, k=5, verbose=True):
        """
        Answer user query using RAG pipeline

        Args:
            user_query (str): User's question
            k (int): Number of recipes to retrieve
            verbose (bool): Print detailed output

        Returns:
            dict: Answer, retrieved recipes, and metadata
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Query: {user_query}")
            print(f"{'='*60}\n")

        # Step 1: Retrieve relevant recipes
        if verbose:
            print("Step 1: Retrieving relevant recipes...")

        retrieved_recipes = self.retriever.retrieve_recipes(user_query, k=k)

        if verbose:
            print(f"✓ Retrieved {len(retrieved_recipes)} recipes\n")
            for i, recipe in enumerate(retrieved_recipes, 1):
                print(f"  {i}. {recipe['title']} (score: {recipe['relevance_score']:.3f})")
            print()

        # Step 2: Create prompt
        if verbose:
            print("Step 2: Creating prompt for LLM...")

        system_prompt, user_message = self._create_prompt(user_query, retrieved_recipes)

        if verbose:
            print("✓ Prompt created\n")

        # Step 3: Call LLM
        if verbose:
            print("Step 3: Generating answer with LLM...")

        answer = self._call_llm(system_prompt, user_message)

        if verbose:
            print(f"✓ Answer generated\n")
            print(f"{'='*60}")
            print("ANSWER:")
            print(f"{'='*60}")
            print(answer)
            print(f"{'='*60}\n")

        # Return complete result
        return {
            "query": user_query,
            "answer": answer,
            "retrieved_recipes": retrieved_recipes,
            "num_recipes_retrieved": len(retrieved_recipes),
            "llm_provider": self.llm_provider,
            "model": self.model_name
        }


# Standalone function for easy use
def answer_query(
    query,
    k=5,
    recipes_path="../data/recipes_subset.json",
    llm_provider="anthropic",
    api_key=None
):
    """
    Answer query using RAG (standalone function)

    Args:
        query (str): User question
        k (int): Number of recipes to retrieve
        recipes_path (str): Path to recipe data
        llm_provider (str): "anthropic" or "openai"
        api_key (str): API key

    Returns:
        dict: Answer and metadata
    """
    rag = RecipeRAG(recipes_path, llm_provider, api_key=api_key)
    return rag.answer_query(query, k=k)


# Test the RAG system
if __name__ == "__main__":
    print("="*60)
    print("Testing RAG Pipeline")
    print("="*60)
    print("\nNote: You need to set ANTHROPIC_API_KEY or OPENAI_API_KEY")
    print("export ANTHROPIC_API_KEY='your-key'")
    print("export OPENAI_API_KEY='your-key'\n")

    try:
        # Initialize RAG with API key from environment variable
        import os
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        rag = RecipeRAG(llm_provider="anthropic", api_key=api_key)

        # Test queries
        test_queries = [
            "Show me a quick vegetarian pasta recipe",
            "What's a low-calorie dinner option?",
            "Suggest a healthy breakfast",
        ]

        for query in test_queries:
            result = rag.answer_query(query, k=3)
            print()

    except ValueError as e:
        print(f"\n⚠️  {e}")
        print("\nTo test the system, set your API key:")
        print("  export ANTHROPIC_API_KEY='your-key'")
        print("  or")
        print("  export OPENAI_API_KEY='your-key'")
