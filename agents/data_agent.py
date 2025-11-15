"""
Reviewer Agent for Coffeeverse AI Automation Platform

This agent is responsible for fact-checking, style verification, and quality assurance.
Role: Validate and refine outputs from other agents to ensure accuracy and coherence.
"""

from typing import Dict, Any, List
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class ReviewerAgent:
    def __init__(self, model: str = "gpt-4"):
        """
        Initialize the Reviewer Agent with specified LLM.
        
        :param model: Language model to use for review
        """
        self.llm = ChatOpenAI(model_name=model)
        self.fact_check_prompt = PromptTemplate(
            input_variables=["report", "sources"],
            template="""
            Fact-check the following report against the provided sources:
            
            Report: {report}
            Sources: {sources}
            
            Provide a detailed review highlighting:
            1. Factual accuracy
            2. Potential inaccuracies or misrepresentations
            3. Suggestions for improvement
            
            Review:
            """
        )
        self.fact_check_chain = LLMChain(llm=self.llm, prompt=self.fact_check_prompt)
    
    def fact_check(self, report: str, sources: List[str]) -> Dict[str, Any]:
        """
        Perform fact-checking on the generated report.
        
        :param report: Report to fact-check
        :param sources: List of source documents
        :return: Fact-checking results
        """
        review = self.fact_check_chain.run(report=report, sources=" | ".join(sources))
        
        return {
            "original_report": report,
            "review": review,
            "status": self._determine_review_status(review)
        }
    
    def _determine_review_status(self, review: str) -> str:
        """
        Determine the overall status of the review.
        
        :param review: Fact-checking review text
        :return: Review status
        """
        # Simple heuristic for review status
        if "no significant issues" in review.lower():
            return "APPROVED"
        elif "minor corrections" in review.lower():
            return "NEEDS_MINOR_REVISION"
        else:
            return "NEEDS_MAJOR_REVISION"

    def run(self, report: Dict[str, Any], sources: List[str]) -> Dict[str, Any]:
        """
        Execute review task.
        
        :param report: Report to review
        :param sources: Source documents for fact-checking
        :return: Review results
        """
        fact_check_result = self.fact_check(report.get('summary', ''), sources)
        
        return {
            "review": fact_check_result,
            "status": fact_check_result['status']
        }

# Example usage
if __name__ == "__main__":
    agent = ReviewerAgent()
    sample_report = {
        "summary": "AI is revolutionizing multiple industries with advanced machine learning techniques."
    }
    sample_sources = [
        "Recent AI research papers",
        "Technology industry reports"
    ]
    print(agent.run(sample_report, sample_sources))
