# MedVision

### Multimodal Medical Image Analysis with MedGemma

MedVision is a multimodal medical AI prototype that analyzes medical images using Google's **MedGemma 1.5 4B** vision-language model.

The system provides an interactive web interface where users can upload medical images, ask clinical questions, and receive AI-generated visual findings. The project is designed as a research and educational prototype and is **not intended to provide medical diagnoses**.

---

## Overview

Medical images can contain complex visual information that requires specialized interpretation. MedVision explores how multimodal generative AI can assist with understanding medical images by combining:

- Medical vision-language models
- Image validation and preprocessing
- FastAPI REST APIs
- React-based web interfaces
- Persistent analysis history
- Local model inference

The current implementation uses **MedGemma 1.5 4B IT** for multimodal image understanding.

---

## Features

### Medical Image Analysis
- Upload JPEG, PNG, and WEBP images
- Validate image format and file size
- Analyze images using MedGemma
- Ask custom clinical questions
- Generate conservative AI-assisted visual findings

### Web Application
- Modern React dashboard
- Image preview before analysis
- Clinical question input
- Real-time analysis state
- Structured result presentation
- Model and image metadata display
- Clinical safety warnings

### Backend
- FastAPI REST API
- Modular router architecture
- Image validation
- MedGemma inference service
- SQLite-based analysis history
- CORS support for frontend integration
- Health monitoring endpoint

---

## System Architecture

```text
                         MedVision
                            │
                            ▼
                    ┌───────────────┐
                    │ React Frontend│
                    │    Vite       │
                    └───────┬───────┘
                            │
                         HTTP API
                            │
                            ▼
                    ┌───────────────┐
                    │    FastAPI    │
                    │    Backend    │
                    └───────┬───────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
      Image Validation   MedGemma       SQLite
        + Pillow         Inference      History
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                    AI-generated
                       Findings
