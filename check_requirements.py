import pkg_resources
import subprocess
import sys

def check_requirements():
    """Check if all required packages are installed and install missing ones"""
    # Define required packages with their versions
    required_packages = {
        'streamlit': '>=1.20.0',
        'yfinance': '>=0.2.0',
        'pandas': '>=1.3.0',
        'tqdm': '>=4.65.0',
    }

    missing_packages = []
    outdated_packages = []

    # Check each required package
    for package, version in required_packages.items():
        try:
            # Check if package is installed and meets version requirement
            pkg_resources.require(f"{package}{version}")
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
        except pkg_resources.VersionConflict:
            outdated_packages.append(package)

    if missing_packages or outdated_packages:
        print("Some required packages are missing or outdated.")
        
        if missing_packages:
            print("\nMissing packages:")
            for package in missing_packages:
                print(f"- {package}")
        
        if outdated_packages:
            print("\nOutdated packages:")
            for package in outdated_packages:
                print(f"- {package}")

        # Ask user if they want to install/update packages
        response = input("\nWould you like to install/update these packages? (y/n): ")
        if response.lower() == 'y':
            # Install missing packages
            for package in missing_packages:
                print(f"\nInstalling {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                    f"{package}{required_packages[package]}"])
            
            # Update outdated packages
            for package in outdated_packages:
                print(f"\nUpdating {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade",
                                    f"{package}{required_packages[package]}"])
            
            print("\nAll required packages have been installed/updated!")
            return True
        else:
            print("\nPlease install/update the required packages manually.")
            return False
    else:
        print("All required packages are installed and up to date!")
        return True

def get_package_versions():
    """Get versions of all installed packages relevant to the project"""
    packages = ['streamlit', 'yfinance', 'pandas', 'tqdm']
    versions = {}
    
    for package in packages:
        try:
            version = pkg_resources.get_distribution(package).version
            versions[package] = version
        except pkg_resources.DistributionNotFound:
            versions[package] = "Not installed"
    
    return versions

if __name__ == "__main__":
    print("Checking requirements for Stock Data Fetcher...")
    print("-" * 50)
    
    # Check requirements
    requirements_met = check_requirements()
    
    if requirements_met:
        print("\nCurrent package versions:")
        versions = get_package_versions()
        for package, version in versions.items():
            print(f"{package}: {version}")
        
        print("\nYou can now run the Stock Data Fetcher with:")
        print("streamlit run stock_app.py")