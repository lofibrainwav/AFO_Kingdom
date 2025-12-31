# Language: ko-KR (AFO SSOT)
import dspy

from AFO.dspy.rag_evidence_graphrag import retrieve_evidence_graphrag


class ActiveRagSignature(dspy.Signature):
    """
    Active Agentic RAG (System 2 Thinking)
    Question -> Plan -> Search -> Reasoning -> Answer
    """

    question = dspy.InputField(desc="User's question or command")
    context = dspy.InputField(desc="Conversation history or manual context", optional=True)
    retrieved_evidence = dspy.InputField(
        desc="Retrieved data from GraphRAG/Obsidian", optional=True
    )

    thought_process = dspy.OutputField(desc="Step-by-step reasoning and search plan")
    answer = dspy.OutputField(desc="Final answer based on retrieved evidence and thoughts")


class RagActiveAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought(ActiveRagSignature)

    def forward(self, question: str, context: str = ""):
        # 1. Active Retrieval using the question
        # In a more advanced version, we'd use a SearchQueryGenerator signature here.
        # For now, we combine question + context hints for better retrieval.
        search_query = question
        if context:
            # Simple heuristic: if context has keywords, append them or let LLM decide
            # To stay 'Agentic', we'll let the retriever handle it, but we can pass more data.
            pass

        evidence = retrieve_evidence_graphrag(search_query, top_k=5)

        # 2. System 2 Thinking (Reasoning over retrieved evidence)
        prediction = self.predict(question=question, context=context, retrieved_evidence=evidence)

        return prediction
