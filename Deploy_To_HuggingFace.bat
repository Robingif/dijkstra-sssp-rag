@echo off
title Deploy Dijkstra SSSP RAG to Hugging Face Spaces
echo ==============================================================
echo    Dijkstra Grounded RAG Platform - Hugging Face Deployment
echo ==============================================================
echo.
echo Make sure you have your Hugging Face write token ready from:
echo https://huggingface.co/settings/tokens
echo.
python deploy_hf.py
echo.
pause
