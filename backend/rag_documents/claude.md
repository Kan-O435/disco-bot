# CLAUDE.md

# AI Agent Playground

## Project Overview

AI Agent Playground is a long-term learning project for building a personal AI Agent.

The primary goal is **not** to build a Discord Bot, but to create an experimental environment where new AI technologies can be continuously integrated and evaluated.

This repository will gradually evolve from a simple Discord Bot into a production-like AI Agent platform.

---

# Goals

This project aims to learn and experiment with:

- AI Agent Architecture
- LLM Integration
- Tool Calling
- Memory
- RAG
- MCP Server
- Backend Development
- Infrastructure
- Cloud Deployment

The project should always prioritize **learning architecture** over simply implementing features.

---

# Current Architecture

```
Discord
    │
Discord Bot (Python)
```

Current Status

- Discord Application created
- Discord Bot created
- Bot invited to Discord Server
- Docker environment created
- Docker Compose configured
- Bot successfully runs inside Docker

---

# Future Architecture

```
Discord
    │
Discord Bot
    │
FastAPI
    │
AI Agent
    │
Tool Calling
    │
PostgreSQL
Redis
Vector DB
    │
LLM
```

Eventually the project will include

- MCP Client
- MCP Server
- RAG
- Memory
- Scheduler
- AWS Infrastructure

---

# Tech Stack

## Current

- Python
- discord.py
- Docker
- Docker Compose

## Future

Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis

AI

- OpenAI
- Anthropic
- Gemini

Infrastructure

- Docker
- AWS EC2
- GitHub Actions
- Terraform

Vector Database

- pgvector

---

# Development Policy

This project is developed incrementally.

Each phase should remain simple and independently testable.

Avoid introducing unnecessary abstractions until they are required.

---

# Coding Guidelines

- Keep code readable.
- Prefer explicit code over clever code.
- Keep modules small.
- Separate Discord-specific logic from AI logic.
- Future AI logic should never depend directly on Discord.

---

# Directory Structure

Current

```
bot/
backend/
compose.yaml
README.md
```

Target

```
bot/
backend/
infra/
docker/
docs/
scripts/
compose.yaml
```

---

# Roadmap

## Phase 1

Discord Bot

- Bot Online
- Docker
- /ping
- /chat
- /help

---

## Phase 2

AI Chat

- OpenAI API
- Conversation
- Message History

---

## Phase 3

Backend

- FastAPI
- REST API
- Docker Compose

---

## Phase 4

Database

- PostgreSQL
- SQLAlchemy
- Alembic

---

## Phase 5

AI Agent

- Tool Calling
- Task Tool
- Reminder Tool
- News Tool

---

## Phase 6

Scheduler

- Redis
- APScheduler
- Background Jobs

---

## Phase 7

Memory

- Embeddings
- pgvector
- Long-term Memory

---

## Phase 8

RAG

- Markdown
- PDF
- Obsidian
- Notion

---

## Phase 9

MCP

- MCP Client
- Filesystem MCP
- GitHub MCP
- Browser MCP
- Custom MCP Server

---

## Phase 10

Infrastructure

- Linux
- AWS EC2
- Nginx
- HTTPS
- GitHub Actions
- CI/CD
- Terraform

---

# Design Philosophy

Discord is **only the User Interface**.

FastAPI will become the **Brain**.

The AI Agent should remain independent from Discord.

Every external feature should be implemented as a Tool.

This architecture allows future migration to

- Slack
- LINE
- Web UI
- CLI

without changing the AI logic.

---

# Learning Objectives

This project should help understand

- Modern AI Agent Architecture
- Production Backend Design
- Docker-based Development
- Infrastructure
- Cloud Deployment
- MCP
- LLM Engineering

rather than simply building a working application.