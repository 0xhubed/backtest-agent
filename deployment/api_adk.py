"""
Simple API for BackTest-Agent info endpoints
Provides health check and agent information for Cloud Run deployment

For full agent functionality, use: adk web
"""
import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the ADK agent
from backtest_agent.agent import root_agent

app = FastAPI(
    title="BackTest-Agent API",
    description="AI-powered trading strategy backtesting via Google ADK. Use 'adk web' for full functionality.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint with service information

    For full agent functionality, run locally with: adk web
    """
    return {
        "service": "BackTest-Agent",
        "version": "1.0.0",
        "description": "AI-powered trading strategy backtesting via Google ADK",
        "agent": root_agent.name,
        "model": root_agent.model,
        "tools_count": len(root_agent.tools),
        "status": "deployed",
        "usage": {
            "local_development": "Run 'adk web' for full agent functionality with interactive UI",
            "api_endpoints": {
                "health": "/health - Health check",
                "tools": "/tools - List all 15 available tools",
                "agent_info": "/agent-info - Detailed agent configuration",
                "docs": "/docs - API documentation"
            }
        }
    }


@app.get("/health")
async def health():
    """
    Health check endpoint for Cloud Run

    Returns service health status.
    """
    return {
        "status": "healthy",
        "agent": root_agent.name,
        "model": root_agent.model
    }


@app.get("/tools")
async def list_tools():
    """
    List all available tools in the agent

    Returns information about the 15 tools registered with the agent.
    """
    tools_info = []

    for tool in root_agent.tools:
        tool_info = {
            "name": tool.__name__,
            "description": tool.__doc__.split('\n')[0] if tool.__doc__ else "No description"
        }
        tools_info.append(tool_info)

    return {
        "agent": root_agent.name,
        "model": root_agent.model,
        "tool_count": len(tools_info),
        "tools": tools_info,
        "categories": {
            "data_tools": [t["name"] for t in tools_info if "fetch" in t["name"] or "get" in t["name"] or "check" in t["name"] or "validate" in t["name"]],
            "backtest_tools": [t["name"] for t in tools_info if "execute" in t["name"] or "compare" in t["name"]],
            "optimization_tools": [t["name"] for t in tools_info if "optimize" in t["name"]]
        }
    }


@app.get("/agent-info")
async def agent_info():
    """
    Get detailed information about the ADK agent configuration

    Returns agent configuration details for deployment verification.
    """
    return {
        "agent_name": root_agent.name,
        "model": root_agent.model,
        "description": root_agent.description,
        "framework": "Google ADK",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "tools_registered": len(root_agent.tools),
        "deployment_platform": "Google Cloud Run",
        "capabilities": [
            "Natural language backtesting queries",
            "5 trading strategies (SMA, RSI, Bollinger Bands, MACD, Buy & Hold)",
            "Parameter optimization via grid search",
            "Multi-symbol parallel data fetching",
            "Comprehensive risk metrics calculation"
        ],
        "usage": "Run 'adk web' locally for full interactive agent functionality"
    }


if __name__ == "__main__":
    import uvicorn

    # Get port from environment (Cloud Run uses PORT env var)
    port = int(os.environ.get("PORT", 8080))

    # Run the FastAPI app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
