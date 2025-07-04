#!/usr/bin/env python3
"""
Environment Validation Script

This script validates that all required environment variables and dependencies
are properly configured before deployment.
"""

import os
import sys
import subprocess
import psycopg2
import redis
import requests
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    """Result of an environment validation check."""
    check_name: str
    passed: bool
    message: str
    details: str = ""


class EnvironmentValidator:
    """Validates environment configuration for web applications."""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.results: List[ValidationResult] = []
        self.load_environment()
    
    def load_environment(self):
        """Load environment variables from .env file."""
        if Path(self.env_file).exists():
            from dotenv import load_dotenv
            load_dotenv(self.env_file)
            print(f"✓ Loaded environment from {self.env_file}")
        else:
            print(f"⚠ No {self.env_file} file found, using system environment")
    
    def validate_required_vars(self, required_vars: List[str]) -> ValidationResult:
        """Validate that required environment variables are set."""
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            return ValidationResult(
                "Required Environment Variables",
                False,
                f"Missing required environment variables: {', '.join(missing_vars)}",
                f"Add these variables to your {self.env_file} file"
            )
        
        return ValidationResult(
            "Required Environment Variables",
            True,
            f"All {len(required_vars)} required environment variables are set"
        )
    
    def validate_database_connection(self) -> ValidationResult:
        """Validate database connection."""
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            return ValidationResult(
                "Database Connection",
                False,
                "DATABASE_URL not configured"
            )
        
        try:
            conn = psycopg2.connect(database_url)
            conn.close()
            return ValidationResult(
                "Database Connection",
                True,
                "Database connection successful"
            )
        except Exception as e:
            return ValidationResult(
                "Database Connection",
                False,
                f"Database connection failed: {str(e)}"
            )
    
    def validate_redis_connection(self) -> ValidationResult:
        """Validate Redis connection."""
        redis_url = os.getenv('REDIS_URL')
        if not redis_url:
            return ValidationResult(
                "Redis Connection",
                False,
                "REDIS_URL not configured"
            )
        
        try:
            r = redis.from_url(redis_url)
            r.ping()
            return ValidationResult(
                "Redis Connection",
                True,
                "Redis connection successful"
            )
        except Exception as e:
            return ValidationResult(
                "Redis Connection",
                False,
                f"Redis connection failed: {str(e)}"
            )
    
    def validate_external_apis(self, apis: Dict[str, str]) -> ValidationResult:
        """Validate external API connections."""
        failed_apis = []
        
        for api_name, url in apis.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code >= 400:
                    failed_apis.append(f"{api_name} (HTTP {response.status_code})")
            except Exception as e:
                failed_apis.append(f"{api_name} ({str(e)})")
        
        if failed_apis:
            return ValidationResult(
                "External APIs",
                False,
                f"Failed to connect to: {', '.join(failed_apis)}"
            )
        
        return ValidationResult(
            "External APIs",
            True,
            f"All {len(apis)} external APIs are reachable"
        )
    
    def validate_file_permissions(self, paths: List[str]) -> ValidationResult:
        """Validate file and directory permissions."""
        failed_paths = []
        
        for path in paths:
            path_obj = Path(path)
            try:
                if not path_obj.exists():
                    path_obj.mkdir(parents=True, exist_ok=True)
                
                # Test write permissions
                test_file = path_obj / ".test_write"
                test_file.write_text("test")
                test_file.unlink()
                
            except Exception as e:
                failed_paths.append(f"{path} ({str(e)})")
        
        if failed_paths:
            return ValidationResult(
                "File Permissions",
                False,
                f"Permission issues with: {', '.join(failed_paths)}"
            )
        
        return ValidationResult(
            "File Permissions",
            True,
            f"All {len(paths)} paths have proper permissions"
        )
    
    def validate_dependencies(self, requirements_file: str = "requirements.txt") -> ValidationResult:
        """Validate that all Python dependencies are installed."""
        if not Path(requirements_file).exists():
            return ValidationResult(
                "Dependencies",
                False,
                f"{requirements_file} not found"
            )
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "check"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return ValidationResult(
                    "Dependencies",
                    False,
                    "Dependency issues found",
                    result.stdout + result.stderr
                )
            
            return ValidationResult(
                "Dependencies",
                True,
                "All dependencies are properly installed"
            )
        except Exception as e:
            return ValidationResult(
                "Dependencies",
                False,
                f"Failed to check dependencies: {str(e)}"
            )
    
    def validate_docker_environment(self) -> ValidationResult:
        """Validate Docker environment if running in container."""
        if not os.path.exists('/.dockerenv'):
            return ValidationResult(
                "Docker Environment",
                True,
                "Not running in Docker container"
            )
        
        # Check if we're in a Docker container
        try:
            with open('/proc/1/cgroup', 'r') as f:
                if 'docker' in f.read():
                    return ValidationResult(
                        "Docker Environment",
                        True,
                        "Running in Docker container"
                    )
        except:
            pass
        
        return ValidationResult(
            "Docker Environment",
            True,
            "Docker environment detected"
        )
    
    def run_validation(self, config: Dict[str, Any]) -> bool:
        """Run all validation checks."""
        print("🔍 Starting environment validation...\n")
        
        # Required environment variables
        if 'required_vars' in config:
            self.results.append(self.validate_required_vars(config['required_vars']))
        
        # Database connection
        if config.get('check_database', True):
            self.results.append(self.validate_database_connection())
        
        # Redis connection
        if config.get('check_redis', True):
            self.results.append(self.validate_redis_connection())
        
        # External APIs
        if 'external_apis' in config:
            self.results.append(self.validate_external_apis(config['external_apis']))
        
        # File permissions
        if 'required_paths' in config:
            self.results.append(self.validate_file_permissions(config['required_paths']))
        
        # Dependencies
        if config.get('check_dependencies', True):
            self.results.append(self.validate_dependencies())
        
        # Docker environment
        if config.get('check_docker', True):
            self.results.append(self.validate_docker_environment())
        
        return self.print_results()
    
    def print_results(self) -> bool:
        """Print validation results and return success status."""
        passed = 0
        failed = 0
        
        for result in self.results:
            status = "✅" if result.passed else "❌"
            print(f"{status} {result.check_name}: {result.message}")
            
            if result.details:
                print(f"   Details: {result.details}")
            
            if result.passed:
                passed += 1
            else:
                failed += 1
        
        print(f"\n📊 Results: {passed} passed, {failed} failed")
        
        if failed > 0:
            print("\n❌ Environment validation failed!")
            return False
        else:
            print("\n✅ Environment validation passed!")
            return True


def main():
    """Main function to run environment validation."""
    # Configuration for web app validation
    config = {
        'required_vars': [
            'DATABASE_URL',
            'REDIS_URL',
            'SECRET_KEY',
            'APP_NAME'
        ],
        'external_apis': {
            'health_check': 'http://localhost:8000/health',
        },
        'required_paths': [
            './uploads',
            './logs',
            './static'
        ],
        'check_database': True,
        'check_redis': True,
        'check_dependencies': True,
        'check_docker': True
    }
    
    validator = EnvironmentValidator()
    success = validator.run_validation(config)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()