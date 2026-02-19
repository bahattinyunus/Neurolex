import subprocess
import time
import sys
import os

def check_dependencies():
    """Checks if critical dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import streamlit
        print("✅ Gerekli kütüphaneler kontrol edildi.")
    except ImportError as e:
        print(f"❌ Eksik kütüphane: {e.name}")
        print("Lütfen şu komutu çalıştırın: pip install -r requirements.txt")
        sys.exit(1)

def check_submodule():
    """Checks if the ML submodule is initialized."""
    submodule_path = os.path.join(os.path.dirname(__file__), "personalized.ml.for.stress.detection")
    if os.path.exists(submodule_path) and not os.listdir(submodule_path):
        print("⚠️ Uyarı: 'personalized.ml.for.stress.detection' submodule boş görünüyor.")
        print("Otomatik olarak başlatılıyor...")
        try:
            subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True)
            print("✅ Submodule başarıyla güncellendi.")
        except subprocess.CalledProcessError:
            print("❌ Submodule güncellenemedi. Lütfen manuel olarak 'git submodule update --init' çalıştırın.")

def run_neurodelay():
    print("🧠 NeuroDelay: Sistem Başlatılıyor...")
    
    check_dependencies()
    check_submodule()
    
    # 1. Backend (Uvicorn)
    print("🚀 Backend (API) başlatılıyor...")
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "src.software.backend.main:app", "--reload"], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)

    # 2. Dashboard (Streamlit)
    print("📊 Dashboard (Web Arayüzü) başlatılıyor...")
    # Wait a bit for backend to start
    time.sleep(2)
    dashboard = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "src/web/dashboard/app.py"], 
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)

    # 3. Simulation (Data/Sensor Generator)
    print("🧬 Simülasyon (Sensör Verisi) başlatılıyor...")
    time.sleep(2)
    simulation = subprocess.Popen([sys.executable, "-m", "src.software.simulation.generator"], 
                                  creationflags=subprocess.CREATE_NEW_CONSOLE)

    print("\n✅ Tüm sistemler aktif!")
    print("Backend: http://localhost:8000")
    print("Dashboard: http://localhost:8501")
    print("\nÇıkış yapmak için açılan pencereleri kapatabilirsiniz.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKapatılıyor...")
        backend.terminate()
        dashboard.terminate()
        simulation.terminate()

if __name__ == "__main__":
    run_neurodelay()
