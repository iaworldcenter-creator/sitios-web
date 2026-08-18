---
name: gemini-api-cli
description: >-
  Provides installation instructions and usage patterns for Google's official Gemini API CLI,
  allowing direct calls via the free Gemini API in the terminal or scripting environments.
---

# Gemini API CLI Skill

This skill provides direct CLI integration to query Gemini models and manage custom agent lifecycles via terminal.

## Setup & Credentials
To use this CLI, you must ensure the `GEMINI_API_KEY` is present in your environment variables:
*   Windows PowerShell: `$env:GEMINI_API_KEY="AIzaSy..."`
*   Windows CMD: `set GEMINI_API_KEY=AIzaSy...`

## Basic Usage
*   **Run Prompt**: `gemini-api run "your prompt"`
*   **Specify Model**: `gemini-api run "explain relativity" --model gemini-2.5-pro`
*   **Initiate scaffold for custom agent**: `gemini-api agents init <agent_name>`
*   **Test custom agent**: `gemini-api agents test --prompt "hello"`
*   **Deploy custom agent**: `gemini-api agents create`
