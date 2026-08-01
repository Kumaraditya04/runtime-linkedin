class LinkedInSelectors:
    SEARCH_INPUT = [
        "input.search-global-typeahead__input",
        ".search-global-typeahead__input"
    ]
    
    POST_CONTAINER = [
        "div[role='listitem']",
        "div[componentkey*='FeedType']",
        ".feed-shared-update-v2",
        "[data-urn*='urn:li:activity:']"
    ]
    
    AUTHOR_NAME = [
        "a[href*='/in/'] span",
        ".update-components-actor__name",
        ".actor-name",
        "[data-test-id='actor-name']"
    ]
    
    AUTHOR_URL = [
        "a[href*='/in/']",
        ".update-components-actor__container-link",
        ".app-aware-link"
    ]
    
    AUTHOR_TITLE = [
        ".update-components-actor__description",
        ".actor-description",
        "[data-test-id='actor-description']"
    ]
    
    POST_TEXT = [
        "[data-testid='expandable-text-box']",
        ".update-components-text",
        ".feed-shared-update-v2__commentary",
        "[data-test-id='post-content']"
    ]
    
    POST_URL = [
        'a[href*="/posts/"]',
        'a[href*="/activity/"]',
        'a[href*="/feed/update/"]'
    ]
