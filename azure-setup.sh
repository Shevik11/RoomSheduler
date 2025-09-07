#!/bin/bash

# 🚀 Script for automatic deployment of RoomScheduler on Azure
# Usage: ./azure-setup.sh

set -e

echo "🚀 Starting deployment of RoomScheduler on Azure..."

# Configuration variables - UK South region
RESOURCE_GROUP="rg-roomScheduler-uksouth"
LOCATION="uksouth"
DB_NAME="roomscheduler-db-uk"
DB_ADMIN="dbadmin"
DB_PASSWORD="RoomScheduler2024!"
REGISTRY_NAME="roomschedulerregistryuk"
CONTAINER_ENV="roomscheduler-env-uk"
BACKEND_APP="roomscheduler-backend-uk"
FRONTEND_APP="roomscheduler-frontend-uk"

echo "📋 Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION (UK South)"
echo "  Database: $DB_NAME"
echo "  Registry: $REGISTRY_NAME"

# Check if logged in to Azure
echo "🔐 Checking Azure login..."
if ! az account show &> /dev/null; then
    echo "Please login to Azure first:"
    az login
fi

echo "✅ Azure CLI configured"

# Create PostgreSQL Database
echo "🗄️ Creating PostgreSQL server in UK South..."
az postgres flexible-server create \
    --resource-group $RESOURCE_GROUP \
    --name $DB_NAME \
    --location $LOCATION \
    --admin-user $DB_ADMIN \
    --admin-password $DB_PASSWORD \
    --sku-name Standard_B1ms \
    --tier Burstable \
    --public-access 0.0.0.0 \
    --storage-size 32 \
    --version 14

# Create database
echo "📊 Creating database..."
az postgres flexible-server db create \
    --resource-group $RESOURCE_GROUP \
    --server-name $DB_NAME \
    --database-name roomscheduler

# Create Container Registry
echo "🐳 Creating Container Registry in UK South..."
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $REGISTRY_NAME \
    --sku Basic \
    --location $LOCATION

# Enable admin user
az acr update --name $REGISTRY_NAME --admin-enabled true

# Get ACR credentials
echo "🔑 Getting ACR credentials..."
ACR_SERVER=$(az acr show --name $REGISTRY_NAME --query loginServer --output tsv)
ACR_USERNAME=$(az acr credential show --name $REGISTRY_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $REGISTRY_NAME --query passwords[0].value --output tsv)

echo "📦 ACR Details:"
echo "  Server: $ACR_SERVER"
echo "  Username: $ACR_USERNAME"

# Build and push backend image
echo "🔨 Building backend image..."
docker build -t $ACR_SERVER/roomscheduler-backend:latest ./backend
docker login $ACR_SERVER --username $ACR_USERNAME --password $ACR_PASSWORD
docker push $ACR_SERVER/roomscheduler-backend:latest

# Build and push frontend image  
echo "🔨 Building frontend image..."
docker build -t $ACR_SERVER/roomscheduler-frontend:latest ./frontend/shedule
docker push $ACR_SERVER/roomscheduler-frontend:latest

# Create Container Apps Environment
echo "🌐 Creating Container Apps Environment in UK South..."
az containerapp env create \
    --name $CONTAINER_ENV \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION

# Get database connection string
DB_CONNECTION_STRING="postgresql://$DB_ADMIN:$DB_PASSWORD@$DB_NAME.postgres.database.azure.com:5432/roomscheduler?sslmode=require"

# Create backend container app
echo "🚀 Creating backend container app..."
az containerapp create \
    --name $BACKEND_APP \
    --resource-group $RESOURCE_GROUP \
    --environment $CONTAINER_ENV \
    --image $ACR_SERVER/roomscheduler-backend:latest \
    --target-port 8000 \
    --ingress external \
    --registry-server $ACR_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --secrets database-url="$DB_CONNECTION_STRING" \
    --env-vars DATABASE_URL=secretref:database-url ENVIRONMENT=production DEBUG=false \
    --cpu 0.5 --memory 1Gi \
    --min-replicas 1 --max-replicas 3

# Get backend URL
BACKEND_URL=$(az containerapp show --name $BACKEND_APP --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)

# Create frontend container app
echo "🎨 Creating frontend container app..."
az containerapp create \
    --name $FRONTEND_APP \
    --resource-group $RESOURCE_GROUP \
    --environment $CONTAINER_ENV \
    --image $ACR_SERVER/roomscheduler-frontend:latest \
    --target-port 80 \
    --ingress external \
    --registry-server $ACR_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --env-vars VITE_API_BASE_URL=https://$BACKEND_URL \
    --cpu 0.25 --memory 0.5Gi \
    --min-replicas 1 --max-replicas 2

# Get frontend URL
FRONTEND_URL=$(az containerapp show --name $FRONTEND_APP --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Deployment Details:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION (UK South)"
echo "  Database: $DB_NAME.postgres.database.azure.com"
echo "  Container Registry: $ACR_SERVER"
echo ""
echo "🌐 Application URLs:"
echo "  Backend API: https://$BACKEND_URL"
echo "  Frontend App: https://$FRONTEND_URL"
echo ""
echo "✅ Your RoomScheduler is now running in UK South!"
