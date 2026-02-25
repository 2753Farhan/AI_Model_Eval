"""
CLI module for command-line interface.

This module provides command-line interface functionality for the AI Model Evaluation framework.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def setup_logging(log_level: str = 'INFO') -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description='AI Model Evaluation Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Run evaluation
  python main.py eval --models ollama huggingface --samples 10
  
  # Start dashboard
  python main.py dashboard --host 0.0.0.0 --port 5000
  
  # Generate report
  python main.py report --input results/evaluation.json --format html
        '''
    )
    
    # Global options
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set logging level (default: INFO)'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Eval command
    eval_parser = subparsers.add_parser('eval', help='Run evaluation')
    eval_parser.add_argument(
        '--models',
        nargs='+',
        required=True,
        help='Models to evaluate'
    )
    eval_parser.add_argument(
        '--dataset',
        default='humaneval',
        help='Dataset to use (default: humaneval)'
    )
    eval_parser.add_argument(
        '--samples',
        type=int,
        default=5,
        help='Number of samples (default: 5)'
    )
    eval_parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Timeout in seconds (default: 30)'
    )
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Start web dashboard')
    dashboard_parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    dashboard_parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind to (default: 5000)'
    )
    dashboard_parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument(
        '--input',
        required=True,
        help='Input evaluation results file'
    )
    report_parser.add_argument(
        '--format',
        choices=['html', 'pdf', 'csv', 'json'],
        default='html',
        help='Output format (default: html)'
    )
    report_parser.add_argument(
        '--output',
        help='Output file path'
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'eval':
            logger.info(f'Starting evaluation with models: {args.models}')
            # Evaluation logic would go here
            
        elif args.command == 'dashboard':
            logger.info(f'Starting dashboard on {args.host}:{args.port}')
            # Dashboard startup logic would go here
            
        elif args.command == 'report':
            logger.info(f'Generating report from {args.input}')
            # Report generation logic would go here
            
        return 0
        
    except Exception as e:
        logger.error(f'Error: {e}', exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
