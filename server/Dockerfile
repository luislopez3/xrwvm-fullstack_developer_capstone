# Step 1: Add a base image
FROM python:3.12.0-slim-bookworm

# Step 2: Set environment variables to prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy and install dependencies
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application files
COPY . /app/

# Step 6: Expose the application port
EXPOSE 8000

# Step 7: Grant execute permissions to the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Step 8: Set entrypoint to execute the entrypoint script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Step 9: Start the Django application using Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
