#!/usr/bin/env python3
"""
CodeSniff Application Launcher
Automates setup and runs both backend and frontend servers
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import time


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.CYAN}→ {text}{Colors.END}")


def check_command(command):
    """Check if a command exists"""
    return shutil.which(command) is not None


def get_python_command():
    """Get the correct Python command"""
    if check_command('python3'):
        return 'python3'
    elif check_command('python'):
        return 'python'
    else:
        return None


def get_pip_command():
    """Get the correct pip command"""
    if check_command('pip3'):
        return 'pip3'
    elif check_command('pip'):
        return 'pip'
    else:
        return None


def check_prerequisites():
    """Check if all required software is installed"""
    print_header("Checking Prerequisites")

    issues = []

    # Check Python
    python_cmd = get_python_command()
    if python_cmd:
        result = subprocess.run([python_cmd, '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Python: {version}")
    else:
        print_error("Python not found")
        issues.append("Install Python 3.10+ from https://www.python.org/downloads/")

    # Check pip
    pip_cmd = get_pip_command()
    if pip_cmd:
        print_success(f"pip: Found")
    else:
        print_error("pip not found")
        issues.append("Install pip (usually comes with Python)")

    # Check Node.js
    if check_command('node'):
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Node.js: {version}")
    else:
        print_error("Node.js not found")
        issues.append("Install Node.js 18+ from https://nodejs.org/")

    # Check npm
    if check_command('npm'):
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"npm: {version}")
    else:
        print_error("npm not found")
        issues.append("Install npm (usually comes with Node.js)")

    # Check Git
    if check_command('git'):
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Git: {version}")
    else:
        print_warning("Git not found (optional, needed for GitHub cloning feature)")

    if issues:
        print_error("\nMissing prerequisites:")
        for issue in issues:
            print(f"  • {issue}")
        return False

    print_success("\nAll prerequisites satisfied!")
    return True


def setup_backend():
    """Set up backend environment"""
    print_header("Setting Up Backend")

    backend_dir = Path(__file__).parent / 'backend'
    venv_dir = backend_dir / 'venv'

    os.chdir(backend_dir)

    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print_info("Creating virtual environment...")
        python_cmd = get_python_command()
        subprocess.run([python_cmd, '-m', 'venv', 'venv'], check=True)
        print_success("Virtual environment created")
    else:
        print_success("Virtual environment already exists")

    # Determine venv activation and pip path
    is_windows = platform.system() == 'Windows'
    if is_windows:
        pip_path = venv_dir / 'Scripts' / 'pip.exe'
    else:
        pip_path = venv_dir / 'bin' / 'pip'

    # Upgrade pip
    print_info("Upgrading pip...")
    subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], check=True, capture_output=True)
    print_success("pip upgraded")

    # Install dependencies
    print_info("Installing Python dependencies (this may take a few minutes)...")
    subprocess.run([str(pip_path), 'install', '-r', 'requirements.txt'], check=True)
    print_success("Python dependencies installed")

    # Check for .env file
    env_file = backend_dir / '.env'
    env_example = backend_dir / '.env.example'

    if not env_file.exists():
        if env_example.exists():
            print_warning(".env file not found")
            print_info("Copying .env.example to .env...")
            shutil.copy(env_example, env_file)
            print_success(".env file created")
            print_warning("\n⚠ IMPORTANT: Edit backend/.env and add your GROQ_API_KEY for chatbot feature")
            print_info("Get your API key from: https://console.groq.com")
        else:
            print_error(".env.example not found!")
    else:
        print_success(".env file exists")
        # Check if GROQ_API_KEY is set
        with open(env_file) as f:
            content = f.read()
            if 'GROQ_API_KEY=your_groq_api_key_here' in content or 'GROQ_API_KEY=' not in content:
                print_warning("GROQ_API_KEY not configured in .env")
                print_info("Chatbot feature will not work until you add your Groq API key")

    print_success("\nBackend setup complete!")


def setup_frontend():
    """Set up frontend environment"""
    print_header("Setting Up Frontend")

    frontend_dir = Path(__file__).parent / 'frontend'
    node_modules = frontend_dir / 'node_modules'

    os.chdir(frontend_dir)

    # Install npm dependencies
    if not node_modules.exists():
        print_info("Installing npm dependencies (this may take a few minutes)...")
        subprocess.run(['npm', 'install'], check=True)
        print_success("npm dependencies installed")
    else:
        print_success("npm dependencies already installed")

    print_success("\nFrontend setup complete!")


def start_backend():
    """Start the backend server"""
    print_header("Starting Backend Server")

    backend_dir = Path(__file__).parent / 'backend'
    venv_dir = backend_dir / 'venv'

    is_windows = platform.system() == 'Windows'
    if is_windows:
        python_path = venv_dir / 'Scripts' / 'python.exe'
    else:
        python_path = venv_dir / 'bin' / 'python'

    os.chdir(backend_dir)

    print_info("Starting FastAPI server on http://localhost:8000")
    print_info("Press Ctrl+C to stop both servers\n")

    # Start backend process
    return subprocess.Popen(
        [str(python_path), '-m', 'app.main'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )


def start_frontend():
    """Start the frontend dev server"""
    print_header("Starting Frontend Server")

    frontend_dir = Path(__file__).parent / 'frontend'
    os.chdir(frontend_dir)

    print_info("Starting Vite dev server on http://localhost:5173")
    print_info("Opening browser in 5 seconds...\n")

    # Start frontend process
    return subprocess.Popen(
        ['npm', 'run', 'dev'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )


def run_servers():
    """Run both backend and frontend servers"""
    print_header("Starting CodeSniff")

    backend_process = None
    frontend_process = None

    try:
        # Start backend
        backend_process = start_backend()

        # Wait a bit for backend to start
        print_info("Waiting for backend to initialize...")
        time.sleep(3)

        # Start frontend
        frontend_process = start_frontend()

        # Wait a bit then open browser
        time.sleep(5)

        # Open browser
        url = "http://localhost:5173"
        print_success(f"\nCodeSniff is running!")
        print_info(f"Frontend: {url}")
        print_info(f"Backend API: http://localhost:8000")
        print_info(f"API Docs: http://localhost:8000/docs")

        # Try to open browser
        try:
            import webbrowser
            webbrowser.open(url)
            print_success("Browser opened")
        except:
            print_warning("Could not open browser automatically")
            print_info(f"Please open {url} in your browser")

        print(f"\n{Colors.BOLD}{Colors.GREEN}Press Ctrl+C to stop servers{Colors.END}\n")

        # Monitor processes and print output
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print_error("Backend process stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print_error("Frontend process stopped unexpectedly")
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Stopping servers...{Colors.END}")

    finally:
        # Clean up processes
        if backend_process:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()

        if frontend_process:
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()

        print_success("Servers stopped")
        print(f"\n{Colors.BOLD}Thanks for using CodeSniff!{Colors.END}\n")


def main():
    """Main application entry point"""
    print(f"""
{Colors.BOLD}{Colors.CYAN}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                      CodeSniff                            ║
║          Semantic Code Search Engine                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.END}
""")

    # Change to script directory
    os.chdir(Path(__file__).parent)

    # Check prerequisites
    if not check_prerequisites():
        print_error("\nPlease install missing prerequisites and try again")
        sys.exit(1)

    # Setup backend
    try:
        setup_backend()
    except Exception as e:
        print_error(f"Backend setup failed: {e}")
        sys.exit(1)

    # Setup frontend
    try:
        setup_frontend()
    except Exception as e:
        print_error(f"Frontend setup failed: {e}")
        sys.exit(1)

    # Run servers
    try:
        run_servers()
    except Exception as e:
        print_error(f"Error running servers: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
