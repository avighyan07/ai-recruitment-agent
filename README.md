# AI Recruitment Agent

An AI-powered recruitment system that automates resume screening, candidate matching, analysis, and ranking against a given job description.

The system combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), semantic embeddings, vector search, and LangGraph-based workflows to streamline the recruitment process.

The application is deployed on AWS EC2 using Docker.

## Overview

Traditional resume screening requires recruiters to manually review large numbers of resumes and compare them against job requirements.

The AI Recruitment Agent automates this process by:

- Accepting multiple candidate resumes
- Extracting relevant candidate information
- Comparing resumes against a Job Description
- Performing semantic similarity-based candidate matching
- Identifying relevant skills and experience
- Generating candidate analysis using an LLM
- Ranking candidates based on their suitability
- Providing an interactive web interface for recruitment analysis

## Key Features

### Multi-Resume Upload

Upload multiple resumes simultaneously for automated processing and candidate evaluation.

### AI-Powered Resume Analysis

Extracts and analyzes candidate information including:

- Skills
- Experience
- Education
- Projects
- Relevant qualifications

### Semantic Candidate Matching

Uses Sentence Transformer embeddings and ChromaDB to perform semantic matching between candidate resumes and job requirements.

### Candidate Ranking

Candidates are ranked based on their relevance to the provided job description.

### LLM-Based Analysis

Uses LLMs to provide deeper candidate analysis and context-aware recruitment insights.

### LangGraph Workflow

Implements a structured recruitment workflow using LangGraph to manage different stages of candidate processing and evaluation.

### REST API

Built with FastAPI to expose recruitment functionality through RESTful endpoints.

### Dockerized Deployment

The complete application is containerized using Docker for consistent deployment.

### AWS Deployment

Deployed on an AWS EC2 instance and made publicly accessible.

## System Architecture

         +----------------------+
                    |      Recruiter       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Web Interface     |
                    |    HTML/CSS/JS       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |       FastAPI        |
                    |      REST APIs       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Resume Parser     |
                    |  Resume Processing   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Sentence Transformers|
                    |   Text Embeddings   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |       ChromaDB       |
                    |     Vector Search    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      LangGraph       |
                    | Recruitment Workflow |
                    +----------+-----------+
                               |
                    +----------+-----------+
                    |                      |
                    v                      v
           +----------------+     +----------------+
           |    Semantic    |     |  LLM Analysis  |
           |    Matching    |     |                |
           +-------+--------+     +-------+--------+
                   |                      |
                   +----------+-----------+
                              |
                              v
                    +----------------------+
                    | Candidate Ranking &  |
                    | Recruitment Results  |
                    +----------------------+
