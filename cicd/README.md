# Module 4: CI/CD Agent

This module implements a CI/CD agent that automates GitHub Actions workflows and AWS SAM deployments for the Birthday Greetings kata.

## Overview

The CI/CD agent enforces deployment pipeline best practices by automating:
- GitHub Actions workflow generation
- AWS SAM build and deploy steps
- Environment-specific configuration management

## Usage

The agent is configured via `.kiro/agents/` and is invoked as part of the standard module workflow.

## Pipeline Stages

1. **Build** – Install dependencies and run linters
2. **Test** – Execute unit and integration tests
3. **Deploy** – SAM package and deploy to target environment
