# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DietAgent is a Python-based AI agent project focused on dietary analysis and nutritional guidance. The project uses LangChain and various AI models, particularly Qwen models, to analyze food images and provide nutritional insights.

## Architecture

- **Core Package**: `prc/` - Main package directory
- **Configuration**: `pyproject.toml` - Project dependencies and metadata using uv package manager
- **Environment**: Uses `.env` file for API keys and configuration

## Key Dependencies

The project heavily relies on:
- **langchain-qwq**: For connecting to Qwen AI models (particularly QwQ and Qwen3 series)
- **langchain-community**: LangChain community integrations
- **langgraph**: For building AI agent workflows
- **fastapi/uvicorn**: For web API functionality
- **pillow**: For image processing
- **dashscope**: Alibaba Cloud AI model service
- **Various AI providers**: OpenAI, Anthropic, and other model providers

## Core Functionality

Based on the codebase analysis:

1. **Image Analysis**: The main functionality involves analyzing food images using vision models
2. **Nutritional Guidance**: Provides dietary recommendations based on food analysis
3. **Multi-model Support**: Supports various Qwen models including QwQ, Qwen3, and vision models
4. **LangChain Integration**: Uses LangChain framework for AI agent orchestration

## Development Commands

**Package Management** (using uv):
```bash
uv sync                    # Install dependencies
uv add <package>          # Add new dependency
uv remove <package>       # Remove dependency
```

**Running the Application**:
```bash
# The project appears to be primarily used as a library/script
# Check main entry points in prc/ package
python -m prc             # If module has __main__.py
```

**Environment Setup**:
- Copy `.env.example` to `.env` if it exists
- Set required API keys:
  - `DASHSCOPE_API_KEY`: For Alibaba Cloud models
  - `DASHSCOPE_API_BASE`: API endpoint (defaults to Alibaba Cloud)

## Model Configuration

The project supports multiple AI model providers:
- **Primary**: Alibaba Cloud DashScope (Qwen models)
- **Alternative**: Silicon Flow, local deployments, and other OpenAI-compatible endpoints
- **Vision Models**: qwen-vl-max for image analysis

## File Structure

- `prc/__init__.py`: Package initialization (currently empty)
- `prc/base64pic.py`: Image processing and analysis functionality
- `prc/langchain-qwq-*.ipynb`: Jupyter notebooks with usage examples and documentation
- `pyproject.toml`: Project configuration with comprehensive dependency list

## Core Features

**Nutrition AI Agent**: The main application is a LangGraph-based nutrition analysis system that:
- Analyzes food images using Qwen vision models
- Provides nutritional information and health recommendations
- Supports user preferences and dietary restrictions
- Offers both API and web interface access

## Key Files

- `prc/nutrition_agent.py`: Main LangGraph Agent implementation
- `prc/api_server.py`: FastAPI web service with image upload
- `prc/base64pic.py`: Original image processing functionality
- `static/index.html`: Web interface for image upload and analysis
- `run_agent.py`: Main application launcher
- `test_agent.py`: Testing and validation script
- `langgraph.json`: LangGraph Server configuration

## Development Commands

**Run the Nutrition Agent**:
```bash
python run_agent.py          # Start web service on localhost:8000
```

**Testing**:
```bash
python test_agent.py         # Test core Agent functionality
```

**Docker Deployment**:
```bash
docker-compose up -d         # Full service stack with Redis/PostgreSQL
docker build -t nutrition-agent .  # Build container image
```

**LangGraph Server**:
```bash
langgraph dev               # Development server
langgraph deploy            # Production deployment
```

## Development Notes

- The project uses Chinese language extensively in code comments and notebooks
- Focus on food image analysis and nutritional assessment
- Uses base64 encoding for image data processing
- Integrates with multiple AI model providers for flexibility
- Notebook files contain extensive examples of langchain-qwq usage patterns
- LangGraph workflow manages the complete analysis pipeline from image to recommendations