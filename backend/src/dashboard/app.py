
from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
import logging
from pathlib import Path
import yaml
from datetime import timedelta

from .routes import register_routes
from ..utils.disk_space_manager import DiskSpaceManager
from ..utils.debug_timer import DebugTimer

logger = logging.getLogger(__name__)


def create_app(config_path: str = None):
    """Create and configure the Flask application"""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            app.config.update(yaml.safe_load(f))
    
    # Configure app
    app.config['SECRET_KEY'] = app.config.get('secret_key', 'dev-secret-key')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    
    # Enable CORS
    CORS(app)
    
    # Register routes
    register_routes(app)
    
    # Add template filters
    @app.template_filter('datetime')
    def datetime_filter(value, format='%Y-%m-%d %H:%M:%S'):
        if value:
            return value.strftime(format)
        return ''
    
    @app.template_filter('filesize')
    def filesize_filter(value):
        if value is None:
            return '0 B'
        for unit in ['B', 'KB', 'MB', 'GB']:
            if value < 1024.0:
                return f"{value:.1f} {unit}"
            value /= 1024.0
        return f"{value:.1f} TB"
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', 
                             error_code=404,
                             error_message="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return render_template('error.html',
                             error_code=500,
                             error_message="Internal server error"), 500
    
    # Context processors
    @app.context_processor
    def utility_processor():
        return {
            'disk_space': DiskSpaceManager.get_available_space_gb(),
            'app_name': 'AI ModelEval',
            'version': '2.0.0'
        }
    
    logger.info("Dashboard application created successfully")
    return app


def main():
    """Run the dashboard application"""
    app = create_app()
    app.run(
        host=app.config.get('host', '0.0.0.0'),
        port=app.config.get('port', 5000),
        debug=app.config.get('debug', False)
    )


if __name__ == '__main__':
    main()