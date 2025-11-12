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
        from main import NewsAnalyzer, get_config, get_utc_time
        
        # Load configuration (lazy loading)
        try:
            config = get_config()
        except FileNotFoundError as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"Configuration file not found: {str(e)}",
                    "type": "FileNotFoundError",
                    "hint": "Ensure config/config.yaml exists in the project root"
                })
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"Failed to load configuration: {str(e)}",
                    "type": type(e).__name__,
                    "hint": "Check config/config.yaml format and required fields"
                })
            }
        
        # Check if crawler is enabled
        if not config.get("ENABLE_CRAWLER", True):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "skipped",
                    "message": "Crawler is disabled in configuration"
                })
            }
        
        # Initialize and run analyzer
        try:
            analyzer = NewsAnalyzer()
            analyzer.run()
            
            now = get_utc_time()
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "success",
                    "message": "Crawler executed successfully",
                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
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
                    "message": f"Crawler execution failed: {str(e)}",
                    "type": type(e).__name__,
                    "traceback": error_trace
                })
            }
        
    except ImportError as e:
        import traceback
        error_trace = traceback.format_exc()
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": f"Import error: {str(e)}",
                "type": "ImportError",
                "traceback": error_trace,
                "hint": "Check requirements.txt and ensure all dependencies are installed"
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
