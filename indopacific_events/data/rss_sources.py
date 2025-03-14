# rss_sources.py
"""
Updated configuration file for RSS feed sources used in the Indo-Pacific Dashboard.
"""

# RSS feed sources with their display names - updated with working feeds
RSS_FEEDS = [
    # Pacific Region Sources
    ("https://www.rnz.co.nz/rss/pacific.xml", "RNZ Pacific"),
    ("https://www.lowyinstitute.org/the-interpreter/rss", "The Interpreter"),  # Updated URL
    ("https://www.eastasiaforum.org/feed/", "East Asia Forum"),
    
    # Regional Analysis & Policy
    ("https://thediplomat.com/feed/", "The Diplomat"),
    # IISS feed replaced with alternative
    ("https://www.iiss.org/online-analysis/rss", "IISS Analysis"),
    ("https://www.aspistrategist.org.au/feed/", "ASPI Strategist"),
    
    # Major News Services
    ("https://asiapacificreport.nz/feed/", "Asia Pacific Report"),
    # SCMP feed replaced with alternative
    ("https://www.scmp.com/rss/4/feed", "South China Morning Post"),
    # USNI feed replaced with alternative
    ("https://news.usni.org/feed", "USNI News"),
    # CNA feed replaced with alternative
    ("https://api.cna.asia/api/v1/rss/2-8", "Channel News Asia"),
    
    # Security & Defense
    # Defense News feed replaced with alternative
    ("https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml", "Defense News"),
    # Breaking Defense feed replaced with alternative
    ("https://breakingdefense.com/feed/", "Breaking Defense"),
    # CSIS feed replaced with alternative
    ("https://www.csis.org/feed", "CSIS"),
    
    # Business & Economics
    # East Asia Forum Economics feed replaced with general feed
    ("https://www.eastasiaforum.org/feed/", "East Asia Forum Economics"),
    # Business Standard feed replaced with alternative
    ("https://www.business-standard.com/rss/latest.rss", "Business Standard"),
    
    # Specialized Regional Sources
    # ABC Pacific feed replaced with alternative
    ("https://www.abc.net.au/news/feed/52498/rss.xml", "ABC News"),
    # Pacific Island Times feed replaced with alternative
    ("https://pacificnewscenter.com/feed/", "Pacific News Center"),
    # Islands Business feed replaced with alternative
    ("https://www.rnz.co.nz/rss/pacific.xml", "RNZ Islands Business"),
    # Devdiscourse feed replaced with alternative
    ("https://www.devdiscourse.com/rss-feed/30-indo-pacific-region-stories", "Devdiscourse Indo-Pacific"),
    
    # Additional Sources
    ("https://www.policyforum.net/feed/", "Asia & Pacific Policy Society"),
    ("https://pacforum.org/feed", "Pacific Forum"),
    
    # Specific Country Focus (New Caledonia, Wallis & Futuna)
    # France Info feed replaced with alternative
    ("https://www.tahiti-infos.com/xml/syndication.rss", "Tahiti Info"),
    # PNG Facts feed replaced with alternative
    ("https://postcourier.com.pg/feed/", "PNG Post Courier"),
    ("https://www.solomonstarnews.com/feed", "Solomon Star News"),
    
    # Additional reliable sources
    ("https://www.reuters.com/world/asia-pacific/rss", "Reuters Asia Pacific"),
    ("https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml", "New York Times Asia"),
    ("https://www.brookings.edu/topic/asia-pacific/feed/", "Brookings Asia Pacific"),
    ("https://www.rand.org/topics/asia-pacific-region.xml/feed", "RAND Corporation Asia"),
    ("https://www.bangkokpost.com/rss/data/topnews.xml", "Bangkok Post")
]

# Optional configuration settings for feed fetching
FEED_CONFIG = {
    "cache_ttl": 3600,  # Time (in seconds) to cache feeds before refreshing
    "timeout": 15,      # Increased HTTP request timeout in seconds
    "max_retries": 3,   # Maximum number of retry attempts
    "retry_delay": 2    # Delay between retries in seconds
}

# Updated source categories for UI organization
SOURCE_CATEGORIES = {
    "Pacific Regional": [
        "RNZ Pacific", 
        "The Interpreter", 
        "ABC News", 
        "Pacific News Center",
        "RNZ Islands Business",
        "Solomon Star News",
        "PNG Post Courier",
        "Tahiti Info"
    ],
    "Analysis & Policy": [
        "The Diplomat", 
        "IISS Analysis", 
        "ASPI Strategist",
        "Asia & Pacific Policy Society",
        "Pacific Forum",
        "Brookings Asia Pacific",
        "RAND Corporation Asia"
    ],
    "News Services": [
        "Asia Pacific Report",
        "South China Morning Post",
        "Channel News Asia",
        "Reuters Asia Pacific",
        "New York Times Asia",
        "Bangkok Post"
    ],
    "Security & Defense": [
        "USNI News",
        "Defense News",
        "Breaking Defense",
        "CSIS"
    ],
    "Business & Economics": [
        "East Asia Forum Economics",
        "Business Standard",
        "Devdiscourse Indo-Pacific"
    ]
}
