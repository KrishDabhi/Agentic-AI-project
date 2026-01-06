# 🌍 ESG Monitor - Environmental, Social & Governance Risk Intelligence

A comprehensive, production-ready system for monitoring Environmental, Social, and Governance (ESG) risks across companies and sectors using advanced natural language processing and machine learning techniques.

## 📋 Quick Navigation

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Integration](#api-integration)
- [Dashboard](#dashboard)
- [Testing & Quality](#testing--quality)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The **ESG Monitor Project** is an intelligent monitoring system designed to automatically detect, classify, and assess ESG-related risks from diverse data sources including news articles, social media, and company reports. It provides organizations with real-time monitoring capabilities to identify potential ESG issues before they become material risks.

### Why ESG Monitoring?
- **Regulatory Compliance**: Stay ahead of evolving ESG disclosure requirements
- **Risk Mitigation**: Identify emerging risks early before they impact your organization
- **Stakeholder Trust**: Demonstrate commitment to ESG principles and transparency
- **Competitive Advantage**: Make data-driven decisions on sustainability initiatives

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **📡 Multi-source Data Ingestion** | Collects data from news APIs, social media platforms, and company reports in real-time |
| **🔍 Named Entity Recognition** | Intelligently identifies companies, people, locations, and organizations in unstructured text |
| **🏷️ ESG Classification** | Automatically categorizes incidents into Environmental, Social, and Governance dimensions |
| **✅ Materiality Assessment** | Cross-references incidents against SASB (Sustainability Accounting Standards Board) standards |
| **📊 Risk Scoring** | Calculates comprehensive risk scores based on severity, likelihood, and materiality |
| **📈 Real-time Dashboard** | Interactive Dash/Plotly dashboard with live ESG risk metrics and trends |
| **⚠️ Alert System** | Generates intelligent alerts for high-risk incidents with configurable thresholds |
| **💾 Database Management** | Persistent storage of ESG incidents and risk assessments using SQLAlchemy |
| **🧪 Comprehensive Testing** | Unit tests and integration tests with pytest framework |

## 🚀 Quick Start

### Prerequisites
- **Python 3.12.5** or higher
- **pip** or **conda** package manager
- **Git** for cloning the repository

### Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/esg_monitor_project.git
cd esg_monitor_project

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python run.py
```

The dashboard will be available at `http://localhost:8050`

## 📖 Installation

### Detailed Setup Instructions

#### Option 1: Virtual Environment Setup (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install --upgrade pip
pip install -r requirements.txt
```

#### Option 2: Conda Environment Setup

```bash
# Create conda environment
conda create -n esg_monitor python=3.12

# Activate environment
conda activate esg_monitor

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test Python version
python --version

# Test key imports
python -c "import dash, pandas, spacy; print('All dependencies installed successfully!')"
```

## 💻 Usage

### Starting the Dashboard

```bash
# Development mode (with debug/hot reload)
python run.py

# Or directly run the dashboard
python -m dashboard.esg_dashboard
```

Visit `http://localhost:8050` in your browser to view the ESG Monitor Dashboard.

### Using Core Modules

#### Data Ingestion
```python
from app.core.data_ingestion import DataIngestion

ingester = DataIngestion()
raw_data = ingester.fetch_from_news_api()
```

#### NER Processing
```python
from app.core.ner_processor import NERProcessor

ner = NERProcessor()
entities = ner.extract_entities(text="Apple Inc. faces environmental concerns in California...")
```

#### ESG Classification
```python
from app.core.esg_classifier import ESGClassifier

classifier = ESGClassifier()
classification = classifier.classify(text)
# Returns: {'environmental': 0.85, 'social': 0.45, 'governance': 0.62}
```

#### Risk Scoring
```python
from app.core.risk_scorer import RiskScorer

scorer = RiskScorer()
risk_score = scorer.calculate_risk(incident_data)
# Returns: {'overall_score': 7.8, 'severity': 8, 'likelihood': 7, 'materiality': 9}
```

## 📁 Project Structure

```
esg_monitor_project/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                  # Application entry point
│   ├── core/                    # Core processing modules
│   │   ├── data_ingestion.py    # Multi-source data collection
│   │   ├── ner_processor.py     # Named Entity Recognition
│   │   ├── esg_classifier.py    # ESG classification logic
│   │   ├── materiality_checker.py  # SASB materiality mapping
│   │   ├── risk_scorer.py       # Risk calculation engine
│   │   └── database_manager.py  # Database operations
│   ├── models/                  # Data models
│   │   ├── company.py           # Company data model
│   │   ├── esg_incident.py      # ESG incident model
│   │   └── risk_alert.py        # Risk alert model
│   └── utils/                   # Utility functions
│       ├── config.py            # Configuration management
│       ├── helpers.py           # Helper functions
│       └── logger.py            # Logging setup
├── dashboard/                   # Dashboard application
│   ├── esg_dashboard.py         # Main dashboard component
├── config/                      # Configuration files
│   └── settings.py              # Global settings
├── data/                        # Data directory
│   ├── raw/                     # Raw data files
│   ├── processed/               # Processed data files
│   ├── companies.csv            # Company reference data
│   └── sasb_materiality.csv     # SASB standards mapping
├── logs/                        # Application logs
├── tests/                       # Test suite
│   ├── test_ner.py
│   ├── test_materiality.py
│   └── test_risk_scorer.py
├── requirements.txt             # Python dependencies
├── setup.sh                     # Setup script
└── README.md                    # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys
NEWS_API_KEY=your_news_api_key_here
TWITTER_API_KEY=your_twitter_key
TWITTER_API_SECRET=your_twitter_secret

# Database
DATABASE_URL=sqlite:///esg_monitor.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/esg_monitor.log

# Dashboard
DASH_PORT=8050
DASH_DEBUG=True
```

### Configuration File

Edit `config/settings.py` to customize:

```python
# Data collection frequency (in hours)
DATA_COLLECTION_INTERVAL = 24

# Risk threshold for alerts
RISK_ALERT_THRESHOLD = 7.0

# NER Model
NER_MODEL = "en_core_web_sm"

# Database path
DATABASE_PATH = "esg_monitor.db"
```

## 🔌 API Integration

### Supported Data Sources

1. **News APIs**
   - NewsAPI.org integration for global news monitoring
   - Configuration in `app/core/data_ingestion.py`

2. **Social Media**
   - Twitter/X API for sentiment analysis
   - LinkedIn integration for company mentions

3. **Company Reports**
   - Direct CSV/PDF ingestion
   - Web scraping capabilities

### Adding New Data Sources

```python
# In app/core/data_ingestion.py
def add_custom_source(self, source_config):
    """Add a custom data source"""
    self.sources.append(source_config)
```

## 📊 Dashboard

The interactive dashboard provides:

### Visualizations
- **ESG Scores Overview**: Bar chart of company ESG scores
- **Trend Analysis**: Time-series visualization of risk evolution
- **Risk Distribution**: Pie charts showing ESG dimension breakdown
- **Top Risks**: Table of high-priority incidents
- **Materiality Matrix**: 2D visualization of risk vs. materiality

### Features
- Real-time data updates
- Customizable filters by company, date range, and risk level
- Export functionality (CSV, PDF)
- Interactive drill-down capabilities

Access the dashboard at: `http://localhost:8050`

## 🧪 Testing & Quality

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_risk_scorer.py -v

# Run with output capture
pytest -s tests/
```

### Test Files

```
tests/
├── test_ner.py              # NER processor tests
├── test_materiality.py      # Materiality checker tests
└── test_risk_scorer.py      # Risk scoring algorithm tests
```

### Code Quality

```bash
# Format code with black
black app/ tests/

# Run linting
pylint app/

# Type checking
mypy app/
```

## 🐛 Troubleshooting

### Common Issues

#### Issue: ModuleNotFoundError for dash/plotly
```bash
# Solution: Reinstall dashboard dependencies
pip install --upgrade dash plotly
```

#### Issue: Database connection error
```bash
# Solution: Check DATABASE_URL in .env
# Reset database:
rm esg_monitor.db
python app/core/database_manager.py --init
```

#### Issue: spaCy model not found
```bash
# Solution: Download required spaCy model
python -m spacy download en_core_web_sm
```

#### Issue: API rate limits
```python
# Solution: Implement rate limiting in config/settings.py
API_RATE_LIMIT = 100  # requests per hour
API_RETRY_ATTEMPTS = 3
```

### Getting Help

- Check logs: `tail -f logs/esg_monitor.log`
- Review [GitHub Issues](https://github.com/yourusername/esg_monitor/issues)
- Create a new issue with detailed error messages and reproduction steps

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

```bash
# Fork the repository
git clone https://github.com/yourusername/esg_monitor.git
cd esg_monitor

# Create feature branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r requirements.txt
pip install black pylint pytest pytest-cov
```

### Making Changes

1. **Code Style**: Follow PEP 8 using `black`
   ```bash
   black app/ tests/
   ```

2. **Type Hints**: Add type annotations to functions
   ```python
   def calculate_risk(incident_data: dict) -> float:
       """Calculate risk score from incident data."""
       pass
   ```

3. **Testing**: Add tests for new features
   ```bash
   pytest tests/ -v --cov
   ```

4. **Documentation**: Update docstrings and README

### Submitting Changes

```bash
# Commit changes
git add .
git commit -m "feat: add new ESG classification feature"

# Push to fork
git push origin feature/your-feature-name

# Create Pull Request
# - Provide clear description
# - Link related issues
# - Include test results
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/esg_monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/esg_monitor/discussions)
- **Email**: contact@example.com

## 🙏 Acknowledgments

- SASB (Sustainability Accounting Standards Board) for materiality standards
- spaCy team for excellent NLP tools
- Plotly/Dash for interactive visualization framework
- Open source community contributions

---

**Last Updated**: January 2026
**Version**: 1.0.0
**Maintainer**: Your Organization Name