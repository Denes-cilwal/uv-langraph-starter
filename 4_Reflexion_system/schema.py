from pydantic import BaseModel, Field
from typing import List


# Critique schema - identifies problems in the answer
class Reflection(BaseModel):
    """Critical analysis of the answer to identify areas for improvement."""
    
    # What information or details are missing from the answer
    missing: str = Field(description="Critique of what is missing.")
    
    # What information is unnecessary or doesn't belong in the answer
    superfluous: str = Field(description="Critique of what is superfluous") 


# Initial response schema - first answer with self-critique
class AnswerQuestion(BaseModel):
    """Answer the question with self-critique and improvement queries."""

    # The initial ~250 word answer to the question
    answer: str = Field(
        description="~250 word detailed answer to the question.")
    
    # Search queries to research improvements based on the critique
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )
    
    # Critical analysis identifying what's missing and superfluous
    reflection: Reflection = Field(
        description="Your reflection on the initial answer.")


# this revise inherits all base properties including references
class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question."""

    references: List[str] = Field(
        description="Citations motivating your updated answer."
    )



