$ErrorActionPreference = "Stop"

# Read tokens from .env file
$envVars = @{}
Get-Content .env -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_ -match "^([^#\s=]+)=(.*)$") {
        $envVars[$matches[1]] = $matches[2]
    }
}

$gh_token = $envVars["GITHUB_TOKEN"]
$hf_token = $envVars["HUGGING_FACE_TOKEN"]

$gh_repo = "https://cwbdayi:$gh_token@github.com/cwbdayi638/disaster_dashboard.git"
$hf_gradio = "https://cwbdayi:$hf_token@huggingface.co/spaces/cwbdayi638/disaster_dashboard"
$hf_fastapi = "https://cwbdayi:$hf_token@huggingface.co/spaces/cwbdayi/disaster_fastapi"

Write-Host "Deploying to GitHub Repo..."
git config --global user.email "cwbdayi@gmail.com"
git config --global user.name "AI Assistant"
git add .
git commit -m "Initial commit for Disaster Dashboard Architecture"
git branch -M main
git remote remove origin 2>$null
git remote add origin $gh_repo
git push -u origin main -f

Write-Host "Deploying to Hugging Face Gradio Space..."
cd backend\gradio_space
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
git init
git add .
git commit -m "Deploy Gradio App"
git branch -M main
git remote add origin $hf_gradio
git push -u origin main -f
cd ..\..

Write-Host "Deploying to Hugging Face FastAPI Space..."
cd backend\fastapi_space
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
git init
git add .
git commit -m "Deploy FastAPI App"
git branch -M main
git remote add origin $hf_fastapi
git push -u origin main -f
cd ..\..

Write-Host "Deployment Complete!"
