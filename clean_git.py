
import os
import shutil
import stat

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

dirs_to_clean = [
    "STRESS-DETECTION-FOR-IT-PROFESSIONALS",
    "Stress-Prediction-Using-HRV",
    "machine-learning-model"
]

base_dir = os.getcwd()

for d in dirs_to_clean:
    target = os.path.join(base_dir, d, ".git")
    if os.path.exists(target):
        print(f"Removing {target}...")
        try:
            if os.path.isfile(target):
                os.remove(target) # submodule file
            else:
                shutil.rmtree(target, onerror=remove_readonly)
            print("Success.")
        except Exception as e:
            print(f"Failed: {e}")
    else:
        print(f"{target} not found.")

# Also try to remove from git index if possible, using subprocess
import subprocess
for d in dirs_to_clean:
    try:
        subprocess.run(["git", "rm", "--cached", d], check=False)
    except Exception as e:
        print(f"Git rm cached failed for {d}: {e}")
