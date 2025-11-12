"""
Simple test handler for Vercel to verify Python function works
"""
import json
import sys

def handler(request):
    """
    Simple test handler
    """
    try:
        # Log to stderr immediately
        print("=" * 50, file=sys.stderr)
        print("TEST HANDLER STARTED", file=sys.stderr)
        print(f"Python version: {sys.version}", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "success",
                "message": "Test handler works!",
                "python_version": sys.version
            }, ensure_ascii=False)
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR: {e}", file=sys.stderr)
        print(error_trace, file=sys.stderr)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": str(e),
                "traceback": error_trace
            }, ensure_ascii=False)
        }

