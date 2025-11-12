"""
Ultra-minimal handler - no imports, no nothing
Just to test if Vercel can call Python functions at all
"""
import sys

def handler(request):
    """
    Minimal Vercel Python handler
    
    Args:
        request: Vercel request object (dict or object, can be None)
    
    Returns:
        dict: Response with statusCode, headers, body
    """
    try:
        # Log to stderr for debugging (Vercel captures this)
        print("=" * 50, file=sys.stderr)
        print("Minimal handler called", file=sys.stderr)
        print(f"Request type: {type(request)}", file=sys.stderr)
        print(f"Request value: {request}", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        # Handle None or unexpected request types
        if request is None:
            print("Warning: request is None", file=sys.stderr)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": '{"status":"ok","message":"minimal handler works"}'
        }
    except Exception as e:
        # Catch any unexpected errors
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR in minimal handler: {e}", file=sys.stderr)
        print(error_trace, file=sys.stderr)
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": f'{{"status":"error","message":"{str(e)}","type":"{type(e).__name__}"}}'
        }

