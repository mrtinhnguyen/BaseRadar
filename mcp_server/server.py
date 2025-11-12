"""
BaseRadar MCP Server - FastMCP 2.0 Implementation

Provides production-grade MCP tool server using FastMCP 2.0.
Supports both stdio and HTTP transport modes.
"""

import json
from typing import List, Optional, Dict

from fastmcp import FastMCP

from .tools.data_query import DataQueryTools
from .tools.analytics import AnalyticsTools
from .tools.search_tools import SearchTools
from .tools.config_mgmt import ConfigManagementTools
from .tools.system import SystemManagementTools


# Create FastMCP 2.0 application
mcp = FastMCP('baseradar-news')

# Global tool instances (initialized on first request)
_tools_instances = {}


def _get_tools(project_root: Optional[str] = None):
    """Get or create tool instances (singleton pattern)"""
    if not _tools_instances:
        _tools_instances['data'] = DataQueryTools(project_root)
        _tools_instances['analytics'] = AnalyticsTools(project_root)
        _tools_instances['search'] = SearchTools(project_root)
        _tools_instances['config'] = ConfigManagementTools(project_root)
        _tools_instances['system'] = SystemManagementTools(project_root)
    return _tools_instances


# ==================== Data Query Tools ====================

@mcp.tool
async def get_latest_news(
    platforms: Optional[List[str]] = None,
    limit: int = 50,
    include_url: bool = False
) -> str:
    """
    Get the latest batch of crawled news data to quickly understand current hot topics

    Args:
        platforms: Platform ID list, e.g., ['coindesk', 'cointelegraph', 'decrypt']
                   - If not specified: uses all platforms configured in config.yaml
                   - Supported platforms come from config/config.yaml platforms configuration
                   - Each platform has a corresponding name field for AI recognition
        limit: Return count limit, default 50, maximum 1000
               Note: Actual return count may be less than requested, depending on total available news
        include_url: Whether to include URL links, default False (saves tokens)

    Returns:
        JSON format news list

    **Important: Data Display Recommendations**
    This tool returns a complete news list (usually 50 items). Please note:
    - **Tool returns**: Complete 50 items of data ✅
    - **Recommended display**: Show all data to users unless they explicitly request a summary
    - **User expectations**: Users may need complete data, please summarize with caution

    **When to summarize**:
    - User explicitly says "summarize for me" or "highlight the key points"
    - When data exceeds 100 items, you can show partial data first and ask if they want to see all

    **Note**: If user asks "why only part is shown", it means they need complete data
    """
    tools = _get_tools()
    result = tools['data'].get_latest_news(platforms=platforms, limit=limit, include_url=include_url)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def get_trending_topics(
    top_n: int = 10,
    mode: str = 'current'
) -> str:
    """
    Get news frequency statistics for personal keywords of interest (based on config/frequency_words.txt)

    Note: This tool does not automatically extract news hot topics, but rather counts the frequency
    of your personal keywords of interest set in config/frequency_words.txt in the news.
    You can customize this keyword list.

    Args:
        top_n: Return TOP N keywords of interest, default 10
        mode: Mode selection
            - daily: Daily cumulative data statistics
            - current: Latest batch data statistics (default)

    Returns:
        JSON format keyword frequency statistics list
    """
    tools = _get_tools()
    result = tools['data'].get_trending_topics(top_n=top_n, mode=mode)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def get_news_by_date(
    date_query: Optional[str] = None,
    platforms: Optional[List[str]] = None,
    limit: int = 50,
    include_url: bool = False
) -> str:
    """
    Get news data for a specified date, for historical data analysis and comparison

    Args:
        date_query: Date query, optional formats:
            - Natural language: "today", "yesterday", "day before yesterday", "3 days ago"
            - Standard date: "2024-01-15", "2024/01/15"
            - Default: "today" (saves tokens)
        platforms: Platform ID list, e.g., ['coindesk', 'cointelegraph', 'decrypt']
                   - If not specified: uses all platforms configured in config.yaml
                   - Supported platforms come from config/config.yaml platforms configuration
                   - Each platform has a corresponding name field for AI recognition
        limit: Return count limit, default 50, maximum 1000
               Note: Actual return count may be less than requested, depending on total news for the specified date
        include_url: Whether to include URL links, default False (saves tokens)

    Returns:
        JSON format news list, including title, platform, rank, etc.

    **Important: Data Display Recommendations**
    This tool returns a complete news list (usually 50 items). Please note:
    - **Tool returns**: Complete 50 items of data ✅
    - **Recommended display**: Show all data to users unless they explicitly request a summary
    - **User expectations**: Users may need complete data, please summarize with caution

    **When to summarize**:
    - User explicitly says "summarize for me" or "highlight the key points"
    - When data exceeds 100 items, you can show partial data first and ask if they want to see all

    **Note**: If user asks "why only part is shown", it means they need complete data
    """
    tools = _get_tools()
    result = tools['data'].get_news_by_date(
        date_query=date_query,
        platforms=platforms,
        limit=limit,
        include_url=include_url
    )
    return json.dumps(result, ensure_ascii=False, indent=2)



# ==================== Advanced Data Analysis Tools ====================

@mcp.tool
async def analyze_topic_trend(
    topic: str,
    analysis_type: str = "trend",
    date_range: Optional[Dict[str, str]] = None,
    granularity: str = "day",
    threshold: float = 3.0,
    time_window: int = 24,
    lookahead_hours: int = 6,
    confidence_threshold: float = 0.7
) -> str:
    """
    Unified topic trend analysis tool - integrates multiple trend analysis modes

    Args:
        topic: Topic keyword (required)
        analysis_type: Analysis type, options:
            - "trend": Heat trend analysis (tracks topic heat changes)
            - "lifecycle": Lifecycle analysis (complete cycle from appearance to disappearance)
            - "viral": Abnormal heat detection (identifies suddenly trending topics)
            - "predict": Topic prediction (predicts future possible hot topics)
        date_range: Date range (for trend and lifecycle modes), optional
                    - **Format**: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
                    - **Example**: {"start": "2025-10-18", "end": "2025-10-25"}
                    - **Note**: AI needs to automatically calculate date range based on user's natural language (e.g., "last 7 days")
                    - **Default**: If not specified, defaults to analyzing last 7 days
        granularity: Time granularity (trend mode), default "day" (only supports day, as underlying data is aggregated by day)
        threshold: Heat surge multiplier threshold (viral mode), default 3.0
        time_window: Detection time window in hours (viral mode), default 24
        lookahead_hours: Predict future hours (predict mode), default 6
        confidence_threshold: Confidence threshold (predict mode), default 0.7

    Returns:
        JSON format trend analysis results

    **AI Usage Instructions:**
    When users use relative time expressions (e.g., "last 7 days", "past week", "last month"),
    AI needs to automatically calculate the corresponding date range and pass it to the date_range parameter.

    Examples:
        - analyze_topic_trend(topic="artificial intelligence", analysis_type="trend", date_range={"start": "2025-10-18", "end": "2025-10-25"})
        - analyze_topic_trend(topic="Tesla", analysis_type="lifecycle", date_range={"start": "2025-10-18", "end": "2025-10-25"})
        - analyze_topic_trend(topic="Bitcoin", analysis_type="viral", threshold=3.0)
        - analyze_topic_trend(topic="ChatGPT", analysis_type="predict", lookahead_hours=6)
    """
    tools = _get_tools()
    result = tools['analytics'].analyze_topic_trend_unified(
        topic=topic,
        analysis_type=analysis_type,
        date_range=date_range,
        granularity=granularity,
        threshold=threshold,
        time_window=time_window,
        lookahead_hours=lookahead_hours,
        confidence_threshold=confidence_threshold
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def analyze_data_insights(
    insight_type: str = "platform_compare",
    topic: Optional[str] = None,
    date_range: Optional[Dict[str, str]] = None,
    min_frequency: int = 3,
    top_n: int = 20
) -> str:
    """
    Unified data insights analysis tool - integrates multiple data analysis modes

    Args:
        insight_type: Insight type, options:
            - "platform_compare": Platform comparison analysis (compares different platforms' attention to topics)
            - "platform_activity": Platform activity statistics (statistics on publishing frequency and active times)
            - "keyword_cooccur": Keyword co-occurrence analysis (analyzes patterns of keywords appearing together)
        topic: Topic keyword (optional, applicable to platform_compare mode)
        date_range: **【Object type】** Date range (optional)
                    - **Format**: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
                    - **Example**: {"start": "2025-01-01", "end": "2025-01-07"}
                    - **Important**: Must be object format, cannot pass integer
        min_frequency: Minimum co-occurrence frequency (keyword_cooccur mode), default 3
        top_n: Return TOP N results (keyword_cooccur mode), default 20

    Returns:
        JSON format data insights analysis results

    Examples:
        - analyze_data_insights(insight_type="platform_compare", topic="artificial intelligence")
        - analyze_data_insights(insight_type="platform_activity", date_range={"start": "2025-01-01", "end": "2025-01-07"})
        - analyze_data_insights(insight_type="keyword_cooccur", min_frequency=5, top_n=15)
    """
    tools = _get_tools()
    result = tools['analytics'].analyze_data_insights_unified(
        insight_type=insight_type,
        topic=topic,
        date_range=date_range,
        min_frequency=min_frequency,
        top_n=top_n
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def analyze_sentiment(
    topic: Optional[str] = None,
    platforms: Optional[List[str]] = None,
    date_range: Optional[Dict[str, str]] = None,
    limit: int = 50,
    sort_by_weight: bool = True,
    include_url: bool = False
) -> str:
    """
    Analyze news sentiment tendency and heat trends

    Args:
        topic: Topic keyword (optional)
        platforms: Platform ID list, e.g., ['coindesk', 'cointelegraph', 'decrypt']
                   - If not specified: uses all platforms configured in config.yaml
                   - Supported platforms come from config/config.yaml platforms configuration
                   - Each platform has a corresponding name field for AI recognition
        date_range: **【Object type】** Date range (optional)
                    - **Format**: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
                    - **Example**: {"start": "2025-01-01", "end": "2025-01-07"}
                    - **Important**: Must be object format, cannot pass integer
        limit: Return news count, default 50, maximum 100
               Note: This tool deduplicates news titles (same title on different platforms only kept once),
               so actual return count may be less than requested limit value
        sort_by_weight: Whether to sort by heat weight, default True
        include_url: Whether to include URL links, default False (saves tokens)

    Returns:
        JSON format analysis results, including sentiment distribution, heat trends, and related news

    **Important: Data Display Strategy**
    - This tool returns complete analysis results and news list
    - **Default display**: Show complete analysis results (including all news)
    - Only filter when user explicitly requests "summary" or "highlight key points"
    """
    tools = _get_tools()
    result = tools['analytics'].analyze_sentiment(
        topic=topic,
        platforms=platforms,
        date_range=date_range,
        limit=limit,
        sort_by_weight=sort_by_weight,
        include_url=include_url
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def find_similar_news(
    reference_title: str,
    threshold: float = 0.6,
    limit: int = 50,
    include_url: bool = False
) -> str:
    """
    Find other news similar to the specified news title

    Args:
        reference_title: News title (complete or partial)
        threshold: Similarity threshold, between 0-1, default 0.6
                   Note: Higher threshold means stricter matching, fewer results
        limit: Return count limit, default 50, maximum 100
               Note: Actual return count depends on similarity matching results, may be less than requested
        include_url: Whether to include URL links, default False (saves tokens)

    Returns:
        JSON format similar news list, including similarity scores

    **Important: Data Display Strategy**
    - This tool returns complete similar news list
    - **Default display**: Show all returned news (including similarity scores)
    - Only filter when user explicitly requests "summary" or "highlight key points"
    """
    tools = _get_tools()
    result = tools['analytics'].find_similar_news(
        reference_title=reference_title,
        threshold=threshold,
        limit=limit,
        include_url=include_url
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def generate_summary_report(
    report_type: str = "daily",
    date_range: Optional[Dict[str, str]] = None
) -> str:
    """
    Daily/Weekly summary generator - automatically generates hot topic summary reports

    Args:
        report_type: Report type (daily/weekly)
        date_range: **【Object type】** Custom date range (optional)
                    - **Format**: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
                    - **Example**: {"start": "2025-01-01", "end": "2025-01-07"}
                    - **Important**: Must be object format, cannot pass integer

    Returns:
        JSON format summary report, including Markdown format content
    """
    tools = _get_tools()
    result = tools['analytics'].generate_summary_report(
        report_type=report_type,
        date_range=date_range
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


# ==================== Intelligent Search Tools ====================

@mcp.tool
async def search_news(
    query: str,
    search_mode: str = "keyword",
    date_range: Optional[Dict[str, str]] = None,
    platforms: Optional[List[str]] = None,
    limit: int = 50,
    sort_by: str = "relevance",
    threshold: float = 0.6,
    include_url: bool = False
) -> str:
    """
    Unified search interface supporting multiple search modes

    Args:
        query: Search keyword or content fragment
        search_mode: Search mode, options:
            - "keyword": Exact keyword matching (default, suitable for searching specific topics)
            - "fuzzy": Fuzzy content matching (suitable for searching content fragments, filters results below threshold)
            - "entity": Entity name search (suitable for searching people/places/organizations)
        date_range: Date range (optional)
                    - **Format**: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
                    - **Example**: {"start": "2025-01-01", "end": "2025-01-07"}
                    - **Note**: AI needs to automatically calculate date range based on user's natural language (e.g., "last 7 days")
                    - **Default**: If not specified, defaults to querying today's news
                    - **Note**: start and end can be the same (represents single day query)
        platforms: Platform ID list, e.g., ['coindesk', 'cointelegraph', 'decrypt']
                   - If not specified: uses all platforms configured in config.yaml
                   - Supported platforms come from config/config.yaml platforms configuration
                   - Each platform has a corresponding name field for AI recognition
        limit: Return count limit, default 50, maximum 1000
               Note: Actual return count depends on search matching results (especially fuzzy mode filters low similarity results)
        sort_by: Sort method, options:
            - "relevance": Sort by relevance (default)
            - "weight": Sort by news weight
            - "date": Sort by date
        threshold: Similarity threshold (only effective in fuzzy mode), between 0-1, default 0.6
                   Note: Higher threshold means stricter matching, fewer results
        include_url: Whether to include URL links, default False (saves tokens)

    Returns:
        JSON format search results, including title, platform, rank, etc.

    **Important: Data Display Strategy**
    - This tool returns complete search results list
    - **Default display**: Show all returned news, no need to summarize or filter
    - Only filter when user explicitly requests "summary" or "highlight key points"

    **AI Usage Instructions:**
    When users use relative time expressions (e.g., "last 7 days", "past week", "last half month"),
    AI needs to automatically calculate the corresponding date range. Calculation rules:
    - "last 7 days" → {"start": "today-6 days", "end": "today"}
    - "past week" → {"start": "today-6 days", "end": "today"}
    - "last 30 days" → {"start": "today-29 days", "end": "today"}

    Examples:
        - Today's news: search_news(query="artificial intelligence")
        - Last 7 days: search_news(query="artificial intelligence", date_range={"start": "2025-10-18", "end": "2025-10-25"})
        - Exact date: search_news(query="artificial intelligence", date_range={"start": "2025-01-01", "end": "2025-01-07"})
        - Fuzzy search: search_news(query="Tesla price cut", search_mode="fuzzy", threshold=0.4)
    """
    tools = _get_tools()
    result = tools['search'].search_news_unified(
        query=query,
        search_mode=search_mode,
        date_range=date_range,
        platforms=platforms,
        limit=limit,
        sort_by=sort_by,
        threshold=threshold,
        include_url=include_url
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def search_related_news_history(
    reference_text: str,
    time_preset: str = "yesterday",
    threshold: float = 0.4,
    limit: int = 50,
    include_url: bool = False
) -> str:
    """
    Search related news in historical data based on seed news

    Args:
        reference_text: Reference news title (complete or partial)
        time_preset: Time range preset, options:
            - "yesterday": Yesterday
            - "last_week": Last week (7 days)
            - "last_month": Last month (30 days)
            - "custom": Custom date range (requires start_date and end_date)
        threshold: Relevance threshold, between 0-1, default 0.4
                   Note: Comprehensive similarity calculation (70% keyword overlap + 30% text similarity)
                   Higher threshold means stricter matching, fewer results
        limit: Return count limit, default 50, maximum 100
               Note: Actual return count depends on relevance matching results, may be less than requested
        include_url: Whether to include URL links, default False (saves tokens)

    Returns:
        JSON format related news list, including relevance scores and time distribution

    **Important: Data Display Strategy**
    - This tool returns complete related news list
    - **Default display**: Show all returned news (including relevance scores)
    - Only filter when user explicitly requests "summary" or "highlight key points"
    """
    tools = _get_tools()
    result = tools['search'].search_related_news_history(
        reference_text=reference_text,
        time_preset=time_preset,
        threshold=threshold,
        limit=limit,
        include_url=include_url
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


# ==================== Configuration and System Management Tools ====================

@mcp.tool
async def get_current_config(
    section: str = "all"
) -> str:
    """
    Get current system configuration

    Args:
        section: Configuration section, options:
            - "all": All configurations (default)
            - "crawler": Crawler configuration
            - "notification": Notification configuration
            - "keywords": Keywords configuration
            - "weights": Weights configuration

    Returns:
        JSON format configuration information
    """
    tools = _get_tools()
    result = tools['config'].get_current_config(section=section)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def get_system_status() -> str:
    """
    Get system running status and health check information

    Returns system version, data statistics, cache status, etc.

    Returns:
        JSON format system status information
    """
    tools = _get_tools()
    result = tools['system'].get_system_status()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
async def trigger_crawl(
    platforms: Optional[List[str]] = None,
    save_to_local: bool = False,
    include_url: bool = False
) -> str:
    """
    Manually trigger a crawl task (optional persistence)

    Args:
        platforms: Specified platform ID list, e.g., ['coindesk', 'cointelegraph', 'decrypt']
                   - If not specified: uses all platforms configured in config.yaml
                   - Supported platforms come from config/config.yaml platforms configuration
                   - Each platform has a corresponding name field for AI recognition
                   - Note: Failed platforms will be listed in the failed_platforms field of the return result
        save_to_local: Whether to save to local output directory, default False
        include_url: Whether to include URL links, default False (saves tokens)

    Returns:
        JSON format task status information, including:
        - platforms: List of successfully crawled platforms
        - failed_platforms: List of failed platforms (if any)
        - total_news: Total number of crawled news
        - data: News data

    Examples:
        - Temporary crawl: trigger_crawl(platforms=['coindesk'])
        - Crawl and save: trigger_crawl(platforms=['cointelegraph'], save_to_local=True)
        - Use default platforms: trigger_crawl()  # Crawls all platforms configured in config.yaml
    """
    tools = _get_tools()
    result = tools['system'].trigger_crawl(platforms=platforms, save_to_local=save_to_local, include_url=include_url)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ==================== Server Startup Entry ====================

def run_server(
    project_root: Optional[str] = None,
    transport: str = 'stdio',
    host: str = '0.0.0.0',
    port: int = 3333
):
    """
    Start MCP server

    Args:
        project_root: Project root directory path
        transport: Transport mode, 'stdio' or 'http'
        host: HTTP mode listen address, default 0.0.0.0
        port: HTTP mode listen port, default 3333
    """
    # Initialize tool instances
    _get_tools(project_root)

    # Print startup information
    print()
    print("=" * 60)
    print("  BaseRadar MCP Server - FastMCP 2.0")
    print("=" * 60)
    print(f"  Transport Mode: {transport.upper()}")

    if transport == 'stdio':
        print("  Protocol: MCP over stdio (standard input/output)")
        print("  Description: Communicates with MCP client via standard input/output")
    elif transport == 'http':
        print(f"  Listen Address: http://{host}:{port}")
        print(f"  HTTP Endpoint: http://{host}:{port}/mcp")
        print("  Protocol: MCP over HTTP (production environment)")

    if project_root:
        print(f"  Project Directory: {project_root}")
    else:
        print("  Project Directory: Current directory")

    print()
    print("  Registered Tools:")
    print("    === Basic Data Query (P0 Core) ===")
    print("    1. get_latest_news        - Get latest news")
    print("    2. get_news_by_date       - Query news by date (supports natural language)")
    print("    3. get_trending_topics    - Get trending topics")
    print()
    print("    === Intelligent Search Tools ===")
    print("    4. search_news                  - Unified news search (keyword/fuzzy/entity)")
    print("    5. search_related_news_history  - Historical related news search")
    print()
    print("    === Advanced Data Analysis ===")
    print("    6. analyze_topic_trend      - Unified topic trend analysis (heat/lifecycle/viral/predict)")
    print("    7. analyze_data_insights    - Unified data insights analysis (platform compare/activity/keyword co-occurrence)")
    print("    8. analyze_sentiment        - Sentiment analysis")
    print("    9. find_similar_news        - Similar news search")
    print("    10. generate_summary_report - Daily/weekly summary generation")
    print()
    print("    === Configuration and System Management ===")
    print("    11. get_current_config      - Get current system configuration")
    print("    12. get_system_status       - Get system running status")
    print("    13. trigger_crawl           - Manually trigger crawl task")
    print("=" * 60)
    print()

    # Run server according to transport mode
    if transport == 'stdio':
        mcp.run(transport='stdio')
    elif transport == 'http':
        # HTTP mode (production recommended)
        mcp.run(
            transport='http',
            host=host,
            port=port,
            path='/mcp'  # HTTP endpoint path
        )
    else:
        raise ValueError(f"Unsupported transport mode: {transport}")


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='BaseRadar MCP Server - Crypto/Base news aggregation MCP tool server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  # STDIO mode (for MCP clients like Claude Desktop, Cline, etc.)
  uv run python mcp_server/server.py

  # HTTP mode (suitable for remote access)
  uv run python mcp_server/server.py --transport http --port 3333

MCP Client Configuration Example:
  Settings > MCP Servers > Add Server
  - Name: BaseRadar
  - Type: STDIO
  - Command: [Full path to UV]
  - Arguments: --directory [project path] run python mcp_server/server.py

For detailed configuration tutorials, please refer to: README-MCP.md
        """
    )
    parser.add_argument(
        '--transport',
        choices=['stdio', 'http'],
        default='stdio',
        help='Transport mode: stdio (default) or http (production environment)'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='HTTP mode listen address, default 0.0.0.0'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=3333,
        help='HTTP mode listen port, default 3333'
    )
    parser.add_argument(
        '--project-root',
        help='Project root directory path'
    )

    args = parser.parse_args()

    run_server(
        project_root=args.project_root,
        transport=args.transport,
        host=args.host,
        port=args.port
    )
