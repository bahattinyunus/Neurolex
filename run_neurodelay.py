import subprocess
import time
import sys
import os

def run_neurodelay():
    print("🧠 NeuroDelay: Sistem Başlatılıyor...")
    
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
