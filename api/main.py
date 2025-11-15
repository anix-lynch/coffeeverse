"""
Unit Tests for Coffeeverse AI Agents

Provides comprehensive testing for individual agents and their core functionalities.
"""

import pytest
from typing import Dict, Any

# Import agents
from agents.research_agent import ResearchAgent
from agents.data_agent import DataAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent

# Fixture for creating agent instances
@pytest.fixture
def research_agent():
    """Fixture for ResearchAgent."""
    return ResearchAgent()

@pytest.fixture
def data_agent():
    """Fixture for DataAgent."""
    return DataAgent()

@pytest.fixture
def writer_agent():
    """Fixture for WriterAgent."""
    return WriterAgent()

@pytest.fixture
def reviewer_agent():
    """Fixture for ReviewerAgent."""
    return ReviewerAgent()

# Research Agent Tests
def test_research_agent_web_search(research_agent):
    """Test web search functionality."""
    query = "AI automation trends"
    results = research_agent.web_search(query)
    
    assert isinstance(results, list), "Web search should return a list of results"
    assert len(results) > 0, "Web search should return non-empty results"

def test_research_agent_run(research_agent):
    """Test overall run method of research agent."""
    task = "Analyze recent developments in machine learning"
    result = research_agent.run(task)
    
    assert isinstance(result, dict), "Run method should return a dictionary"
    assert "web_search" in result, "Result should contain web search results"
    assert "analysis" in result, "Result should contain analysis status"

# Data Agent Tests
def test_data_agent_vector_store(data_agent):
    """Test vector store creation and semantic search."""
    sample_docs = [
        "AI is transforming multiple industries",
        "Machine learning models are becoming more sophisticated",
        "Data science requires interdisciplinary skills"
    ]
    
    data_agent.create_vector_store(sample_docs)
    search_results = data_agent.semantic_search("AI technology", k=2)
    
    assert len(search_results) == 2, "Semantic search should return specified number of results"

def test_data_agent_metrics(data_agent):
    """Test metric analysis functionality."""
    sample_data = [
        {"name": "Project A", "value": 100},
        {"name": "Project B", "value": 200}
    ]
    
    metrics = data_agent.analyze_metrics(sample_data)
    
    assert metrics["total_records"] == 2, "Metrics should count total records"
    assert "keys" in metrics, "Metrics should include keys"

# Writer Agent Tests
def test_writer_agent_summary(writer_agent):
    """Test summary generation."""
    context = "Recent AI developments show significant progress in multimodal learning"
    task = "Summarize key AI trends"
    
    result = writer_agent.run(task, context)
    
    assert isinstance(result, dict), "Run method should return a dictionary"
    assert "report" in result, "Result should contain a report"
    assert "summary" in result["report"], "Report should have a summary"

# Reviewer Agent Tests
def test_reviewer_agent_fact_check(reviewer_agent):
    """Test fact-checking functionality."""
    sample_report = {
        "summary": "AI is revolutionizing multiple industries with advanced machine learning techniques."
    }
    sample_sources = [
        "Recent AI research papers",
        "Technology industry reports"
    ]
    
    result = reviewer_agent.run(sample_report, sample_sources)
    
    assert isinstance(result, dict), "Run method should return a dictionary"
    assert "review" in result, "Result should contain a review"
    assert "status" in result, "Result should have a status"

# Integration Test
def test_agent_workflow():
    """Basic integration test simulating agent workflow."""
    research_agent = ResearchAgent()
    data_agent = DataAgent()
    writer_agent = WriterAgent()
    reviewer_agent = ReviewerAgent()
    
    # Simulate workflow
    task = "Analyze AI automation trends"
    
    # Research stage
    research_result = research_agent.run(task)
    assert research_result, "Research stage should produce results"
    
    # Data processing stage
    data_result = data_agent.run(str(research_result))
    assert data_result, "Data processing stage should produce results"
    
    # Writing stage
    context = str(research_result) + str(data_result)
    writing_result = writer_agent.run(task, context)
    assert writing_result, "Writing stage should produce results"
    
    # Review stage
    review_result = reviewer_agent.run(
        writing_result.get('report', {}), 
        research_result.get('web_search', [])
    )
    assert review_result, "Review stage should produce results"

# Run tests with: pytest tests/test_agents.py
