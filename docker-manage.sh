#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env file not found!"
        if [ -f .env.example ]; then
            print_message "Creating .env file from .env.example..."
            cp .env.example .env
            print_message "Please update the .env file with your configuration."
        else
            print_error ".env.example file not found!"
            exit 1
        fi
    fi
}

# Function to start services
start_services() {
    local env=$1
    print_message "Starting services in $env environment..."
    docker compose -f docker-compose.$env.yml up -d
}

# Function to stop services
stop_services() {
    local env=$1
    print_message "Stopping services in $env environment..."
    docker compose -f docker-compose.$env.yml down
}

# Function to rebuild services
rebuild_services() {
    local env=$1
    print_message "Rebuilding services in $env environment..."
    docker compose -f docker-compose.$env.yml up -d --build
}

# Function to view logs
view_logs() {
    local env=$1
    local service=$2
    if [ -z "$service" ]; then
        docker compose -f docker-compose.$env.yml logs -f
    else
        docker compose -f docker-compose.$env.yml logs -f $service
    fi
}

# Function to execute command in a service
exec_service() {
    local env=$1
    local service=$2
    shift 2
    docker compose -f docker-compose.$env.yml exec $service "$@"
}

# Function to delete volumes
delete_volumes() {
    local env=$1
    print_warning "This will delete ALL volumes for the $env environment!"
    read -p "Are you sure you want to continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_message "Stopping services..."
        docker compose -f docker-compose.$env.yml down
        print_message "Deleting volumes..."
        docker compose -f docker-compose.$env.yml down -v
        print_message "Volumes deleted successfully."
    else
        print_message "Operation cancelled."
    fi
}

# Function to show help
show_help() {
    echo "Usage: ./docker-manage.sh [command] [environment] [service]"
    echo ""
    echo "Commands:"
    echo "  start     - Start services"
    echo "  stop      - Stop services"
    echo "  restart   - Restart services"
    echo "  rebuild   - Rebuild and start services"
    echo "  logs      - View logs (all or specific service)"
    echo "  exec      - Execute command in a service"
    echo "  delete-volumes - Delete all volumes for the environment"
    echo "  help      - Show this help message"
    echo ""
    echo "Environments:"
    echo "  dev       - Development environment"
    echo "  prod      - Production environment"
    echo ""
    echo "Examples:"
    echo "  ./docker-manage.sh start dev"
    echo "  ./docker-manage.sh logs dev backend"
    echo "  ./docker-manage.sh exec dev backend python manage.py migrate"
    echo "  ./docker-manage.sh delete-volumes dev"
}

# Main script logic
case "$1" in
    "start")
        check_env_file
        start_services "$2"
        ;;
    "stop")
        stop_services "$2"
        ;;
    "restart")
        stop_services "$2"
        start_services "$2"
        ;;
    "rebuild")
        check_env_file
        rebuild_services "$2"
        ;;
    "logs")
        view_logs "$2" "$3"
        ;;
    "exec")
        exec_service "$2" "$3" "${@:4}"
        ;;
    "delete-volumes")
        delete_volumes "$2"
        ;;
    "help"|"")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac 