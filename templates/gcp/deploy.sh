#!/bin/bash

# GCP Deployment Script
# This script handles deployment to Google Cloud Platform

set -e

# Configuration
PROJECT_ID=""
REGION="us-central1"
APP_NAME=""
IMAGE_TAG=""
SERVICE_ACCOUNT=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Load environment variables
load_environment() {
    if [ -f ".env" ]; then
        export $(cat .env | grep -v '#' | xargs)
        print_info "Loaded environment variables from .env"
    else
        print_warning "No .env file found"
    fi
}

# Set default values
set_defaults() {
    PROJECT_ID=${GCP_PROJECT_ID:-$PROJECT_ID}
    APP_NAME=${APP_NAME:-$(basename $(pwd))}
    IMAGE_TAG=${IMAGE_TAG:-$(git rev-parse --short HEAD)}
    REGION=${GCP_REGION:-$REGION}
    SERVICE_ACCOUNT=${GCP_SERVICE_ACCOUNT:-$SERVICE_ACCOUNT}
}

# Validate required variables
validate_config() {
    if [ -z "$PROJECT_ID" ]; then
        print_error "PROJECT_ID is not set"
        exit 1
    fi
    
    if [ -z "$APP_NAME" ]; then
        print_error "APP_NAME is not set"
        exit 1
    fi
    
    print_info "Configuration:"
    print_info "  Project ID: $PROJECT_ID"
    print_info "  App Name: $APP_NAME"
    print_info "  Region: $REGION"
    print_info "  Image Tag: $IMAGE_TAG"
}

# Check if gcloud is authenticated
check_auth() {
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "No active gcloud authentication found"
        print_info "Run: gcloud auth login"
        exit 1
    fi
    
    print_info "gcloud authentication verified"
}

# Set the active project
set_project() {
    gcloud config set project $PROJECT_ID
    print_info "Set active project to: $PROJECT_ID"
}

# Enable required APIs
enable_apis() {
    print_info "Enabling required APIs..."
    
    gcloud services enable \
        cloudbuild.googleapis.com \
        run.googleapis.com \
        containerregistry.googleapis.com \
        secretmanager.googleapis.com \
        sql-component.googleapis.com \
        --project=$PROJECT_ID
    
    print_info "APIs enabled successfully"
}

# Build and push Docker image
build_image() {
    print_info "Building Docker image..."
    
    # Build the image
    docker build -t gcr.io/$PROJECT_ID/$APP_NAME:$IMAGE_TAG .
    docker tag gcr.io/$PROJECT_ID/$APP_NAME:$IMAGE_TAG gcr.io/$PROJECT_ID/$APP_NAME:latest
    
    # Configure Docker to push to GCR
    gcloud auth configure-docker --quiet
    
    # Push the image
    docker push gcr.io/$PROJECT_ID/$APP_NAME:$IMAGE_TAG
    docker push gcr.io/$PROJECT_ID/$APP_NAME:latest
    
    print_info "Docker image built and pushed successfully"
}

# Create secrets in Secret Manager
create_secrets() {
    print_info "Creating secrets in Secret Manager..."
    
    # Database URL
    if [ ! -z "$DATABASE_URL" ]; then
        echo -n "$DATABASE_URL" | gcloud secrets create database-url --data-file=- --project=$PROJECT_ID 2>/dev/null || \
        echo -n "$DATABASE_URL" | gcloud secrets versions add database-url --data-file=- --project=$PROJECT_ID
        print_info "Created/updated database-url secret"
    fi
    
    # Redis URL
    if [ ! -z "$REDIS_URL" ]; then
        echo -n "$REDIS_URL" | gcloud secrets create redis-url --data-file=- --project=$PROJECT_ID 2>/dev/null || \
        echo -n "$REDIS_URL" | gcloud secrets versions add redis-url --data-file=- --project=$PROJECT_ID
        print_info "Created/updated redis-url secret"
    fi
    
    # Secret key
    if [ ! -z "$SECRET_KEY" ]; then
        echo -n "$SECRET_KEY" | gcloud secrets create app-secret-key --data-file=- --project=$PROJECT_ID 2>/dev/null || \
        echo -n "$SECRET_KEY" | gcloud secrets versions add app-secret-key --data-file=- --project=$PROJECT_ID
        print_info "Created/updated app-secret-key secret"
    fi
}

# Deploy to Cloud Run
deploy_to_cloud_run() {
    print_info "Deploying to Cloud Run..."
    
    gcloud run deploy $APP_NAME \
        --image gcr.io/$PROJECT_ID/$APP_NAME:$IMAGE_TAG \
        --region $REGION \
        --platform managed \
        --allow-unauthenticated \
        --port 8080 \
        --cpu 1 \
        --memory 512Mi \
        --min-instances 0 \
        --max-instances 10 \
        --timeout 300s \
        --set-env-vars "NODE_ENV=production" \
        --set-secrets "DATABASE_URL=database-url:latest,REDIS_URL=redis-url:latest,SECRET_KEY=app-secret-key:latest" \
        --project=$PROJECT_ID
    
    print_info "Deployment completed successfully"
}

# Get service URL
get_service_url() {
    SERVICE_URL=$(gcloud run services describe $APP_NAME --region=$REGION --format="value(status.url)" --project=$PROJECT_ID)
    print_info "Service URL: $SERVICE_URL"
}

# Test the deployment
test_deployment() {
    print_info "Testing deployment..."
    
    # Wait for service to be ready
    sleep 10
    
    # Test health endpoint
    if curl -f -s "${SERVICE_URL}/health" > /dev/null; then
        print_info "Health check passed ✅"
    else
        print_warning "Health check failed ❌"
    fi
}

# Main deployment function
deploy() {
    print_info "Starting deployment process..."
    
    load_environment
    set_defaults
    validate_config
    check_auth
    set_project
    enable_apis
    build_image
    create_secrets
    deploy_to_cloud_run
    get_service_url
    test_deployment
    
    print_info "🚀 Deployment completed successfully!"
    print_info "🌐 Your application is available at: $SERVICE_URL"
}

# Handle command line arguments
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "build")
        load_environment
        set_defaults
        validate_config
        check_auth
        set_project
        build_image
        ;;
    "secrets")
        load_environment
        set_defaults
        validate_config
        check_auth
        set_project
        create_secrets
        ;;
    "test")
        load_environment
        set_defaults
        validate_config
        get_service_url
        test_deployment
        ;;
    *)
        echo "Usage: $0 {deploy|build|secrets|test}"
        echo "  deploy  - Full deployment process"
        echo "  build   - Build and push Docker image only"
        echo "  secrets - Create/update secrets only"
        echo "  test    - Test the deployed service"
        exit 1
        ;;
esac