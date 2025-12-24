"""
SAGE - Smart AI Desktop Assistant
Setup script for easy installation and configuration.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.10 or higher."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required.")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install required dependencies."""
    try:
        print("📦 Installing dependencies...")
        
        # Determine pip path based on OS
        if os.name == 'nt':  # Windows
            pip_path = Path("venv/Scripts/pip.exe")
        else:  # Linux/Mac
            pip_path = Path("venv/bin/pip")
        
        if not pip_path.exists():
            print("❌ Virtual environment pip not found")
            return False
        
        # Install requirements
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_configuration():
    """Set up configuration files."""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ Configuration file (.env) already exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    try:
        shutil.copy(env_example, env_file)
        print("✅ Configuration file (.env) created")
        print("⚠️  Please edit .env file and add your API keys:")
        print("   - GROQ_API_KEY (required)")
        print("   - PICOVOICE_ACCESS_KEY (required)")
        print("   - OPENROUTER_API_KEY (optional, for advanced features)")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration file: {e}")
        return False

def create_data_directories():
    """Create necessary data directories."""
    directories = [
        "data",
        "data/recordings",
        "data/generated_tools"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Data directories created")
    return True

def check_system_requirements():
    """Check system-specific requirements."""
    print("🔍 Checking system requirements...")
    
    # Check if running on Windows (primary supported platform)
    if os.name != 'nt':
        print("⚠️  SAGE is primarily designed for Windows")
        print("   Some features may not work on other platforms")
    
    # Check for microphone access (basic check)
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        if p.get_device_count() > 0:
            print("✅ Audio devices detected")
        p.terminate()
    except:
        print("⚠️  Audio system check failed - voice features may not work")
    
    return True

def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "="*60)
    print("🎉 SAGE Setup Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your API keys:")
    print("   - Get Groq API key: https://console.groq.com/")
    print("   - Get Picovoice key: https://console.picovoice.ai/")
    print("   - (Optional) Get OpenRouter key: https://openrouter.ai/")
    
    print("\n2. Activate virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Linux/Mac
        print("   source venv/bin/activate")
    
    print("\n3. Run SAGE:")
    print("   python main.py")
    
    print("\n📚 Documentation:")
    print("   - README.md - Full documentation")
    print("   - PROJECT_DESCRIPTION.md - Detailed project info")
    print("   - CONTRIBUTING.md - How to contribute")
    
    print("\n🎤 Voice Commands Examples:")
    print("   - 'Hey SAGE' (wake word)")
    print("   - 'Open Chrome'")
    print("   - 'What's the weather?'")
    print("   - 'Send email to manager'")
    print("   - 'Play music on Spotify'")
    
    print("\n🔧 Troubleshooting:")
    print("   - Check microphone permissions")
    print("   - Ensure Windows Speech is enabled")
    print("   - Verify API keys in .env file")
    
    print("\n" + "="*60)

def main():
    """Main setup function."""
    print("🧠 SAGE - Smart AI Desktop Assistant")
    print("🚀 Setup Script")
    print("="*50)
    
    # Check requirements
    if not check_python_version():
        return False
    
    # Setup steps
    steps = [
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up configuration", setup_configuration),
        ("Creating data directories", create_data_directories),
        ("Checking system requirements", check_system_requirements)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            return False
    
    print_next_steps()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)