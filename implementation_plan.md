# AFO Kingdom Implementation Plan: Active RAG & Reflexive Learning

## Active Agentic RAG (Shadow to Light)

### Goal Description (Active RAG)

Transition the "Shadow Mode" RAG (which only logged potential actions) into an "Active Agent" that directly handles user queries on the `/api/chat` endpoint. This requires implementing a "System 2" thinking agent that can plan, search, and reason before answering.

### User Review Required (Active RAG)

> [!IMPORTANT]
> I will be intercepting the `/api/chat` endpoint.
> Currently, it might be using a simple LLM call or dummy response. Verification of `test_api_chat.py` suggests it expects specific formats. I must ensure backward compatibility with the frontend's expected format.

### Proposed Changes (Active RAG)

#### Packages

##### [NEW] [rag_active_agent.py](file:///Users/brnestrm/AFO_Kingdom/packages/afo-core/AFO/dspy/rag_active_agent.py)

- A specialized DSPy module for "Active RAG":
  - **Signature**: `Question -> Plan, SearchQueries, Reasoning, Answer`
  - **Logic**:
    1. Receive user query.
    2. Generate a search plan (or "Thought").
    3. Execute retrieval (using the GraphRAG/Obsidian retrievers we built in TICKET-018).
    4. Synthesize answer.

##### [MODIFY] [system_stream.py](file:///Users/brnestrm/AFO_Kingdom/packages/afo-core/AFO/api/routes/system_stream.py)

- Or whichever file handles the actual chat logic (investigation pending).
- Replace simple LLM call with `RagActiveAgent.forward()`.

### Verification Plan (Active RAG)

#### Automated Tests

- Create `scripts/verify_active_rag.py`
  - Send a complex query (e.g., "What is the Trinity Score trend?").
  - Verify the response contains "evidence" or specific data from the RAG store.

---

## Reflexive Learning (Hot-Swap Deployment)

### Goal Description (Hot-Swap)

Bridge the gap between the "Optimization Engine" (MIPROv2) and the "Runtime System" (CommanderBriefing). Currently, optimized JSON files effectively sit on the shelf. We need the runtime modules to automatically load these optimized weights/instructions when available.

### User Review Required (Hot-Swap)

> [!IMPORTANT]
> I will implement "Boot-Swap" first: checking for the optimized file *at module initialization*.
> True "Hot-Swap" (runtime reload without restart) requires a reload trigger or periodic check, which introduces complexity. I will focus on the initialization load first as it covers 90% of the value (restart to upgrade).

### Proposed Changes (Hot-Swap)

#### Packages

##### [MODIFY] [commander_briefing.py](file:///Users/brnestrm/AFO_Kingdom/packages/afo-core/AFO/dspy/commander_briefing.py)

- Update `CommanderBriefing.__init__`:
  - Check for existence of `data/dspy/compiled_commander_briefing.v2.json`.
  - If found, call `self.load(path)`.
  - Log the successful load (or failure).

#### Scripts

##### [NEW] [verify_hot_swap.py](file:///Users/brnestrm/AFO_Kingdom/scripts/verify_hot_swap.py)

- A script that:
  1. Instantiates `CommanderBriefing`.
  2. Checks if it has loaded the optimized state (by inspecting internal state or log output).
  3. Prints verification result.

### Verification Plan (Hot-Swap)

#### Automated Tests

- Run `python scripts/verify_hot_swap.py`
  - Expectation: It should print "✅ Optimized State Loaded".
