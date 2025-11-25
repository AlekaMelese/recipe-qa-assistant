"""
Simple Conversation Handler
Tracks last query and supports clarifications
"""

from rag_pipeline import RecipeRAG


class ConversationalRecipeAssistant:
    """
    Simple conversational wrapper that tracks last query and results
    Supports follow-up clarifications like "shorter", "with chicken instead"
    """

    def __init__(self, llm_provider="anthropic", api_key=None):
        """Initialize the conversational assistant"""
        self.rag = RecipeRAG(llm_provider=llm_provider, api_key=api_key)
        self.last_query = None
        self.last_results = None
        self.conversation_history = []

    def _is_clarification(self, query):
        """
        Check if query is a clarification/follow-up
        Returns True if query seems like a follow-up
        """
        query_lower = query.lower()

        # Keywords that indicate clarification
        clarification_keywords = [
            'shorter', 'longer', 'faster', 'slower',
            'healthier', 'less healthy', 'more calories', 'fewer calories',
            'with chicken', 'with beef', 'with fish', 'with vegetables',
            'without', 'instead', 'different', 'another',
            'simpler', 'easier', 'harder',
            'vegan', 'vegetarian', 'gluten-free'
        ]

        # Check if any clarification keyword is present
        for keyword in clarification_keywords:
            if keyword in query_lower:
                return True

        # Check if query is very short (likely a clarification)
        if len(query.split()) <= 3:
            return True

        return False

    def _build_clarified_query(self, original_query, clarification):
        """
        Combine original query with clarification

        Args:
            original_query: The previous query
            clarification: The follow-up/clarification

        Returns:
            Modified query string
        """
        clarification_lower = clarification.lower()

        # Handle "with X instead" patterns
        if 'instead' in clarification_lower or 'with' in clarification_lower:
            return f"{original_query}, but {clarification}"

        # Handle time-based clarifications
        if any(word in clarification_lower for word in ['shorter', 'faster', 'quicker']):
            return f"{original_query} that takes less time"
        if any(word in clarification_lower for word in ['longer', 'slower']):
            return f"{original_query} that takes more time"

        # Handle health-based clarifications
        if 'healthier' in clarification_lower or 'healthy' in clarification_lower:
            return f"{original_query} that is healthier"
        if 'calorie' in clarification_lower:
            if 'fewer' in clarification_lower or 'less' in clarification_lower or 'low' in clarification_lower:
                return f"{original_query} with fewer calories"
            else:
                return f"{original_query} with more calories"

        # Default: append clarification
        return f"{original_query}, {clarification}"

    def ask(self, query, k=5):
        """
        Ask a question with conversation context

        Args:
            query: User query (can be new or follow-up)
            k: Number of recipes to retrieve

        Returns:
            dict: Answer and metadata
        """
        # Check if this is a clarification
        if self.last_query and self._is_clarification(query):
            print(f"[Detected clarification based on previous query]")
            # Combine with previous query
            modified_query = self._build_clarified_query(self.last_query, query)
            print(f"[Modified query: {modified_query}]")
            actual_query = modified_query
        else:
            actual_query = query

        # Get answer from RAG system
        result = self.rag.answer_query(actual_query, k=k, verbose=True)

        # Store for next turn
        self.last_query = actual_query
        self.last_results = result['retrieved_recipes']

        # Add to conversation history
        self.conversation_history.append({
            'user_input': query,
            'actual_query': actual_query,
            'answer': result['answer'],
            'num_recipes': len(result['retrieved_recipes'])
        })

        return result

    def reset(self):
        """Reset conversation state"""
        self.last_query = None
        self.last_results = None
        print("Conversation reset.")


def interactive_conversation():
    """
    Interactive conversation loop for testing
    """
    print("="*70)
    print("Conversational Recipe Q&A Assistant")
    print("="*70)
    print("\nSupports follow-ups like:")
    print("  'shorter', 'with chicken instead', 'healthier', etc.")
    print("\nCommands:")
    print("  'reset' - Start new conversation")
    print("  'quit' or 'exit' - End session")
    print("="*70 + "\n")

    # Initialize with API key from environment variable
    import os
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set it using: export ANTHROPIC_API_KEY='your-api-key'")
        return
    assistant = ConversationalRecipeAssistant(llm_provider="anthropic", api_key=api_key)

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if user_input.lower() == 'reset':
                assistant.reset()
                continue

            # Ask the assistant
            result = assistant.ask(user_input, k=5)

            print()  # Extra spacing for readability

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


def demo_conversation():
    """
    Demonstrate conversation with predefined examples
    """
    print("="*70)
    print("Conversation Demo")
    print("="*70)

    import os
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set it using: export ANTHROPIC_API_KEY='your-api-key'")
        return
    assistant = ConversationalRecipeAssistant(llm_provider="anthropic", api_key=api_key)

    # Demo conversation
    examples = [
        "Show me a pasta recipe",
        "with chicken instead",  # Clarification
        "and make it healthier",  # Another clarification
    ]

    for query in examples:
        print(f"\n{'='*70}")
        print(f"USER: {query}")
        print(f"{'='*70}")

        result = assistant.ask(query, k=3)
        print()

    print("\n" + "="*70)
    print("Demo conversation complete!")
    print("="*70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        # Run demo
        demo_conversation()
    else:
        # Run interactive
        interactive_conversation()
