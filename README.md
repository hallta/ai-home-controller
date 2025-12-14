# LLM Test Docker Environment

A Docker-based environment for running and experimenting with large language models (LLMs) locally using [Ollama](https://ollama.com/).

## Installation

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) installed and running on your system
- Git (for cloning the repository)

### Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd llm-test
   ```

2. **Make the install script executable (if needed):**
   ```bash
   chmod +x install.sh
   ```

## Setup

### Building and Running the Container

Run the installation script to build the Docker image and start the container:

```bash
./install.sh
```

This script will:
- Build the Docker image tagged as `llm-test:0.1.0`
- Start a container in detached mode with:
  - 6GB memory allocated
  - 4 CPUs allocated
  - Port 5432 exposed (for potential database services)
  - Shared memory size of 6GB (required for Ollama)

### Accessing the Container

1. **Find the running container:**
   ```bash
   docker ps
   ```
   Note the container ID or name from the output.

2. **Enter the container as the `trevor` user:**
   ```bash
   docker exec -it <container-id> bash
   ```
   Or if you know the container name:
   ```bash
   docker exec -it <container-name> bash
   ```

## Usage

### Basic Ollama Commands

Once inside the container, you can use Ollama to interact with LLMs:

**List available models:**
```bash
ollama list
```

**Pull a model (download it locally):**
```bash
ollama pull llama2
ollama pull llama3
ollama pull llava
```

**Run a model interactively:**
```bash
ollama run llama2
ollama run llama3
```

**Generate text via API:**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

### Using the Send Request Script

The `send_request.sh` script provides a convenient way to send requests to Ollama from your host machine:

1. **Ensure the container is running** and Ollama is accessible on port 11434 (default Ollama port)

2. **Edit the script** to set your desired model:
   ```bash
   vim send_request.sh
   ```
   Update the `model` variable (e.g., `llama3`, `llava`, etc.)

3. **Run the script:**
   ```bash
   ./send_request.sh
   ```

The script sends a POST request to the Ollama API and formats the JSON response.

### Example: Using Prompts

You can use prompt files like `garage.prompt` with Ollama. For example:

```bash
# Inside the container
ollama run llava < garage.prompt
```

Or via API:
```bash
curl -X POST http://localhost:11434/api/generate -d @- <<EOF
{
  "model": "llava",
  "prompt": "$(cat garage.prompt)"
}
EOF
```

### Container Configuration

The container includes:
- **Pre-installed tools:** curl, git, vim, screen, wget, ping, and other utilities
- **User account:** `trevor` with sudo privileges (no password required)
- **Ollama:** Pre-installed and ready to use
- **Base OS:** Debian Trixie (slim)

### Resource Limits

Default resource allocation (configurable in `install.sh`):
- Memory: 6GB
- CPUs: 4
- Shared memory: 6GB

To customize these limits, edit `install.sh` and modify the `docker run` command parameters.

## Troubleshooting

**Container won't start:**
- Ensure Docker is running: `docker ps`
- Check available resources (memory/CPU)
- Review Docker logs: `docker logs <container-id>`

**Ollama not responding:**
- Verify the container is running: `docker ps`
- Check if Ollama service is running inside the container
- Ensure port 11434 is accessible (Ollama's default port)

**Permission denied on install.sh:**
```bash
chmod +x install.sh
```

**Model download fails:**
- Check internet connectivity inside the container
- Verify sufficient disk space: `df -h`
- Try pulling a smaller model first

## Additional Resources

- [Ollama Documentation](https://ollama.com/)
- [Docker Documentation](https://docs.docker.com/)
