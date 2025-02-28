# Investigative Profile Builder

A Streamlit application for extracting, organizing, and analyzing information for investigative profiles.

## Features

- **Document Processing**: Extract data from PDF, DOCX, and TXT files
- **Entity Recognition**: Identify people, organizations, locations, dates, and financial information
- **Pattern Matching**: Find emails, phone numbers, addresses, social media handles, and more
- **Profile Building**: Organize extracted information into structured profiles
- **API Connections**: Connect to external data sources (LinkedIn, public records, social media)
- **Document Repository**: Manage and organize source documents

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/investigative-profile-tool.git
cd investigative-profile-tool
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the spaCy model:
```bash
python -m spacy download en_core_web_lg
```

## Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at http://localhost:8501.

## Pages

1. **Data Extraction**: Upload and process documents to extract information
2. **Profile Builder**: Organize extracted data into structured profiles
3. **API Connections**: Connect to external data sources
4. **Document Repository**: Manage source documents

## Developing & Extending

### Adding New Extraction Patterns

Add new regex patterns in `utils/data_extraction.py`:

```python
PATTERNS = {
    # Existing patterns...
    'your_new_pattern': r'your_regex_pattern_here',
}
```

### Implementing Actual API Connections

Replace the mock implementations in `utils/api_connectors.py` with actual API clients.

### Adding Visualization Features

Create custom visualizations in `utils/visualizations.py` and integrate them into the profile pages.

## Ethical Usage

This tool is designed for legitimate investigative purposes only. Always:

- Respect privacy and data protection laws
- Use only publicly available information or information obtained through legal means
- Follow journalistic ethics and standards
- Verify information from multiple sources
- Be transparent about your methods

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web application framework
- [spaCy](https://spacy.io/) for natural language processing
- [NLTK](https://www.nltk.org/) for text processing
- [PyPDF2](https://pypi.org/project/PyPDF2/) and [python-docx](https://python-docx.readthedocs.io/) for document processing
