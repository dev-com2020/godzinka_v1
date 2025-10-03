"""
Skrypt do budowania aplikacji Godzinka jako plik exe
Używa PyInstaller do konwersji aplikacji Python na wykonywalny plik
"""

import os
import sys
import subprocess
import shutil

def build_exe():
    """Buduje aplikację jako plik exe"""
    
    print("Rozpoczynam budowanie aplikacji Godzinka...")
    
    # Sprawdź czy PyInstaller jest zainstalowany
    try:
        import PyInstaller
        print(f"PyInstaller {PyInstaller.__version__} jest zainstalowany")
    except ImportError:
        print("PyInstaller nie jest zainstalowany. Instaluję...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller został zainstalowany")
    
    # Komenda PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Jeden plik exe
        "--windowed",                   # Bez konsoli (GUI app)
        "--name=Godzinka",              # Nazwa pliku exe
        "--distpath=dist",              # Katalog wyjściowy
        "--workpath=build",             # Katalog tymczasowy
        "--specpath=.",                 # Gdzie umieścić plik spec
        "--clean",                      # Wyczyść poprzednie budowania
        "--noconfirm",                  # Nie pytaj o potwierdzenie
        "main.py"                       # Główny plik aplikacji
    ]
    
    # Opcjonalne dodatkowe opcje
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon=icon.ico"])
        print("Używam ikony: icon.ico")
    
    # Dodaj dodatkowe pliki jeśli istnieją
    if os.path.exists("README.md"):
        cmd.extend(["--add-data", "README.md;."])
    
    print(f"Uruchamiam: {' '.join(cmd)}")
    
    try:
        # Uruchom PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("Budowanie zakończone pomyślnie!")
        
        # Sprawdź czy plik exe został utworzony
        exe_path = os.path.join("dist", "Godzinka.exe")
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"Plik exe utworzony: {exe_path}")
            print(f"Rozmiar pliku: {file_size:.1f} MB")
            
            # Skopiuj na pulpit (opcjonalne)
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Godzinka.exe")
            try:
                shutil.copy2(exe_path, desktop_path)
                print(f"Skopiowano na pulpit: {desktop_path}")
            except Exception as e:
                print(f"Nie udało się skopiować na pulpit: {e}")
        else:
            print("Plik exe nie został utworzony")
            
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas budowania: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    
    return True

def clean_build():
    """Czyści pliki tymczasowe budowania"""
    print("Czyszczenie plików tymczasowych...")
    
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["Godzinka.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Usunięto katalog: {dir_name}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Usunięto plik: {file_name}")

def main():
    """Główna funkcja"""
    print("=" * 50)
    print("BUILDER APLIKACJI GODZINKA")
    print("=" * 50)
    
    # Sprawdź czy main.py istnieje
    if not os.path.exists("main.py"):
        print("Nie znaleziono pliku main.py")
        return
    
    # Wyczyść poprzednie budowania
    clean_build()
    
    # Zbuduj aplikację
    if build_exe():
        print("\nBudowanie zakończone pomyślnie!")
        print("Plik exe znajduje się w katalogu 'dist'")
        print("Możesz uruchomić aplikację z pulpitu")
    else:
        print("\nBudowanie nie powiodło się")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
