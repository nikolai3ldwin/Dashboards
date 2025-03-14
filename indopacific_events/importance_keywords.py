# keywords.py
"""
Enhanced keyword dictionaries for the Indo-Pacific Dashboard.
Keywords are organized by category and include importance weights (1-10).
"""

# Political and Diplomatic Keywords
POLITICAL_KEYWORDS = {
    'crisis': 8, 'conflict': 8, 'treaty': 6, 'agreement': 6, 'election': 6, 'coup': 10,
    'diplomacy': 6, 'sanctions': 8, 'trade war': 8, 'summit': 6, 'negotiation': 6,
    'alliance': 7, 'territorial dispute': 9, 'sovereignty': 7, 'peacekeeping': 6,
    'political reform': 6, 'government collapse': 10, 'referendum': 7, 'secession': 8,
    'political instability': 8, 'constitutional crisis': 8, 'state visit': 5,
    'diplomatic relations': 7, 'diplomatic incident': 8, 'foreign policy': 6,
    'bilateral talks': 6, 'multilateral negotiations': 6, 'joint statement': 5,
    'political opposition': 6, 'power transition': 7, 'regime change': 9
}

# Major Powers and Regional Actors
REGIONAL_ACTORS_KEYWORDS = {
    'US': 7, 'United States': 7, 'China': 7, 'Russia': 7, 'Japan': 6, 'India': 6, 'Australia': 6,
    'South Korea': 6, 'North Korea': 8, 'ASEAN': 6, 'EU': 6, 'UN': 6,
    'Taiwan': 8, 'Hong Kong': 7, 'Tibet': 7, 'Xinjiang': 7,
    'Indonesia': 6, 'Vietnam': 6, 'Philippines': 6, 'Malaysia': 6, 'Singapore': 6,
    'Pacific Islands': 7, 'Pacific Island Countries': 7, 'Fiji': 6, 'Papua New Guinea': 6,
    'Cambodia': 6, 'Laos': 6, 'Myanmar': 7, 'Thailand': 6, 'Brunei': 6,
    'Mongolia': 6, 'Pakistan': 7, 'Bangladesh': 6, 'Sri Lanka': 6, 'Nepal': 6,
    'Timor-Leste': 6, 'Bhutan': 6, 'Maldives': 6, 'Palau': 6, 'Marshall Islands': 6,
    'Micronesia': 6, 'Solomon Islands': 7, 'Vanuatu': 6, 'Samoa': 6, 'Tonga': 6,
    'New Zealand': 6, 'Kiribati': 6, 'Tuvalu': 6, 'Nauru': 6
}

# Military and Defense Keywords - Expanded
MILITARY_KEYWORDS = {
    'military': 7, 'defense': 7, 'war': 10, 'terrorism': 9, 'insurgency': 9,
    'nuclear': 10, 'missile': 8, 'cyber attack': 9, 'intelligence': 7,
    'arms race': 8, 'naval exercise': 7, 'joint military exercise': 7,
    'troop deployment': 8, 'military base': 7, 'defense pact': 7, 'arms deal': 7,
    'military modernization': 7, 'defense budget': 6, 'force posture': 7,
    'combat readiness': 8, 'air defense': 7, 'maritime security': 7,
    'joint task force': 7, 'special forces': 7, 'counter-terrorism': 8,
    'military alliance': 7, 'armaments': 7, 'defense industry': 6,
    'defense technology': 7, 'military strategy': 7, 'asymmetric warfare': 8,
    'hybrid warfare': 8, 'conventional forces': 6, 'combined operations': 7,
    'precision strike': 7, 'force projection': 7, 'forward presence': 7,
    'deterrence': 8, 'theater security': 7, 'military doctrine': 6,
    'security cooperation': 7, 'defense cooperation': 7, 'defense ecosystem': 6,
    'military logistics': 6, 'defense acquisition': 6, 'defense exports': 6,
    'gray zone operations': 8, 'amphibious capability': 7, 'power projection': 7
}

# Civil Affairs Keywords - Comprehensive
CIVIL_AFFAIRS_KEYWORDS = {
    'civil affairs': 8, 'civil-military operations': 7, 'humanitarian assistance': 8, 
    'disaster relief': 8, 'civilian casualties': 9, 'displaced persons': 8, 
    'civilian infrastructure': 7, 'reconstruction': 7, 'stabilization': 8, 
    'community engagement': 6, 'civil society': 6, 'local governance': 7, 
    'tribal leaders': 7, 'chiefs': 7, 'community resilience': 6, 
    'cultural heritage': 6, 'indigenous rights': 7, 'traditional practices': 6, 
    'gender equality': 6, 'women empowerment': 6, 'education access': 7, 
    'civic education': 6, 'public services': 7, 'community development': 6,
    'healthcare access': 7, 'vulnerable populations': 7, 'child protection': 7,
    'essential services': 7, 'food security': 8, 'water security': 8,
    'sanitation': 7, 'shelter': 7, 'civil institutions': 6, 'rule of law': 7,
    'judicial system': 6, 'police reform': 7, 'customs support': 6,
    'border management': 7, 'election support': 7, 'governance capacity': 7,
    'public safety': 7, 'non-governmental organizations': 6, 'civil defense': 7,
    'civil protection': 7, 'community policing': 6, 'local leadership': 6,
    'village council': 6, 'institutional capacity': 6, 'informal governance': 6,
    'traditional authority': 6, 'national unity': 7, 'social cohesion': 7,
    'conflict resolution': 7, 'peace building': 8, 'reconciliation': 7,
    'trauma healing': 6, 'psychological support': 6, 'livelihoods': 6,
    'vocational training': 5, 'youth programs': 6, 'community infrastructure': 6
}

# Drug Proliferation Keywords
DRUG_PROLIFERATION_KEYWORDS = {
    'drug trafficking': 9, 'narcotics': 8, 'methamphetamine': 8, 'opioids': 8,
    'fentanyl': 9, 'heroin': 8, 'cocaine': 8, 'drug precursors': 7,
    'synthetic drugs': 8, 'golden triangle': 8, 'drug seizure': 7, 
    'drug smuggling': 8, 'narcotic production': 8, 'drug cartel': 8,
    'drug syndicate': 8, 'drug laboratory': 7, 'illicit substances': 7,
    'drug enforcement': 7, 'counter-narcotics': 7, 'maritime interdiction': 7,
    'border control': 7, 'customs seizure': 7, 'supply chain disruption': 7,
    'money laundering': 8, 'drug proceeds': 7, 'pharmaceutical diversion': 7,
    'darknet markets': 7, 'chemical precursors': 7, 'synthetic opioids': 8,
    'transnational crime': 8, 'cross-border trafficking': 8, 'drug rehabilitation': 6,
    'addiction crisis': 7, 'drug cultivation': 7, 'poppy fields': 7,
    'drug transit route': 7, 'port security': 7, 'maritime trafficking': 7,
    'drug control policy': 6, 'alternative development': 6, 'drug diplomacy': 6,
    'pharmaceutical security': 6, 'pharmaceutical crime': 7, 'drug market': 6
}

# Counter Weapons of Mass Destruction (CWMD) Proliferation Keywords
CWMD_KEYWORDS = {
    'WMD': 10, 'nuclear weapon': 10, 'chemical weapon': 10, 'biological weapon': 10,
    'proliferation': 9, 'nuclear material': 9, 'radioactive material': 9,
    'radiological threat': 9, 'uranium enrichment': 9, 'plutonium': 9,
    'centrifuge': 8, 'missile technology': 8, 'nonproliferation': 8,
    'nuclear test': 10, 'nuclear facility': 9, 'nuclear program': 9,
    'nuclear export control': 8, 'dual-use technology': 8, 'IAEA': 8,
    'nuclear inspection': 8, 'nuclear safeguards': 8, 'nuclear agreement': 8,
    'nuclear deal': 8, 'nuclear treaty': 8, 'nuclear disarmament': 8,
    'tactical nuclear': 9, 'nuclear submarine': 8, 'nuclear delivery system': 8,
    'chemical precursors': 8, 'nerve agent': 9, 'chemical attack': 10,
    'chemical facility': 8, 'biological agent': 9, 'pathogen': 9,
    'bioterrorism': 10, 'biosecurity': 8, 'biosafety': 8, 'biodefense': 8,
    'OPCW': 8, 'Chemical Weapons Convention': 8, 'Biological Weapons Convention': 8,
    'nuclear smuggling': 9, 'illicit transfer': 8, 'WMD intelligence': 8,
    'nuclear security': 8, 'missile defense': 8, 'nuclear command': 8,
    'nuclear export': 8, 'nuclear trade': 8, 'nuclear sharing': 8
}

# Business and Economic Keywords - Expanded
BUSINESS_KEYWORDS = {
    'trade': 6, 'investment': 6, 'economic crisis': 9, 'recession': 8,
    'currency': 6, 'stock market': 6, 'supply chain': 7, 'belt and road': 7,
    'free trade agreement': 6, 'tariff': 6, 'economic cooperation': 6,
    'financial crisis': 9, 'market crash': 9, 'economic sanctions': 8,
    'foreign direct investment': 7, 'joint venture': 6, 'business partnership': 6,
    'market access': 7, 'trade barrier': 7, 'trade policy': 6, 'export control': 7,
    'economic zone': 6, 'special economic zone': 7, 'industrial policy': 6,
    'digital economy': 7, 'e-commerce': 6, 'technology transfer': 7,
    'intellectual property': 7, 'patent dispute': 7, 'corporate takeover': 7,
    'market manipulation': 8, 'business regulation': 6, 'anti-monopoly': 7,
    'business disruption': 7, 'supply chain resilience': 7, 'resource security': 7,
    'economic strategy': 6, 'central bank': 7, 'monetary policy': 7,
    'inflation': 7, 'deflation': 7, 'national debt': 7, 'sovereign debt': 7,
    'credit rating': 6, 'financial stability': 7, 'banking system': 7,
    'investor confidence': 6, 'capital flight': 8, 'economic reform': 7,
    'privatization': 6, 'state-owned enterprise': 6, 'market liberalization': 6,
    'trade deficit': 6, 'trade surplus': 6, 'economic diplomacy': 6,
    'economic statecraft': 7, 'commercial diplomacy': 6, 'business delegation': 5,
    'sovereign wealth fund': 7, 'economic development': 6, 'economic diversification': 6
}

# Economic and Resources Categories - Expanded
ECONOMIC_RESOURCES_KEYWORDS = {
    'oil': 7, 'gas': 7, 'renewable energy': 6, 'nuclear power': 8,
    'rare earth minerals': 8, 'energy security': 8, 'resource conflict': 9,
    'energy crisis': 9, 'power shortage': 7, 'critical minerals': 7,
    'strategic resources': 8, 'energy infrastructure': 7, 'energy cooperation': 6,
    'resource nationalism': 7, 'resource extraction': 6, 'mining rights': 7,
    'land grab': 7, 'water rights': 7, 'fishing rights': 7, 'agricultural land': 6,
    'food security': 8, 'commodity prices': 6, 'resource dependency': 7,
    'energy transition': 6, 'carbon market': 6, 'carbon pricing': 6,
    'sustainability': 6, 'green economy': 6, 'circular economy': 6
}

# Regional-Specific Keywords
NEW_CALEDONIA_KEYWORDS = {
    'New Caledonia': 9, 'Nouméa': 7, 'FLNKS': 8, 'Kanak': 8, 'nickel mining': 8,
    'nickel': 6, 'Province Sud': 6, 'Province Nord': 6, 'Province Iles': 6,
    'Customary Senate': 7, 'Louis Mapou': 7, 'independence referendum': 9,
    'French territory': 7, 'indigenous rights': 7, 'Caldoche': 7,
    'Loyalty Islands': 6, 'Grand Terre': 6, 'Pacific decolonization': 8
}

WALLIS_FUTUNA_KEYWORDS = {
    'Wallis and Futuna': 9, 'Mata-Utu': 7, 'Uvea': 7, 'Sigave': 7, 'Alo': 7,
    'Lavelua': 7, 'French collectivity': 7, 'Territorial Assembly': 7,
    'Gendarmerie': 7, 'traditional kingdoms': 7, 'royal chiefdoms': 7,
    'Catholic Church': 6, 'French administration': 7, 'customary authority': 7
}

# Technology and Innovation Keywords - Expanded
TECHNOLOGY_KEYWORDS = {
    'AI': 7, 'artificial intelligence': 7, '5G': 7, 'quantum computing': 7,
    'space program': 7, 'satellite': 6, 'tech war': 8, 'innovation': 6,
    'cybersecurity': 8, 'data privacy': 7, 'digital economy': 6, 
    'blockchain': 6, 'cryptocurrency': 6, 'digital infrastructure': 7,
    'tech sovereignty': 8, 'semiconductor': 8, 'chip manufacturing': 8,
    'tech sanctions': 8, 'digital divide': 6, 'internet access': 6,
    'tech regulation': 7, 'data localization': 7, 'cloud computing': 6,
    'big tech': 6, 'digital platform': 6, 'e-government': 6,
    'digital surveillance': 8, 'facial recognition': 7, 'digital ID': 7
}

# Critical Scenarios - Highest Priority
CRITICAL_SCENARIOS_KEYWORDS = {
    'doomsday': 10, 'apocalypse': 10, 'existential threat': 10,
    'catastrophic': 10, 'mass casualty': 10, 'imminent threat': 10
}

# Combined master dictionary for use in the app
IMPORTANT_KEYWORDS = {
    **POLITICAL_KEYWORDS, 
    **REGIONAL_ACTORS_KEYWORDS,
    **MILITARY_KEYWORDS,
    **CIVIL_AFFAIRS_KEYWORDS,
    **DRUG_PROLIFERATION_KEYWORDS,
    **CWMD_KEYWORDS,
    **BUSINESS_KEYWORDS,
    **ECONOMIC_RESOURCES_KEYWORDS,
    **NEW_CALEDONIA_KEYWORDS,
    **WALLIS_FUTUNA_KEYWORDS,
    **TECHNOLOGY_KEYWORDS,
    **CRITICAL_SCENARIOS_KEYWORDS
}

# Optional category weights for advanced scoring
CATEGORY_WEIGHTS = {
    'political': 1.0,
    'regional_actors': 1.0,
    'military': 1.2,  # Slightly higher priority
    'civil_affairs': 1.0,
    'drug_proliferation': 1.1,
    'cwmd': 1.3,  # Higher priority due to severity
    'business': 0.9,
    'economic_resources': 1.0,
    'regional_specific': 1.1,
    'technology': 1.0,
    'critical_scenarios': 1.5  # Highest priority
}
