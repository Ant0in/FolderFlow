

from src.core.assertion_helper import AssertionHelper
import yaml


class YAMLSafeHelper:
    
    @staticmethod
    def safe_load(yaml_filepath: str) -> dict:

        AssertionHelper.verify_file_extension(yaml_filepath, '.yaml')
        
        try:
            with open(yaml_filepath, 'r') as f:
                return yaml.safe_load(f)
        except Exception as yaml_exception:
            raise yaml_exception(f'[E] Unknown error occurred while loading YAML file data @ {yaml_filepath}.')
        
    @staticmethod
    def safe_dump(yaml_filepath: str, data: dict) -> None:

        AssertionHelper.verify_file_extension(yaml_filepath, '.yaml')
        
        try:
            with open(yaml_filepath, 'w') as f:
                yaml.safe_dump(data, f)
        except Exception as yaml_exception:
            raise yaml_exception(f'[E] Unknown error occurred while dumping data in YAML file @ {yaml_filepath}.')