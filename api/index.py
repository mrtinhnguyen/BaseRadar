"""
Vercel serverless function for BaseRadar
"""
# Wrap all imports in try-except to prevent module-level crashes
try:
    import json
    import sys
    import os
    
    # DO NOT import anything that might fail at module level
    # All imports should be inside handler function
    
    # Add project root to path (safe operation)
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
    except Exception as e:
        # If even this fails, we'll handle it in handler
        project_root = None
        print(f"Warning: Could not set project_root at module level: {e}", file=sys.stderr)
except Exception as e:
    # Catch any import errors at module level
    import sys
    print(f"CRITICAL: Module-level import error in api/index.py: {e}", file=sys.stderr)
    import traceback
    print(traceback.format_exc(), file=sys.stderr)
    # Set defaults so handler can still be defined
    project_root = None

def handler(request):
    """
    Vercel serverless function handler
    
    Args:
        request: Vercel request object with method, path, headers, body
        
    Returns:
        dict: Response with statusCode, headers, body
    """
    # Import logging inside handler to avoid module-level issues
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Log to stderr (Vercel captures this) - this is the FIRST thing we do
        print("=" * 50, file=sys.stderr)
        print("BaseRadar API Handler Started", file=sys.stderr)
        print(f"Python version: {sys.version}", file=sys.stderr)
        
        # Ensure project_root is set
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, project_root)
        
        print(f"Project root: {project_root}", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        logger.info("Handler called")
        
        # Set Vercel environment flag before importing main
        os.environ["VERCEL"] = "1"
        logger.info(f"Project root: {project_root}")
        
        # Check if config file exists
        config_path = os.path.join(project_root, "config", "config.yaml")
        print(f"Checking config file: {config_path}", file=sys.stderr)
        print(f"Config file exists: {os.path.exists(config_path)}", file=sys.stderr)
        
        if not os.path.exists(config_path):
            error_msg = f"Config file not found at: {config_path}"
            print(f"ERROR: {error_msg}", file=sys.stderr)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": error_msg,
                    "type": "FileNotFoundError",
                    "hint": "Ensure config/config.yaml exists in the project root",
                    "project_root": project_root,
                    "files_in_root": os.listdir(project_root) if os.path.exists(project_root) else []
                }, ensure_ascii=False)
            }
        
        # Import here to avoid issues with Vercel's cold start
        # This imports main.py which is the entry point when running directly
        try:
            print("Importing main module...", file=sys.stderr)
            logger.info("Importing main module...")
            
            # Set VERCEL flag BEFORE importing to prevent auto-loading config
            os.environ["VERCEL"] = "1"
            
            from main import NewsAnalyzer, get_config, get_utc_time
            print("Main module imported successfully", file=sys.stderr)
            logger.info("Main module imported successfully")
        except ImportError as import_error:
            import traceback
            error_trace = traceback.format_exc()
            print(f"IMPORT ERROR: {import_error}", file=sys.stderr)
            print(error_trace, file=sys.stderr)
            logger.error(f"Import error: {import_error}")
            logger.error(error_trace)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"Failed to import main module: {str(import_error)}",
                    "type": "ImportError",
                    "traceback": error_trace,
                    "hint": "Check if all dependencies are installed. Common issues: missing packages in requirements.txt, syntax errors in main.py or crawlers.py",
                    "project_root": project_root
                }, ensure_ascii=False)
            }
        except Exception as import_error:
            import traceback
            error_trace = traceback.format_exc()
            print(f"MODULE LEVEL ERROR: {import_error}", file=sys.stderr)
            print(error_trace, file=sys.stderr)
            logger.error(f"Module-level error: {import_error}")
            logger.error(error_trace)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"Error during module import: {str(import_error)}",
                    "type": type(import_error).__name__,
                    "traceback": error_trace,
                    "hint": "This error occurred at module level. Check main.py for code that runs on import.",
                    "project_root": project_root
                }, ensure_ascii=False)
            }
        
        # Load configuration (lazy loading)
        try:
            logger.info("Loading configuration...")
            config = get_config()
            logger.info("Configuration loaded successfully")
        except FileNotFoundError as e:
            logger.error(f"Config file not found: {e}")
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"Configuration file not found: {str(e)}",
                    "type": "FileNotFoundError",
                    "hint": "Ensure config/config.yaml exists in the project root",
                    "project_root": project_root
                }, ensure_ascii=False)
            }
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            logger.error(f"Config load error: {e}")
            logger.error(error_trace)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"Failed to load configuration: {str(e)}",
                    "type": type(e).__name__,
                    "hint": "Check config/config.yaml format and required fields",
                    "traceback": error_trace
                }, ensure_ascii=False)
            }
        
        # Check if crawler is enabled
        if not config.get("ENABLE_CRAWLER", True):
            logger.info("Crawler is disabled in configuration")
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "skipped",
                    "message": "Crawler is disabled in configuration"
                }, ensure_ascii=False)
            }
        
        # Initialize and run analyzer
        # This mimics running: python main.py
        try:
            print("Initializing NewsAnalyzer...", file=sys.stderr)
            logger.info("Initializing NewsAnalyzer...")
            analyzer = NewsAnalyzer()
            print("Running analyzer.run()...", file=sys.stderr)
            logger.info("Running analyzer...")
            analyzer.run()
            print("Analyzer completed successfully", file=sys.stderr)
            logger.info("Analyzer completed successfully")
            
            now = get_utc_time()
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "success",
                    "message": "Crawler executed successfully",
                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
                }, ensure_ascii=False)
            }
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"CRITICAL ERROR in analyzer.run(): {e}", file=sys.stderr)
            print(error_trace, file=sys.stderr)
            logger.error(f"Crawler execution error: {e}")
            logger.error(error_trace)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"Crawler execution failed: {str(e)}",
                    "type": type(e).__name__,
                    "traceback": error_trace
                }, ensure_ascii=False)
            }
        
    except ImportError as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Top-level import error: {e}")
        logger.error(error_trace)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": f"Import error: {str(e)}",
                "type": "ImportError",
                "traceback": error_trace,
                "hint": "Check requirements.txt and ensure all dependencies are installed",
                "project_root": project_root
            }, ensure_ascii=False)
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Unexpected error: {e}")
        logger.error(error_trace)
        
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": str(e),
                "type": type(e).__name__,
                "traceback": error_trace,
                "project_root": project_root
            }, ensure_ascii=False)
        }
