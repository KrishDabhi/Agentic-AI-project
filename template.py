import os

def create_directory(path):
    """Create a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def create_file(path, content=""):
    """Create a file with optional content."""
    with open(path, 'w') as f:
        f.write(content)

def main():
    # Create directories
    directories = [
        'app',
        'app/core',
        'app/models',
        'app/utils',
        'data',
        'data/raw',
        'data/processed',
        'logs',
        'tests',
        'dashboard',
        'config'
    ]
    
    for directory in directories:
        create_directory(directory)
    
    # Create __init__.py files
    init_files = [
        'app/__init__.py',
        'app/core/__init__.py',
        'app/models/__init__.py',
        'app/utils/__init__.py',
        'tests/__init__.py',
        'dashboard/__init__.py',
        'config/__init__.py'
    ]
    
    for file_path in init_files:
        create_file(file_path)
    
    # Create core module files
    core_files = [
        'app/core/data_ingestion.py',
        'app/core/ner_processor.py',
        'app/core/esg_classifier.py',
        'app/core/materiality_checker.py',
        'app/core/risk_scorer.py',
        'app/core/database_manager.py'
    ]
    
    for file_path in core_files:
        create_file(file_path)
    
    # Create model files
    model_files = [
        'app/models/company.py',
        'app/models/esg_incident.py',
        'app/models/risk_alert.py'
    ]
    
    for file_path in model_files:
        create_file(file_path)
    
    # Create utility files
    util_files = [
        'app/utils/config.py',
        'app/utils/logger.py',
        'app/utils/helpers.py'
    ]
    
    for file_path in util_files:
        create_file(file_path)
    
    # Create test files
    test_files = [
        'tests/test_ner.py',
        'tests/test_materiality.py',
        'tests/test_risk_scorer.py'
    ]
    
    for file_path in test_files:
        create_file(file_path)
    
    # Create other files
    other_files = [
        'app/main.py',
        'dashboard/esg_dashboard.py',
        'config/settings.py',
        'requirements.txt',
        'setup.sh',
        'run.py',
        'README.md',
        'data/sasb_materiality.csv',
        'data/companies.csv',
        'logs/esg_monitor.log',
        'logs/error.log'
    ]
    
    for file_path in other_files:
        create_file(file_path)

if __name__ == "__main__":
    main()
    print("ESG Monitor Project structure created successfully!")