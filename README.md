[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/yourusername/esg_monitor/issues)

# 🌍 ESG Monitor - Multi-Agent ESG Risk Intelligence System

A sophisticated, production-ready multi-agent system for monitoring Environmental, Social, and Governance (ESG) risks across companies and sectors using advanced agents, JSON-RPC communication, and machine learning techniques.

## 📋 Quick Navigation

- [Overview](#overview)
- [Key Features](#key-features)
- [Multi-Agent Architecture](#multi-agent-architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Agent Communication](#agent-communication)
- [Testing & Quality](#testing--quality)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The **ESG Monitor Multi-Agent System** is an intelligent distributed monitoring system that uses autonomous agents to automatically detect, classify, assess, and validate ESG-related risks from diverse data sources. Each agent operates independently with specialized responsibilities while coordinating through JSON-RPC communication to provide real-time monitoring and risk intelligence.

### Key Use Cases
- **Real-time ESG Risk Monitoring**: Track ESG incidents across multiple companies
- **Portfolio Risk Assessment**: Evaluate ESG risk exposure in investment portfolios
- **Regulatory Compliance**: Monitor compliance with SASB and other ESG standards
- **Incident Response**: Automatic detection and validation of ESG-related incidents
- **Stakeholder Reporting**: Generate comprehensive ESG risk reports

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **🤖 Multi-Agent Architecture** | Three specialized agents (Planner, Executor, Validator) working in coordination |
| **🔄 JSON-RPC Communication** | Scalable inter-agent messaging using JSON-RPC 2.0 protocol |
| **📊 Strategic Planning** | Intelligent task decomposition and priority assignment |
| **📡 Multi-source Execution** | Synthetic data generation and multi-source data ingestion |
| **✅ Quality Validation** | Automated quality checks and validation of results |
| **🎯 ESG Scoring** | ML-based incident scoring with feature weighting |
| **📈 Portfolio Risk Analysis** | Aggregate portfolio-wide ESG risk assessment |
| **⚙️ YAML Configuration** | Flexible configuration for all agents and system components |
| **🧪 Comprehensive Testing** | Full test suite for agents, communication, and workflows |
| **📊 Synthetic Data Support** | Built-in generators for incidents, news, and market data |

## 🤖 Multi-Agent Architecture

### Agent Roles

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Coordinator                         │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐ ┌────────────┐ │
│  │  Planner Agent   │  │  Executor Agent  │ │ Validator  │ │
│  │                  │  │                  │ │   Agent    │ │
│  │ • Strategy       │  │ • Data           │ │ • Quality  │ │
│  │ • Decomposition  │  │ • Execution      │ │ • Validation│ │
│  │ • Prioritization │  │ • Collection     │ │ • Reports  │ │
│  └────────┬─────────┘  └────────┬─────────┘ └─────┬──────┘ │
│           │                     │                  │        │
│           └─────────────────────┼──────────────────┘        │
│                     JSON-RPC 2.0                             │
│                                                              │
│  Supporting Components:                                      │
│  • Portfolio Management   • ESG Scoring Model                │
│  • Risk Calculator       • Synthetic Data Generator          │
│  • Configuration Loader  • Logging System                    │
└─────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

**🎯 Planner Agent**
- Creates strategic monitoring plans
- Decomposes tasks into subtasks
- Assigns priorities to monitoring activities
- Defines execution strategy

**⚡ Executor Agent**
- Executes monitoring tasks
- Collects ESG data from multiple sources
- Generates synthetic data for testing
- Performs real-time data collection

**✅ Validator Agent**
- Validates execution results
- Performs quality checks
- Generates recommendations
- Produces validation reports

## 🚀 Quick Start

### Prerequisites
- **Python 3.12.5** or higher
- **pip** package manager
- **Git** for repository access

### Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/esg_monitor.git
cd esg_monitor

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the multi-agent coordinator
python main.py
```

## 📖 Installation

### Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
# Check Python version
python --version

# Verify key packages
python -c "from agents import PlannerAgent, ExecutorAgent, ValidatorAgent; print('✓ All imports successful')"
```

## 💻 Usage

### Running the Multi-Agent System

```bash
# Run the main coordinator
python main.py
```

This will:
1. Initialize all three agents (Planner, Executor, Validator)
2. Load portfolio data (5 dummy companies)
3. Execute a complete monitoring cycle
4. Display results and portfolio risk assessment

### Using Individual Agents Programmatically

```python
from agents import PlannerAgent, ExecutorAgent, ValidatorAgent
from portfolio import DummyPortfolio, RiskCalculator
from models import ESGScoringModel
from utils import get_logger

# Initialize agents
planner = PlannerAgent({"planning_horizon": 30})
executor = ExecutorAgent({"parallel_tasks": 5})
validator = ValidatorAgent({"validation_threshold": 0.8})

# Step 1: Create strategy
plan = planner.plan_monitoring_strategy(
    companies=["TechCorp", "GreenEnergy"],
    esg_dimensions=["E", "S", "G"]
)

# Step 2: Execute tasks
result = executor.execute_task(plan["tasks"][0])

# Step 3: Validate results
validation = validator.validate_result(result)

# Step 4: Score incidents
scorer = ESGScoringModel()
score = scorer.score_incident({
    "severity": 8.0,
    "media_coverage": 4,
    "financial_impact": 50000,
    "regulatory_risk": 7,
    "sentiment": -0.8
})

# Step 5: Calculate portfolio risk
portfolio = DummyPortfolio()
calculator = RiskCalculator(portfolio)
portfolio_risk = calculator.calculate_portfolio_risk()
```

### Generating Synthetic Data

```python
from data import SyntheticDataGenerator

generator = SyntheticDataGenerator(seed=42)

# Generate ESG incidents
incidents = generator.generate_incidents(count=100)

# Generate news articles
news = generator.generate_news_data(count=50)

# Generate market data
market_data = generator.generate_market_data(days=365)
```

## 📁 Project Structure

```
esg_monitor/
├── agents/                      # Multi-agent modules
│   ├── __init__.py
│   ├── planner_agent.py         # Strategic planning agent
│   ├── executor_agent.py        # Execution agent
│   └── validator_agent.py       # Validation agent
│
├── communication/               # JSON-RPC communication layer
│   ├── __init__.py
│   ├── rpc_handler.py           # JSON-RPC server/client
│   └── message_protocol.py      # Message format definitions
│
├── config/                      # Configuration files
│   ├── settings.yml             # Main system configuration
│   └── agent_configs/           # Individual agent configs
│       ├── planner_config.yml
│       ├── executor_config.yml
│       └── validator_config.yml
│
├── data/                        # Data management
│   ├── __init__.py
│   ├── synthetic_generator.py   # Synthetic data generation
│   ├── raw/                     # Raw data storage
│   ├── processed/               # Processed data storage
│   ├── companies.csv            # Company reference data
│   └── sasb_materiality.csv     # SASB standards mapping
│
├── portfolio/                   # Portfolio management
│   ├── __init__.py
│   ├── dummy_portfolio.py       # Synthetic portfolio manager
│   └── risk_calculator.py       # ESG risk calculations
│
├── models/                      # ML/Data models
│   ├── __init__.py
│   └── esg_scoring.py           # ESG incident scoring model
│
├── dashboard/                   # Dashboard application (future)
│   ├── __init__.py
│   └── (agent_dashboard.py)     # Agent status dashboard
│
├── tests/                       # Comprehensive test suite
│   ├── __init__.py
│   ├── test_agents.py           # Agent interaction tests
│   ├── test_communication.py    # RPC communication tests
│   └── test_fintech_workflow.py # Portfolio workflow tests
│
├── utils/                       # Utility functions
│   ├── __init__.py
│   ├── config_loader.py         # YAML configuration loader
│   └── logger.py                # Logging utilities
│
├── logs/                        # Application logs
│   ├── esg_monitor_YYYYMMDD.log # Daily log files
│   └── error.log                # Error log
│
├── main.py                      # Agent coordinator entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── LICENSE                      # MIT License
```

## ⚙️ Configuration

### Main Configuration (config/settings.yml)

```yaml
system:
  name: ESG Monitor
  version: 2.0.0
  log_level: INFO

agents:
  enable_planner: true
  enable_executor: true
  enable_validator: true
  communication_timeout: 30

data:
  synthetic_data_enabled: true
  data_refresh_interval: 3600

portfolio:
  dummy_portfolio_enabled: true
  risk_threshold: 7.0
  materiality_threshold: 6.0

monitoring:
  esg_dimensions:
    - E  # Environmental
    - S  # Social
    - G  # Governance
  alert_threshold: 7.5
  check_interval: 300
```

### Agent Configuration Example

```yaml
# config/agent_configs/planner_config.yml
agent_id: planner_agent
agent_type: strategic

planning:
  strategy_type: hierarchical
  decomposition_depth: 3
  task_prioritization: true

thresholds:
  minimum_companies: 1
  maximum_companies: 100
  confidence_threshold: 0.85
```

### Environment Variables

Create a `.env` file (optional):

```bash
# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/esg_monitor.log

# Portfolio
PORTFOLIO_RISK_THRESHOLD=7.0
MATERIALITY_THRESHOLD=6.0

# System
DEBUG_MODE=False
```

## 🔌 Agent Communication

### JSON-RPC Protocol

Agents communicate using JSON-RPC 2.0 standard:

```python
# Example: Planner sending request to Executor
request = {
    "jsonrpc": "2.0",
    "method": "execute_task",
    "params": {
        "task_id": "TASK_001",
        "company": "TechCorp",
        "dimension": "E"
    },
    "id": "req_12345"
}

# Response
response = {
    "jsonrpc": "2.0",
    "result": {
        "task_id": "TASK_001",
        "status": "completed",
        "data": {...},
        "metrics": {...}
    },
    "id": "req_12345"
}
```

### RPC Handler

```python
from communication import RPCHandler

# Create handler
handler = RPCHandler("executor_agent")

# Register methods
handler.register_method("execute_task", execute_task_function)
handler.register_method("get_status", get_status_function)

# Handle incoming request
response = await handler.handle_request(request)

# Send request to another agent
result = await handler.send_request(
    target_agent="validator_agent",
    method="validate_result",
    params={"result": result_data}
)
```

## 🧪 Testing & Quality

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=communication --cov=portfolio tests/

# Run specific test file
pytest tests/test_agents.py -v

# Run with detailed output
pytest -s tests/test_fintech_workflow.py
```

### Test Coverage

```
tests/
├── test_agents.py              # Agent interaction tests
│   ├── test_planner_creates_strategy
│   ├── test_executor_executes_task
│   └── test_validator_validates_result
│
├── test_communication.py       # RPC communication tests
│   ├── test_create_request
│   ├── test_create_response
│   ├── test_message_validation
│   └── test_serialize_deserialize
│
└── test_fintech_workflow.py   # Portfolio workflow tests
    ├── test_portfolio_creation
    ├── test_calculate_company_risk
    └── test_calculate_portfolio_risk
```

### Code Quality

```bash
# Format code with black
black agents/ communication/ portfolio/ models/ utils/ tests/

# Type checking with mypy
mypy agents/ communication/ portfolio/

# Linting with pylint
pylint agents/ communication/ portfolio/
```

## 🐛 Troubleshooting

### Common Issues

#### Issue: Import errors when running main.py
```bash
# Solution: Ensure all dependencies are installed
pip install -r requirements.txt

# Verify Python path includes project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Issue: Configuration not loading
```bash
# Solution: Check YAML syntax and file paths
python -c "from utils import ConfigLoader; config = ConfigLoader.load_config('config/settings.yml'); print(config)"
```

#### Issue: Agents not responding
```bash
# Solution: Check agent status
python -c "from agents import PlannerAgent; agent = PlannerAgent({}); print(agent.get_status())"
```

#### Issue: Port already in use (for future dashboard)
```bash
# Solution: Change port in config/settings.yml
# Or kill process using the port
lsof -i :8050  # macOS/Linux
netstat -ano | findstr :8050  # Windows
```

### Debug Mode

```python
import logging
from utils import get_logger

# Enable debug logging
logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)

# Now all operations will be logged with debug details
```

### Checking Logs

```bash
# View today's log
tail -f logs/esg_monitor_$(date +%Y%m%d).log

# View errors
tail -f logs/error.log

# Search logs
grep "ERROR" logs/*.log
```

## 🚀 Advanced Usage

### Custom Agent Implementation

```python
from agents import PlannerAgent
from communication import RPCHandler

class CustomAgent(PlannerAgent):
    def __init__(self, config):
        super().__init__(config)
        self.custom_rpc = RPCHandler("custom_agent")
        self.custom_rpc.register_method("custom_method", self.custom_method)
    
    def custom_method(self, param1, param2):
        """Implement custom agent functionality."""
        return {"result": f"Custom processing: {param1}, {param2}"}
```

### Extending the Portfolio

```python
from portfolio import DummyPortfolio

# Add custom companies
portfolio = DummyPortfolio()
portfolio.add_company({
    "company_id": "CUSTOM001",
    "name": "My Company",
    "sector": "Tech",
    "country": "USA",
    "market_cap": 1e9,
    "esg_exposure": {"E": 0.8, "S": 0.7, "G": 0.75}
})
```

### Custom ESG Scoring

```python
from models import ESGScoringModel

scorer = ESGScoringModel()

# Score custom incident
custom_incident = {
    "incident_id": "CUSTOM_001",
    "severity": 7.5,
    "media_coverage": 3,
    "financial_impact": 75000,
    "regulatory_risk": 8,
    "sentiment": -0.6
}

result = scorer.score_incident(custom_incident)
print(f"Risk Level: {result['risk_level']}")
print(f"Recommendations: {result['recommendations']}")
```

## 📊 System Monitoring

### Agent Status Dashboard

```python
from main import AgentCoordinator

coordinator = AgentCoordinator()
status = coordinator.get_portfolio_status()

print(f"Planner Status: {status['agent_status']['planner']}")
print(f"Executor Status: {status['agent_status']['executor']}")
print(f"Validator Status: {status['agent_status']['validator']}")
```

### Performance Metrics

```python
# Get portfolio risk metrics
portfolio_risk = coordinator.risk_calculator.calculate_portfolio_risk()

print(f"Average Risk: {portfolio_risk['average_overall_risk']:.2f}")
print(f"High Risk Companies: {portfolio_risk['companies_at_high_risk']}")
print(f"Risk Range: {portfolio_risk['min_risk']:.2f} - {portfolio_risk['max_risk']:.2f}")
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

```bash
# Fork and clone repository
git clone https://github.com/yourusername/esg_monitor.git
cd esg_monitor

# Create feature branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r requirements.txt
pip install black pylint pytest pytest-cov mypy
```

### Making Changes

1. **Follow Code Style**
   ```bash
   black agents/ communication/ portfolio/
   ```

2. **Add Type Hints**
   ```python
   def process_data(self, data: Dict[str, Any]) -> Dict[str, float]:
       """Process ESG data and return scores."""
       pass
   ```

3. **Write Tests**
   ```bash
   pytest tests/ -v --cov
   ```

4. **Update Documentation**
   - Update README.md if structure changes
   - Document new agent methods
   - Add docstrings to functions

### Commit Guidelines

```bash
# Commit with descriptive messages
git commit -m "feat(agents): add new monitoring capability"
git commit -m "fix(communication): resolve RPC timeout issue"
git commit -m "docs(readme): update installation instructions"

# Format: <type>(<scope>): <subject>
# Types: feat, fix, docs, style, refactor, test, chore
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/esg_monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/esg_monitor/discussions)
- **Email**: contact@example.com

## 🙏 Acknowledgments

- JSON-RPC 2.0 specification
- SASB (Sustainability Accounting Standards Board) standards
- Open source community contributions
- Python ecosystem for excellent tools and libraries

---

**Last Updated**: January 6, 2026
**Version**: 2.0.0 (Multi-Agent System)
**Maintainer**: ESG Monitor Team

> **Note**: This README is regularly updated to reflect the current system architecture. Changes to the folder structure or major features will automatically trigger README updates.
