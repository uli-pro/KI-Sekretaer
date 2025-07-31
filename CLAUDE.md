# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KI-Sekretaer is the first module of an ADHS (ADHD) assistant app, developed as a CS50 final project. This AI-powered secretary helps adults with ADHD manage tasks and improve productivity through intelligent task processing and ADHD-specific user experience design.

## Current Project Status

This repository is in the **initial planning phase** with comprehensive background research completed but no code implementation yet. The project follows a phased development approach optimized for CS50 requirements.

## Planned Technology Stack

Based on the development plan in `hintergrund/claude-plan-ki-sekretaer.md`:

- **Backend**: Flask + SQLite (CS50-compatible)
- **Frontend**: Vanilla HTML/CSS/JavaScript (no complex frameworks initially)
- **AI Integration**: OpenAI API for natural language processing
- **Database**: SQLite with ADHD-optimized schema
- **Deployment**: Local development first, Azure migration planned post-CS50

## Core Functionality (Planned)

1. **Unstructured Input Processing**: Natural language task input
2. **LLM-Based Task Analysis**: Intelligent extraction of task details, deadlines, energy requirements
3. **ADHD-Specific Features**: Energy-level tracking, time estimation, forgiveness mechanisms
4. **Structured Task Management**: SQLite database with ADHD-optimized fields

## Database Schema (Planned)

Key tables will include:
- `users`: Basic authentication
- `tasks`: Core task data with ADHD-specific fields (energy_required, estimated_duration, etc.)
- `task_dependencies`: Task relationship management

## Development Commands

When code is implemented:
- **Run Flask app**: `python app.py` or `flask run`
- **Database operations**: Custom Flask CLI commands for schema management
- **Testing**: Standard Python testing framework (pytest planned)

## CS50 Requirements Compliance

The project must deliver:
- Functional web application with user authentication
- LLM-based natural language processing
- Relational database with SQLite
- JavaScript frontend interactivity
- 3-minute demonstration video
- Comprehensive README documentation

## ADHD-Specific Design Principles

This project specifically targets ADHD users with:
- **Emotional regulation**: Non-judgmental interface design
- **Executive function support**: Task breakdown and energy matching
- **Forgiveness mechanisms**: Handling missed tasks without shame
- **Interest-driven prioritization**: Beyond standard importance/urgency matrices

## Market Context

The project addresses a gap in existing ADHD productivity tools by combining:
- Intelligent task processing (like Goblin Tools)
- ADHD-specific UX considerations
- Emotional regulation features
- German market focus with potential DiGA pathway

## Development Timeline

- **Phase 1 (Weeks 1-6)**: CS50 MVP with core functionality
- **Phase 2 (Post-CS50)**: Azure migration and advanced ADHD features
- **Phase 3**: Preparation for broader ADHS app ecosystem

## Key Documentation

- `hintergrund/ADHS-Tool_ Idee, Markt, Umsetzung.md`: Comprehensive market analysis
- `hintergrund/claude-plan-ki-sekretaer.md`: Detailed development roadmap
- `hintergrund/requirements-final-project.md`: CS50 submission requirements

## Next Steps for Development

1. Set up Flask development environment
2. Implement basic user authentication
3. Create SQLite database schema
4. Integrate OpenAI API for task processing
5. Build minimal viable frontend

When implementing, prioritize CS50 demonstration requirements while maintaining the ADHD-specific focus that differentiates this project from generic task management apps.