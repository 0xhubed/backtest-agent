"""
FastAPI wrapper for BackTestPilot ADK Agent
Simplified version for Cloud Run deployment

This provides a REST API interface to the ADK agent for deployment evidence.
"""
import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the ADK agent
from backtest_agent.agent import root_agent

app = FastAPI(
    title="BackTestPilot API",
    description="AI-powered trading strategy backtesting via Google ADK",
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


class BacktestRequest(BaseModel):
    """Request model for backtesting queries"""
    query: str
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Backtest SMA(20,50) on BTC from 2020 to 2021",
                "session_id": "user-123"
            }
        }


class BacktestResponse(BaseModel):
    """Response model for backtesting queries"""
    response: str
    session_id: str
    agent_name: str
    model: str


@app.get("/")
async def root():
    """
    Root endpoint - service information

    Returns basic information about the BackTestPilot API service.
    """
    return {
        "status": "healthy",
        "service": "BackTestPilot",
        "version": "1.0.0",
        "description": "AI-powered trading strategy backtesting",
        "agent": root_agent.name,
        "model": root_agent.model,
        "tools_count": len(root_agent.tools),
        "endpoints": {
            "health": "/health",
            "tools": "/tools",
            "backtest": "/backtest",
            "docs": "/docs"
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


@app.post("/backtest", response_model=BacktestResponse)
async def run_backtest(request: BacktestRequest):
    """
    Run a backtesting query via the ADK agent

    Note: This is a simplified endpoint for deployment demonstration.
    For full agent interaction with streaming responses and session management,
    use the ADK CLI (`adk web`) or Agent Engine deployment.

    Example request:
    ```json
    {
        "query": "What cryptocurrencies are available?",
        "session_id": "user-123"
    }
    ```
    """
    try:
        # For deployment evidence, we return agent info
        # Full agent execution would require ADK session integration

        return BacktestResponse(
            response=(
                f"BackTestPilot agent received your query: '{request.query}'\n\n"
                "This API demonstrates deployment to Cloud Run. "
                "For full interactive agent capabilities with streaming responses "
                "and session memory, please use:\n"
                "- Agent Engine: `adk run backtest_agent --project-id PROJECT_ID`\n"
                "- Local ADK Web UI: `adk web` at http://localhost:8000\n\n"
                f"The agent has {len(root_agent.tools)} tools available for backtesting."
            ),
            session_id=request.session_id or "demo-session",
            agent_name=root_agent.name,
            model=root_agent.model
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


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
        ]
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
