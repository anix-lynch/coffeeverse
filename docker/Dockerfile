# Production-ready Docker image for Azure ETL Pipeline
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    COFFEEVERSE_HOME=/opt/coffeeverse

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create coffeeverse user
RUN useradd -ms /bin/bash -d ${COFFEEVERSE_HOME} coffeeverse

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Create necessary directories
RUN mkdir -p ${COFFEEVERSE_HOME}/dbt_project \
    ${COFFEEVERSE_HOME}/data_factory \
    ${COFFEEVERSE_HOME}/deploy \
    ${COFFEEVERSE_HOME}/azure_function \
    ${COFFEEVERSE_HOME}/logs

# Copy application code
COPY --chown=coffeeverse:coffeeverse streamlit_app.py ${COFFEEVERSE_HOME}/
COPY --chown=coffeeverse:coffeeverse azure_function/ ${COFFEEVERSE_HOME}/azure_function/
COPY --chown=coffeeverse:coffeeverse dbt_project/ ${COFFEEVERSE_HOME}/dbt_project/
COPY --chown=coffeeverse:coffeeverse data_factory/ ${COFFEEVERSE_HOME}/data_factory/
COPY --chown=coffeeverse:coffeeverse cosmosdb_schema.json ${COFFEEVERSE_HOME}/
COPY --chown=coffeeverse:coffeeverse .streamlit/ ${COFFEEVERSE_HOME}/.streamlit/

# Copy docker entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Change ownership
RUN chown -R coffeeverse:coffeeverse ${COFFEEVERSE_HOME}

# Switch to coffeeverse user
USER coffeeverse

# Set working directory
WORKDIR ${COFFEEVERSE_HOME}

# Expose ports
EXPOSE 8501

# Default entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["streamlit", "run", "streamlit_app.py"]

