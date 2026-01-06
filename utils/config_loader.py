"""Configuration loader for YAML files."""

import yaml
from pathlib import Path
from typing import Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """Load and manage YAML configuration files."""

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            Configuration dictionary
        """
        path = Path(config_path)
        
        if not path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            return {}
        
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config or {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return {}

    @staticmethod
    def load_all_agent_configs(agent_configs_dir: str) -> Dict[str, Dict[str, Any]]:
        """
        Load all agent configuration files.
        
        Args:
            agent_configs_dir: Directory containing agent config files
            
        Returns:
            Dictionary of agent configurations
        """
        agent_configs = {}
        configs_path = Path(agent_configs_dir)
        
        if not configs_path.exists():
            logger.warning(f"Agent configs directory not found: {agent_configs_dir}")
            return agent_configs
        
        for config_file in configs_path.glob("*_config.yml"):
            agent_name = config_file.stem.replace("_config", "")
            try:
                config = ConfigLoader.load_config(str(config_file))
                agent_configs[agent_name] = config
                logger.info(f"Loaded config for {agent_name}")
            except Exception as e:
                logger.error(f"Error loading {config_file}: {e}")
        
        return agent_configs

    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str) -> bool:
        """
        Save configuration to YAML file.
        
        Args:
            config: Configuration dictionary
            config_path: Path to save configuration
            
        Returns:
            True if successful, False otherwise
        """
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, 'w') as f:
                yaml.safe_dump(config, f, default_flow_style=False)
            logger.info(f"Saved configuration to {config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

    @staticmethod
    def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configuration dictionaries.
        
        Args:
            base_config: Base configuration
            override_config: Override configuration
            
        Returns:
            Merged configuration
        """
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = ConfigLoader.merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged

    @staticmethod
    def get_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
        """
        Get value from config using dot notation.
        
        Args:
            config: Configuration dictionary
            key_path: Dot-separated key path (e.g., "agents.planner.enabled")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
