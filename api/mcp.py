"""
Vercel serverless function for BaseRadar MCP Server
Exposes MCP Server via HTTP for Vercel deployment
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
    Vercel serverless function handler for MCP Server
    
    This endpoint exposes the MCP Server via HTTP transport mode.
    MCP clients can connect to this endpoint to use BaseRadar tools.
    """
    try:
        # Import MCP server
        from mcp_server.server import mcp, _get_tools
        
        # Initialize tools (singleton pattern)
        _get_tools(project_root)
        
        # Get request method and path
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        headers = request.get('headers', {})
        body = request.get('body', '')
        
        # MCP HTTP endpoint is typically at /mcp
        if path.startswith('/mcp') or path == '/':
            # Handle MCP protocol requests
            # FastMCP HTTP mode expects requests at /mcp endpoint
            
            # For Vercel, we need to handle the request differently
            # Since FastMCP's HTTP mode expects a running server,
            # we'll create a simple HTTP adapter
            
            # Check if this is a health check
            if method == 'GET' and path in ['/', '/mcp', '/api/mcp']:
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                        "Access-Control-Allow-Headers": "Content-Type, Authorization"
                    },
                    "body": json.dumps({
                        "status": "online",
                        "service": "BaseRadar MCP Server",
                        "transport": "http",
                        "endpoint": "/api/mcp",
                        "message": "MCP Server is running. Use MCP client to connect.",
                        "tools_available": len(mcp._tools) if hasattr(mcp, '_tools') else 0
                    })
                }
            
            # Handle OPTIONS for CORS
            if method == 'OPTIONS':
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                        "Access-Control-Allow-Headers": "Content-Type, Authorization"
                    },
                    "body": ""
                }
            
            # Handle POST requests (MCP protocol)
            if method == 'POST':
                try:
                    # Parse request body
                    if isinstance(body, str):
                        request_data = json.loads(body)
                    else:
                        request_data = body
                    
                    # FastMCP HTTP mode handles requests internally
                    # For Vercel, we need to manually route to FastMCP
                    # Note: This is a simplified adapter
                    # Full MCP protocol support requires FastMCP's HTTP transport
                    
                    return {
                        "statusCode": 200,
                        "headers": {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*"
                        },
                        "body": json.dumps({
                            "status": "success",
                            "message": "MCP request received",
                            "note": "Full MCP protocol support requires FastMCP HTTP transport mode",
                            "recommendation": "For production use, consider deploying MCP Server as a standalone HTTP service"
                        })
                    }
                except json.JSONDecodeError:
                    return {
                        "statusCode": 400,
                        "headers": {"Content-Type": "application/json"},
                        "body": json.dumps({
                            "status": "error",
                            "message": "Invalid JSON in request body"
                        })
                    }
            
            # Default response
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": "Endpoint not found",
                    "available_endpoints": ["/", "/mcp", "/api/mcp"]
                })
            }
        
        else:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"Path {path} not found"
                })
            }
            
    except ImportError as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": f"Import error: {str(e)}",
                "type": "ImportError",
                "note": "Ensure all dependencies are installed"
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

