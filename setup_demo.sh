#!/bin/bash

# Aider Pentesting Agent Demo Setup Script
# This script demonstrates the one-click setup capability

set -e

echo "🔒 Aider Pentesting Agent Demo Setup"
echo "===================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data reports audit_logs config

# Create default configuration
echo "⚙️  Creating default configuration..."
cat > config/pentest_config.json << EOF
{
  "llm_providers": [
    {
      "name": "openai",
      "model": "gpt-4",
      "enabled": true
    },
    {
      "name": "local",
      "base_url": "http://localhost:11434",
      "model": "llama2",
      "enabled": false
    }
  ],
  "security_config": {
    "enforce_zero_trust": true,
    "require_consent": true,
    "audit_log_enabled": true,
    "allowed_targets": [
      "localhost",
      "127.0.0.1",
      "http://localhost:3000",
      "192.168.0.0/16",
      "10.0.0.0/8",
      "172.16.0.0/12"
    ]
  },
  "tool_config": {
    "auto_install": true,
    "sandbox_mode": true,
    "tool_timeout": 300
  },
  "report_formats": ["json", "html", "markdown"],
  "report_api_enabled": true,
  "report_api_port": 8080
}
EOF

# Build and start containers
echo "🚀 Building and starting containers..."
docker-compose -f docker-compose.pentest.yml up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose -f docker-compose.pentest.yml ps

echo ""
echo "✅ Demo setup complete!"
echo ""
echo "🎯 Available demo targets:"
echo "  - OWASP Juice Shop: http://localhost:3000"
echo ""
echo "🔧 Pentesting Agent Commands:"
echo "  # Run demo campaign"
echo "  docker exec -it aider-pentesting-agent python -m aider --pentest-demo"
echo ""
echo "  # Target specific assessment"
echo "  docker exec -it aider-pentesting-agent python -m aider --pentest --pentest-target http://localhost:3000 --pentest-type web"
echo ""
echo "  # Interactive mode"
echo "  docker exec -it aider-pentesting-agent python -m aider --pentest"
echo ""
echo "📊 Reporting API: http://localhost:8080/api/status"
echo "📁 Reports will be saved to: ./reports/"
echo "🔍 Audit logs will be saved to: ./audit_logs/"
echo ""
echo "🛑 To stop the demo:"
echo "  docker-compose -f docker-compose.pentest.yml down"