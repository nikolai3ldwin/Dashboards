# importance_keywords.py

IMPORTANT_KEYWORDS = {
    # Political and Diplomatic - Increased Weights
    'crisis': 8, 'conflict': 8, 'treaty': 6, 'agreement': 6, 'election': 6, 'coup': 10,
    'diplomacy': 6, 'sanctions': 8, 'trade war': 8, 'summit': 6, 'negotiation': 6,
    'alliance': 7, 'territorial dispute': 9, 'sovereignty': 7, 'peacekeeping': 6,
    'political reform': 6, 'government collapse': 10, 'referendum': 7, 'secession': 8,

    # Major Powers and Regional Actors - Increased Base Importance
    'US': 7, 'China': 7, 'Russia': 7, 'Japan': 6, 'India': 6, 'Australia': 6,
    'South Korea': 6, 'North Korea': 8, 'ASEAN': 6, 'EU': 6, 'UN': 6,
    'Taiwan': 8, 'Hong Kong': 7, 'Tibet': 7, 'Xinjiang': 7,
    'Indonesia': 6, 'Vietnam': 6, 'Philippines': 6, 'Malaysia': 6, 'Singapore': 6,

    # Military and Security - Highest Weights
    'military': 7, 'defense': 7, 'war': 10, 'terrorism': 9, 'insurgency': 9,
    'nuclear': 10, 'missile': 8, 'cyber attack': 9, 'intelligence': 7,
    'arms race': 8, 'naval exercise': 7, 'joint military exercise': 7,
    'troop deployment': 8, 'military base': 7, 'defense pact': 7, 'arms deal': 7,

    # Economic - Increased for Major Issues
    'trade': 6, 'investment': 6, 'economic crisis': 9, 'recession': 8,
    'currency': 6, 'stock market': 6, 'supply chain': 7, 'belt and road': 7,
    'free trade agreement': 6, 'tariff': 6, 'economic cooperation': 6,
    'financial crisis': 9, 'market crash': 9, 'economic sanctions': 8,

    # Social and Internal Issues - Adjusted Up
    'protest': 8, 'unrest': 8, 'riot': 9, 'human rights': 7, 'censorship': 7,
    'corruption': 7, 'inequality': 6, 'discrimination': 7, 'minority rights': 7,
    'social movement': 7, 'labor strike': 7, 'civil disobedience': 8,

    # Natural Disasters and Environment - Higher Priority
    'disaster': 9, 'earthquake': 9, 'tsunami': 10, 'typhoon': 9, 'flood': 8,
    'drought': 8, 'wildfire': 8, 'climate change': 8, 'global warming': 7,
    'pollution': 6, 'biodiversity': 6, 'deforestation': 7,
    'environmental crisis': 8, 'ecological disaster': 9,

    # Health and Humanitarian - Critical Issues
    'pandemic': 10, 'epidemic': 9, 'outbreak': 8, 'vaccine': 7, 'healthcare': 6,
    'famine': 9, 'hunger': 8, 'poverty': 7, 'refugee': 8, 'humanitarian crisis': 9,
    'disease': 7, 'medical emergency': 8, 'public health': 7,

    # Technology and Innovation - Strategic Importance
    'AI': 7, 'artificial intelligence': 7, '5G': 7, 'quantum computing': 7,
    'space program': 7, 'satellite': 6, 'tech war': 8, 'innovation': 6,
    'cybersecurity': 8, 'data privacy': 7, 'digital economy': 6,

    # Energy and Resources - Critical Infrastructure
    'oil': 7, 'gas': 7, 'renewable energy': 6, 'nuclear power': 8,
    'rare earth minerals': 8, 'energy security': 8, 'resource conflict': 9,
    'energy crisis': 9, 'power shortage': 7,

    # Infrastructure and Development - Base Increased
    'infrastructure': 6, 'development project': 5, 'urbanization': 5,
    'smart city': 5, 'transportation': 5, 'port development': 6,

    # Maritime Issues - Regional Priority
    'south china sea': 9, 'east china sea': 9, 'freedom of navigation': 8,
    'maritime dispute': 9, 'piracy': 7, 'fishing rights': 6,
    'naval confrontation': 9, 'maritime law': 6,

    # Regional Organizations
    'RCEP': 6, 'TPP': 6, 'CPTPP': 6, 'APEC': 6, 'SAARC': 6, 'SCO': 6,

    # Critical Scenarios - Highest Priority
    'doomsday': 10, 'apocalypse': 10, 'existential threat': 10,

    # New Caledonia Specific
    'New Caledonia': 9, 'Nouméa': 7, 'FLNKS': 8, 'Kanak': 8, 'nickel mining': 8,
    'nickel': 6, 'Province Sud': 6, 'Province Nord': 6, 'Province Iles': 6,
    'Customary Senate': 7, 'Louis Mapou': 7, 'independence referendum': 9,
    'French territory': 7,
    
    # Wallis and Futuna Specific
    'Wallis and Futuna': 9, 'Mata-Utu': 7, 'Uvea': 7, 'Sigave': 7, 'Alo': 7,
    'Lavelua': 7, 'French collectivity': 7, 'Territorial Assembly': 7,
    'Gendarmerie': 7, 'traditional kingdoms': 7,
}
