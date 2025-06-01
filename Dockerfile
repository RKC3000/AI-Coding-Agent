FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable (REPLACE with your actual key in production)
ENV OPENAI_API_KEY=your_openai_api_key_here

# Run the agent
CMD ["python", "app.py"]