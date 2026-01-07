"""
Authentication management for SKU CLI
Handles GitHub authentication for private repository
"""

import yaml
from pathlib import Path
from typing import Optional
from .utils import console, error, success

class AuthManager:
    """Manages GitHub authentication"""

    def __init__(self):
        """Initialize auth manager"""
        self.config_dir = Path.home() / ".sku"
        self.config_file = self.config_dir / "config.yaml"

    def login(self, token: Optional[str] = None):
        """Login to GitHub

        Args:
            token: GitHub personal access token (if None, will prompt)
        """
        # Get token
        if not token:
            import os
            token = os.environ.get('GITHUB_TOKEN')

            if not token:
                from questionary import prompt
                answer = prompt({
                    'type': 'password',
                    'name': 'token',
                    'message': 'GitHub Personal Access Token:'
                })
                token = answer['token']

        # Validate token
        if not self._validate_token(token):
            error("✗ Invalid token")
            return

        # Save config
        self.config_dir.mkdir(parents=True, exist_ok=True)

        config = {}
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)

        config['github'] = {
            'token': token,
            'authenticated_at': self._get_timestamp()
        }

        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        success("✓ Authenticated successfully")

    def logout(self):
        """Logout and clear credentials"""
        if not self.config_file.exists():
            error("Not logged in")
            return

        # Remove token from config
        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)

        if 'github' in config:
            del config['github']['token']

        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        success("✓ Logged out successfully")

    def _validate_token(self, token: str) -> bool:
        """Validate GitHub token

        Args:
            token: Token to validate

        Returns:
            True if valid
        """
        import requests

        try:
            response = requests.get(
                'https://api.github.com/user',
                headers={'Authorization': f'token {token}'},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def _get_timestamp(self) -> str:
        """Get current timestamp

        Returns:
            ISO format timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat()
