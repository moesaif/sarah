# Docker Usage Guide for Sarah

This guide explains how to build and run Sarah using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier management)

## Building the Docker Image

### Option 1: Using Docker directly

```bash
# Build the image
docker build -t sarah:latest .

# Run Sarah
docker run -it --rm sarah:latest

# Run Sarah with a specific command (e.g., list available plugins)
docker run -it --rm sarah:latest sarah list

# Run Sarah with a plugin (e.g., weather plugin)
docker run -it --rm sarah:latest sarah weather
```

### Option 2: Using Docker Compose

```bash
# Build and run with docker-compose
docker-compose up --build

# Run a specific command
docker-compose run --rm sarah sarah list

# Run interactively
docker-compose run --rm sarah /bin/bash
```

## Available Commands

Once inside the container, you can use Sarah just like the native installation:

```bash
# List all available plugins
sarah list

# Use a specific plugin (replace 'plugin-name' with actual plugin name)
sarah plugin-name [arguments]

# Examples:
sarah weather
sarah time
sarah hi
sarah wiki search-term
```

## Available Plugins

Sarah comes with several built-in plugins:

- `adhan` - Prayer times
- `github` - GitHub integration
- `google` - Google search
- `hi` - Simple greeting
- `marketwatch` - Market data
- `speedtest` - Internet speed test
- `time` - Time utilities
- `watch` - File watching
- `weather` - Weather information
- `whois` - Domain/IP information
- `wiki` - Wikipedia search
- `youtube` - YouTube utilities

## Troubleshooting

### Build Issues

If you encounter build issues:

1. Make sure you have the latest Docker version
2. Try building with `--no-cache`:
   ```bash
   docker build --no-cache -t sarah:latest .
   ```

### Runtime Issues

If Sarah doesn't work properly:

1. Check if all plugins are loaded:

   ```bash
   docker run -it --rm sarah:latest sarah list
   ```

2. Run with bash to debug:
   ```bash
   docker run -it --rm sarah:latest /bin/bash
   ```

## Customization

### Adding Your Own Plugins

To add your own plugins:

1. Place your plugin files in the `plugins/` directory
2. Follow the existing plugin structure (`.plugin` file and implementation)
3. Rebuild the Docker image

### Persistent Data

If you need to persist data between container runs, uncomment the volumes section in `docker-compose.yml`:

```yaml
volumes:
  - ./data:/app/data
```

## Development

For development purposes, you can mount the source code:

```bash
docker run -it --rm -v $(pwd):/app sarah:latest /bin/bash
```

This allows you to modify the code and rebuild without recreating the container.
