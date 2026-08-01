import os
from pathlib import Path
from app.crawler.parser import LeadParser

def test_parse_linkedin_post():
    # Load fixture
    fixture_path = Path(os.path.dirname(__file__)) / "fixtures" / "linkedin_post.html"
    with open(fixture_path, "r") as f:
        html_content = f.read()

    # Parse
    result = LeadParser.parse_linkedin_post(html_content)

    # Assertions
    assert result["author_name"] == "John Doe"
    assert result["author_url"] == "https://www.linkedin.com/in/johndoe"
    assert result["author_title"] == "VP of Engineering at TechCorp"
    assert result["post_url"] == "https://www.linkedin.com/posts/johndoe_ai-python-activity-12345"
    assert "We are building the next generation" in result["post_text"]
    assert result["normalized_data"]["author"] == "John Doe"
    
def test_parse_linkedin_post_fallback():
    # Fallback to defaults when nothing matches
    html_content = "<div><p>Random text</p></div>"
    result = LeadParser.parse_linkedin_post(html_content)
    
    assert result["author_name"] == "Unknown Author"
    assert result["author_url"] == "https://linkedin.com"
    assert result["author_title"] == "Unknown Title"
    assert result["post_url"] == "https://linkedin.com"
    assert result["post_text"] == ""
