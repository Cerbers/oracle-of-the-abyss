# Stage 1: Build the React frontend
FROM node:20 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build  # Creates dist/ in this stage

# Stage 2: Python/FastAPI backend
FROM python:3.12-slim
WORKDIR /app

# Install Python deps (adjust if your requirements.txt is elsewhere)
# Assuming you have requirements.txt in oracle/ — if not, create one there
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt uvicorn[standard]

# Copy backend code
COPY oracle/ ./oracle

# Copy built frontend dist from previous stage
COPY --from=frontend-build /app/frontend/dist ./dist

# Expose port
EXPOSE 8000

# Run the API (oracle.api because api.py is in oracle/)
CMD exec uvicorn oracle.api:app --host 0.0.0.0 --port ${PORT:-8000}