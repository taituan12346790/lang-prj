# Multi-Agent Architecture Documentation

## Overview
The system implements a **true multi-agent architecture** for language learning support. Each specialized AI Agent handles a specific domain of learning.

## Agent Structure

### 1. Base Agent (`app/agents/base_agent.py`)
- Abstract base class for all AI Agents
- Defines common interface and error handling
- Ensures consistency across all agents

### 2. Three Specialized Agents

#### GrammarAgent (`app/agents/grammar_agent.py`)
**Role:** Grammar analysis and error correction

**Responsibilities:**
- Analyze student writing for grammar errors
- Classify errors by type (verb tense, preposition, word order, etc.)
- Provide explanations in Vietnamese
- Suggest personalized corrections based on student's known weaknesses

**Input Parameters:**
```python
{
    "content": "Student's text to check",
    "target_lang": "English",  # Target learning language
    "teaching_lang": "Vietnamese",  # Explanation language
    "weaknesses": ["verb_tense", "prepositions"]  # Known weak areas
}
```

**Output:**
```python
{
    "success": True/False,
    "errors": [...],
    "explanations": [...],
    "suggestions": [...]
}
```

#### ExerciseAgent (`app/agents/exercise_agent.py`)
**Role:** Adaptive exercise generation

**Responsibilities:**
- Generate exercises based on CEFR level (A1-C2)
- Adapt difficulty based on student performance
- Create topic-specific practice problems
- Focus on identified weak areas

**Input Parameters:**
```python
{
    "topic": "present_perfect",  # Learning topic
    "cefr_level": "B1",  # Current CEFR level
    "weaknesses": ["verb_tense"],  # Areas to focus on
    "num": 5,  # Number of exercises to generate
    "lesson_type": "grammar"  # Type of lesson
}
```

**Output:**
```python
{
    "success": True/False,
    "exercises": [
        {
            "question": "...",
            "correct_answer": "...",
            "options": ["..."],
            "explanation": "..."
        }
    ]
}
```

#### TranslatorAgent (`app/agents/translator_agent.py`)
**Role:** Translation and vocabulary support

**Responsibilities:**
- Translate text between languages
- Provide contextual vocabulary explanations
- Handle idioms and expressions
- Support bilingual learning

**Input Parameters:**
```python
{
    "content": "Text to translate",
    "source_lang": "English",
    "target_lang": "Vietnamese",
    "context": "Optional context for better translation"
}
```

**Output:**
```python
{
    "success": True/False,
    "original_text": "...",
    "translated_text": "...",
    "explanations": [...]
}
```

## How Agents Work

### 1. Registration
When the application starts, `register_all_tools()` in `app/core/register_tools.py`:
- Creates instances of each tool (GrammarChecker, ExerciseGenerator, TranslatorTool)
- Wraps each tool with its corresponding AI Agent
- Registers agents in the tool registry with multiple aliases

### 2. Execution Flow
```
Pipeline/Orchestrator
    ↓
Tool Registry
    ↓
AI Agent (e.g., GrammarAgent)
    ↓
Tool Instance (e.g., GrammarChecker)
    ↓
LLM (Groq) or processing logic
    ↓
Result
```

### 3. Error Handling
Each agent implements graceful error handling:
- Catches exceptions
- Returns error details in structured format
- Logs errors for debugging
- Returns sensible defaults

## Integration with System

### In Pipeline (`app/core/pipeline.py`)
Agents are called through the tool registry:
```python
result = await tool_registry.execute("grammar_check", params)
```

### In Routers
When API endpoints need to check grammar:
```python
result = await tool_registry.execute("grammar_check", {
    "content": user_input,
    "target_lang": "English",
    "teaching_lang": "Vietnamese",
    "weaknesses": user_weaknesses
})
```

## Advantages of Multi-Agent Architecture

1. **Separation of Concerns:** Each agent has a single, well-defined responsibility
2. **Maintainability:** Changes to one agent don't affect others
3. **Scalability:** Easy to add new agents (e.g., ListeningAgent, SpeakingAgent)
4. **Testability:** Each agent can be tested independently
5. **Clear Roles:** Matches the logical decomposition of language learning tasks
6. **Documentation:** Each agent clearly documents its purpose and interface

## Future Extensions

Potential new agents:
- **ListeningAgent:** Speech recognition and listening comprehension
- **SpeakingAgent:** Pronunciation analysis and speaking practice
- **WritingAgent:** Advanced essay evaluation and feedback
- **VocabularyAgent:** Spaced repetition and vocabulary management
- **CoordinatorAgent:** Orchestrates multi-agent workflows for complex tasks

## Files Modified/Created

**Created:**
- `app/agents/__init__.py`
- `app/agents/base_agent.py`
- `app/agents/grammar_agent.py`
- `app/agents/exercise_agent.py`
- `app/agents/translator_agent.py`

**Modified:**
- `app/core/register_tools.py`

**Can be deprecated (but kept for backward compatibility):**
- `app/tools/grammar_checker_wrapper.py`
- `app/tools/exercise_generator_wrapper.py`
- `app/tools/translator_wrapper.py`
