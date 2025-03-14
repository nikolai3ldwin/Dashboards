# Indo-Pacific Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red.svg)](https://streamlit.io/)

A comprehensive real-time dashboard for monitoring and analyzing current events in the Indo-Pacific region. This tool uses RSS feeds from reputable sources to present categorized, filtered, and prioritized news with importance ratings and sentiment analysis.

![Dashboard Screenshot](docs/images/dashboard_screenshot.png)

## Features

- **Multi-source News Aggregation**: Collects and consolidates news from multiple RSS feeds.
- **Advanced Filtering**: Filter by country, topic, importance, and sentiment.
- **Importance Rating**: Automatically rates article importance using keyword-based weighting.
- **Sentiment Analysis**: Analyzes sentiment toward key regional actors.
- **Categorical Analysis**: Classifies content into key regional topics:
  - Political & Diplomatic
  - Military & Defense
  - Civil Affairs
  - Drug Proliferation
  - CWMD (Counter Weapons of Mass Destruction)
  - Business & Economic
  - Regional Specific (New Caledonia, Wallis and Futuna, etc.)
- **Search Functionality**: Find specific events and topics across all sources.
- **Visual Presentation**: Clean, responsive interface with images and importance indicators.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/indo-pacific-dashboard.git
   cd indo-pacific-dashboard
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

3. Use the sidebar filters to customize your view:
   - Select news sources
   - Filter by country or region
   - Choose topic categories
   - Set minimum importance level
   - Filter by sentiment
   - Sort by date, importance, or relevance
   - Search for specific keywords

## Customization

### Adding New RSS Sources

Edit `data/rss_sources.py` to add new RSS feeds:

```python
RSS_FEEDS = [
    ("https://www.example.com/feed", "Source Name"),
    # Add more feeds here
]
```

### Modifying Keywords

The keyword dictionaries in `data/keywords.py` can be modified to adjust importance ratings or add new terms relevant to your specific monitoring needs.

## Project Structure

```
indo-pacific-dashboard/
├── dashboard/               # Main application directory
│   ├── app.py               # Main Streamlit application
│   ├── utils/               # Utility functions
│   ├── data/                # Data resources and keywords
│   └── components/          # UI components
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── requirements.txt         # Project dependencies
├── LICENSE                  # MIT license
└── README.md                # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the fantastic web application framework
- All the news sources that provide RSS feeds for their content
- [NLTK](https://www.nltk.org/) and [TextBlob](https://textblob.readthedocs.io/) for text processing
