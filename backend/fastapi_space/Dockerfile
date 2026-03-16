FROM python:3.9

# Setup standard non-root user for Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY --chown=user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY --chown=user . .

# Command to run the Fastapi application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
