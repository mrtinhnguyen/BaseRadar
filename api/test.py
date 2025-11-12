"""
Simple test handler for Vercel to verify Python function works
"""
import json
import sys
import os

# Wrap everything in try-except to catch module-level errors
try:
    # Minimal module-level code
    pass
except Exception as e:
    import sys
    print(f"Module-level error in test.py: {e}", file=sys.stderr)
    # Don't raise - allow handler to be defined

def handler(request):
    """
    Simple test handler for Vercel
    
    Args:
        request: Vercel request object (dict with method, path, headers, body, etc.)
    
    Returns:
        dict: Response with statusCode, headers, body
    """
    # Wrap entire handler in try-except
    try:
        # Log to stderr immediately - Vercel captures this
        print("=" * 50, file=sys.stderr)
        print("TEST HANDLER STARTED", file=sys.stderr)
        print(f"Python version: {sys.version}", file=sys.stderr)
        print(f"Request type: {type(request)}", file=sys.stderr)
        if isinstance(request, dict):
            print(f"Request keys: {list(request.keys())}", file=sys.stderr)
        elif hasattr(request, '__dict__'):
            print(f"Request attributes: {dir(request)}", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        # Return response
        response_body = {
            "status": "success",
            "message": "Test handler works!",
            "python_version": sys.version.split()[0] if sys.version else "unknown",
            "request_type": str(type(request))
        }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response_body, ensure_ascii=False)
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR in handler: {e}", file=sys.stderr)
        print(error_trace, file=sys.stderr)
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "status": "error",
                "message": str(e),
                "type": type(e).__name__,
                "traceback": error_trace
            }, ensure_ascii=False)
        }
