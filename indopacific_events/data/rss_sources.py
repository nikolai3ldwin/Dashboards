# rss_sources.py
"""
Configuration file for RSS feed sources used in the Indo-Pacific Dashboard.
"""

# RSS feed sources with their display names
RSS_FEEDS = [
    # Pacific Region Sources
    ("https://www.rnz.co.nz/rss/pacific.xml", "RNZ Pacific"),
    ("https://www.lowyinstitute.org/the-interpreter/rss.xml", "The Interpreter"),
    ("https://www.eastasiaforum.org/feed/", "East Asia Forum"),
    
    # Regional Analysis & Policy
    ("https://thediplomat.com/feed/", "The Diplomat"),
    ("https://www.iiss.org/publications/feed/strategic-comments", "IISS Strategic Comments"),
    ("https://www.aspistrategist.org.au/feed/", "ASPI Strategist"),
    
    # Major News Services
    ("https://asiapacificreport.nz/feed/", "Asia Pacific Report"),
    ("https://www.scmp.com/rss/91/feed", "South China Morning Post"),
    ("https://news.usni.org/category/news-analysis/feed", "USNI News"),
    ("https://www.channelnewsasia.com/api/v1/rss-outbound-feed/asia", "Channel News Asia"),
    
    # Security & Defense
    ("https://www.defensenews.com/arc/outboundfeeds/rss/category/global/asia-pacific/", "Defense News Asia-Pacific"),
    ("https://breakingdefense.com/category/global/asia/feed/", "Breaking Defense Asia"),
    ("https://www.csis.org/programs/regional/pacific-partners-initiative/rss.xml", "CSIS Pacific Partners"),
    
    # Business & Economics
    ("https://www.eastasiaforum.org/topics/economics/feed/", "East Asia Forum Economics"),
    ("https://www.business-standard.com/rss/international-116.rss", "Business Standard International"),
    
    # Specialized Regional Sources
    ("https://www.abc.net.au/news/feed/12840718/rss.xml", "ABC Pacific"),
    ("https://www.pacificislandtimes.com/rss", "Pacific Island Times"),
    ("https://islandsbusiness.com/feed", "Islands Business"),
    ("https://www.devdiscourse.com/rss-feed/191-indo-pacific", "Devdiscourse Indo-Pacific"),
    
    # Additional Sources
    ("https://www.policyforum.net/feed/", "Asia & Pacific Policy Society"),
    ("https://www.pacforum.org/feed", "Pacific Forum"),
    
    # Specific Country Focus (New Caledonia, Wallis & Futuna)
    ("https://la1ere.francetvinfo.fr/corse/rss", "France Info Outre-Mer"),
    ("https://news.pngfacts.com/feeds/posts/default", "PNG Facts"),
    ("https://www.solomonstarnews.com/feed", "Solomon Star News")
]

# Optional configuration settings for feed fetching
FEED_CONFIG = {
    "cache_ttl": 3600,  # Time (in seconds) to cache feeds before refreshing
    "timeout": 10,      # HTTP request timeout in seconds
    "max_retries": 3,   # Maximum number of retry attempts
    "retry_delay": 1    # Delay between retries in seconds
}

# Group sources by category for UI organization
SOURCE_CATEGORIES = {
    "Pacific Regional": [
        "RNZ Pacific", 
        "The Interpreter", 
        "ABC Pacific", 
        "Pacific Island Times",
        "Islands Business"
    ],
    "Analysis & Policy": [
        "The Diplomat", 
        "IISS Strategic Comments", 
        "ASPI Strategist",
        "Asia & Pacific Policy Society",
        "Pacific Forum"
    ],
    "News Services": [
        "Asia Pacific Report",
        "South China Morning Post",
        "Channel News Asia"
    ],
    "Security & Defense": [
        "USNI News",
        "Defense News Asia-Pacific",
        "Breaking Defense Asia",
        "CSIS Pacific Partners"
    ],
    "Business & Economics": [
        "East Asia Forum Economics",
        "Business Standard International"
    ],
    "Country-Specific": [
        "France Info Outre-Mer",
        "PNG Facts",
        "Solomon Star News"
    ]
}
