# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Create non-root user and directories
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/staticfiles /app/media /app/logs && \
    chown -R appuser:appuser /app

# Create default profile image
RUN python3 -c "from PIL import Image, ImageDraw; img = Image.new('RGB', (300, 300), color='#6c757d'); draw = ImageDraw.Draw(img); draw.ellipse([100, 70, 200, 170], fill='white'); draw.ellipse([75, 160, 225, 280], fill='white'); img.save('/app/media/default.jpg', 'JPEG', quality=95)" && \
    chown appuser:appuser /app/media/default.jpg

# Switch to non-root user
USER appuser

# Collect static files as the app user
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "django_project.wsgi:application"]
