import subprocess
import sys

print("=" * 50)
print("🚀 Altra Research - Installing Dependencies")
print("=" * 50)

def install(package):
    print(f"\n📦 Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully!")
    except:
        print(f"❌ Failed to install {package}")
        return False
    return True

# Upgrade pip first
print("\n1️⃣ Upgrading pip...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# Install packages one by one
packages = [
    "wheel",
    "setuptools",
    "numpy",
    "pandas",
    "streamlit",
    "plotly",
    "streamlit-option-menu",
    "requests",
    "Pillow"
]

success_count = 0
for i, package in enumerate(packages, 1):
    print(f"\n{i}/{len(packages)}")
    if install(package):
        success_count += 1

print("\n" + "=" * 50)
print(f"✅ Installation Complete! ({success_count}/{len(packages)} packages)")
print("=" * 50)
print("\n🎯 Next step: Run the app with command:")
print("   streamlit run app.py")
print("\n📧 Contact: altraresearch@gmail.com")
print("📍 Location: Eruthoorkadai")