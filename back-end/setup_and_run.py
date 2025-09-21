#!/usr/bin/env python3
"""
Tree Planting Dashboard Setup Script
This script helps set up and run the complete dashboard system.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def create_tree_species_json():
    """Create the tree_species.json file with your provided data"""
    tree_data = {
        "species": {
            "Bargad (Banyan)": {
                "Avg_Biomass_kg_per_year": 90,
                "Carbon_Content_Ratio": 0.5,
                "CO2_Conversion_Factor": 3.67,
                "Survival_Rate": 0.7,
                "Lifespan_Years": 20,
                "CO2_Sequestration_20yrs": [
                    115.6, 231.21, 346.81, 462.42, 578.02, 693.63, 809.23, 924.84, 1040.44, 1156.05,
                    1271.65, 1387.26, 1502.86, 1618.47, 1734.07, 1849.68, 1965.28, 2080.89, 2196.49, 2312.1
                ]
            },
            "Gulmohar": {
                "Avg_Biomass_kg_per_year": 45,
                "Carbon_Content_Ratio": 0.5,
                "CO2_Conversion_Factor": 3.67,
                "Survival_Rate": 0.8,
                "Lifespan_Years": 20,
                "CO2_Sequestration_20yrs": [
                    66.06, 132.12, 198.18, 264.24, 330.3, 396.36, 462.42, 528.48, 594.54, 660.6,
                    726.66, 792.72, 858.78, 924.84, 990.9, 1056.96, 1123.02, 1189.08, 1255.14, 1321.2
                ]
            },
            "Neem": {
                "Avg_Biomass_kg_per_year": 60,
                "Carbon_Content_Ratio": 0.5,
                "CO2_Conversion_Factor": 3.67,
                "Survival_Rate": 0.85,
                "Lifespan_Years": 30,
                "CO2_Sequestration_20yrs": [
                    93.58, 187.17, 280.75, 374.34, 467.92, 561.51, 655.09, 748.68, 842.26, 935.85,
                    1029.43, 1123.02, 1216.61, 1310.19, 1403.77, 1497.36, 1590.94, 1684.53, 1778.11, 1871.7
                ]
            },
            "Peepal": {
                "Avg_Biomass_kg_per_year": 80,
                "Carbon_Content_Ratio": 0.5,
                "CO2_Conversion_Factor": 3.67,
                "Survival_Rate": 0.75,
                "Lifespan_Years": 25,
                "CO2_Sequestration_20yrs": [
                    110.1, 220.2, 330.3, 440.4, 550.5, 660.6, 770.7, 880.8, 990.9, 1101.0,
                    1211.1, 1321.2, 1431.3, 1541.4, 1651.5, 1761.6, 1871.7, 1981.8, 2091.9, 2202.0
                ]
            },
            # Add more species as needed...
            "Mango": {
                "Avg_Biomass_kg_per_year": 55,
                "Carbon_Content_Ratio": 0.5,
                "CO2_Conversion_Factor": 3.67,
                "Survival_Rate": 0.8,
                "Lifespan_Years": 30,
                "CO2_Sequestration_20yrs": [
                    80.74, 161.48, 242.22, 322.96, 403.7, 484.44, 565.18, 645.92, 726.66, 807.4,
                    888.14, 968.88, 1049.62, 1130.36, 1211.1, 1291.84, 1372.58, 1453.32, 1534.06, 1614.8
                ]
            }
        }
    }
    
    with open('tree_species.json', 'w') as f:
        json.dump(tree_data, f, indent=2)
    print("✓ Created tree_species.json")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install Python requirements"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Python packages installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = ['generated_charts']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✓ Created necessary directories")

def run_fastapi_server():
    """Run the FastAPI server"""
    try:
        print("🚀 Starting FastAPI server...")
        print("📊 Dashboard will be available at: http://localhost:8000")
        print("📚 API docs available at: http://localhost:8000/docs")
        print("Press Ctrl+C to stop the server")
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    """Main setup function"""
    print("🌳 Tree Planting Dashboard Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Create tree species data file
    if not os.path.exists('tree_species.json'):
        create_tree_species_json()
    else:
        print("✓ tree_species.json already exists")
    
    # Install requirements
    if os.path.exists('requirements.txt'):
        install_requirements()
    else:
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Start the FastAPI server: python setup_and_run.py")
    print("2. Open your React app and test the dashboard generation")
    print("3. Generated charts will be saved in ./generated_charts/")
    
    # Ask if user wants to start the server
    start_server = input("\nStart the FastAPI server now? (y/N): ").lower().strip()
    if start_server == 'y':
        run_fastapi_server()

if __name__ == "__main__":
    main()