
import os

def list_large_files(threshold_mb=10):
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        for f in files:
            full_path = os.path.join(root, f)
            try:
                size_mb = os.path.getsize(full_path) / (1024 * 1024)
                if size_mb > threshold_mb:
                    print(f"{full_path} : {size_mb:.2f} MB")
            except Exception:
                pass

if __name__ == "__main__":
    list_large_files()
