#!/bin/bash
set -e

# Read tokens from .env file
if [ -f .env ]; then
  GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" .env | cut -d '=' -f 2- | tr -d '\r')
  HUGGING_FACE_TOKEN=$(grep "^HUGGING_FACE_TOKEN=" .env | cut -d '=' -f 2- | tr -d '\r')
  SENDER_EMAIL=$(grep "^SENDER_EMAIL=" .env | cut -d '=' -f 2- | tr -d '\r')
else
  echo ".env file not found"
  exit 1
fi

# URLs
GH_REPO="https://cwbdayi:${GITHUB_TOKEN}@github.com/cwbdayi638/disaster_dashboard.git"
HF_GRADIO="https://cwbdayi:${HUGGING_FACE_TOKEN}@huggingface.co/spaces/cwbdayi/disaster_dashboard"
HF_FASTAPI="https://cwbdayi:${HUGGING_FACE_TOKEN}@huggingface.co/spaces/cwbdayi/disaster_fastapi"

echo "Deploying to GitHub Repo..."
git config --global user.email "${SENDER_EMAIL}"
git config --global user.name "AI Assistant"
git add .
git commit -m "Initial commit for Disaster Dashboard Architecture" || true
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "$GH_REPO"
git push -u origin main -f

echo "Deploying to Hugging Face Gradio Space..."
cd backend/gradio_space
rm -rf .git
git init
git add .
git commit -m "Deploy Gradio App" || true
git branch -M main
git remote add origin "$HF_GRADIO"
git push -u origin main -f
cd ../..

echo "Deploying to Hugging Face FastAPI Space..."
cd backend/fastapi_space
rm -rf .git
git init
git add .
git commit -m "Deploy FastAPI App" || true
git branch -M main
git remote add origin "$HF_FASTAPI"
git push -u origin main -f
cd ../..

echo "Deployment Complete!"
