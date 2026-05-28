# app/services/service_container.py
"""
Service container with lazy initialization to avoid import-time side effects.
LearningService is expensive to initialize (creates Pipeline, LangGraph, etc),
so we lazy-load it on first use instead of at import time.
"""

_learning_service = None

def get_learning_service():
    """
    Get or lazily initialize the LearningService.
    Called on first chat request, not on import.
    """
    global _learning_service
    if _learning_service is None:
        from app.services.learning_service import LearningService
        _learning_service = LearningService()
    return _learning_service


# For backward compatibility (will be lazy-loaded)
learning_service = None
