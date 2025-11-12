"""
Vercel serverless function for BaseRadar
"""
import json
import sys
import os
from http.server import BaseHTTPRequestHandler

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def handler(request):
    """
    Vercel serverless function handler
    """
    try:
        # Import here to avoid issues with Vercel's cold start
        from main import NewsAnalyzer, load_config
        
        # Load configuration
        CONFIG = load_config()
        
        # Check if crawler is enabled
        if not CONFIG.get("ENABLE_CRAWLER", True):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "skipped",
                    "message": "Crawler is disabled in configuration"
                })
            }
        
        # Initialize and run analyzer
        analyzer = NewsAnalyzer()
        analyzer.run()
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "success",
                "message": "Crawler executed successfully",
                "timestamp": analyzer.now.strftime("%Y-%m-%d %H:%M:%S") if hasattr(analyzer, 'now') else None
            })
        }
        
    except ImportError as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": f"Import error: {str(e)}",
                "type": "ImportError"
            })
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": str(e),
                "type": type(e).__name__,
                "traceback": error_trace
            })
        }

