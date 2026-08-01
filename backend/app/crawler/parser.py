import json
import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from app.crawler.selectors.linkedin import LinkedInSelectors

class LeadParser:
    @staticmethod
    def _extract_text(soup: BeautifulSoup, selectors: List[str], separator=" ", strip=True) -> str:
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(separator=separator, strip=strip)
        return ""

    @staticmethod
    def _extract_href(soup: BeautifulSoup, selectors: List[str]) -> str:
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem and elem.has_attr("href"):
                return elem["href"]
        return ""

    @staticmethod
    def parse_linkedin_post(
        html_content: str,
        exact_post_url: str | None = None,
        timestamp_str: str | None = None
    ) -> Dict[str, Any]:
        """
        Takes raw HTML from a LinkedIn post and normalizes it.
        Iterates over a list of selectors to be resilient against DOM changes.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        
        author_url = LeadParser._extract_href(soup, LinkedInSelectors.AUTHOR_URL) or "https://linkedin.com"
        author_name = LeadParser._extract_text(soup, LinkedInSelectors.AUTHOR_NAME)
        
        if not author_name or author_name == "Unknown Author":
            # Extract from URL slug if available (e.g. /in/tanmaydhake/ -> Tanmaydhake)
            if "/in/" in author_url:
                slug = author_url.split("/in/")[-1].strip("/").split("?")[0].replace("-", " ")
                author_name = slug.title() if slug else "Unknown Author"
            else:
                author_name = "Unknown Author"

        author_title = LeadParser._extract_text(soup, LinkedInSelectors.AUTHOR_TITLE) or "Unknown Title"
        post_text = LeadParser._extract_text(soup, LinkedInSelectors.POST_TEXT, separator="\n")
        
        # Determine exact post URL
        if exact_post_url and exact_post_url.startswith("http"):
            post_url = exact_post_url.split("?")[0] # Clean tracking params
        else:
            post_url = LeadParser._extract_href(soup, LinkedInSelectors.POST_URL)
            if not post_url:
                urn_match = re.search(r'(urn:li:(?:activity|share|ugcPost):\d+)', html_content)
                if urn_match:
                    post_url = f"https://www.linkedin.com/feed/update/{urn_match.group(1)}/"
                elif "/in/" in author_url:
                    clean_author_url = author_url.split("?")[0].rstrip("/")
                    post_url = f"{clean_author_url}/recent-activity/all/"
                else:
                    post_url = author_url

        # Extract/clean timestamp
        published_at_str = None
        if timestamp_str:
            time_match = re.search(r'\b(\d+[mhdwy])\b', timestamp_str)
            if time_match:
                published_at_str = time_match.group(1)
            else:
                published_at_str = timestamp_str.split("•")[0].strip()

        return {
            "author_name": author_name,
            "author_url": author_url,
            "author_title": author_title,
            "post_url": post_url,
            "post_text": post_text,
            "published_at": None,
            "normalized_data": {
                "author": author_name,
                "title": author_title,
                "text": post_text,
                "published_at_str": published_at_str
            },
            "raw_payload": {"html": html_content[:2000]} # Limit payload size
        }
