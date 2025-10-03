# Zegar Przerw - Aplikacja do Szkoleń

Aplikacja w Tkinter do zarządzania przerwami podczas szkoleń z osobnymi interfejsami dla trenera i uczestników. Aplikacja może być uruchamiana jako plik exe na pulpicie.

## Funkcje

- ⏰ **Zegar Przerw** - Odliczanie czasu przerwy z możliwością ustawienia
- 👨‍🏫 **Panel Trenera** - Pełna kontrola nad czasem przerwy
- 👥 **Okna Uczestników** - Wyświetlanie pozostałego czasu dla uczestników
- 🎨 **System Kolorów** - Zielony → Żółty → Czerwony (im bliżej końca)
- 📱 **Wielokrotne Okna** - Możliwość otwarcia wielu okien dla uczestników
- 🔔 **Automatyczne Zakończenie** - Powiadomienie o końcu przerwy
- 💾 **Jednoplikowy exe** - Łatwa dystrybucja

## Instalacja i uruchomienie

### Opcja 1: Uruchomienie z kodu źródłowego

1. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

2. Uruchom aplikację:
```bash
python main.py
```

### Opcja 2: Budowanie pliku exe

1. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

2. Zbuduj aplikację:
```bash
python build_exe.py
```

3. Plik `Godzinka.exe` zostanie utworzony w katalogu `dist` i automatycznie skopiowany na pulpit.

## Struktura projektu

```
godzinka_v1/
├── main.py              # Główna aplikacja (BreakTimerApp)
├── build_exe.py         # Skrypt do budowania exe
├── requirements.txt     # Wymagane pakiety
├── README.md           # Ten plik
├── dist/               # Katalog z plikiem exe (po budowaniu)
└── icon.ico            # Ikona aplikacji (opcjonalna)
```

## Użycie

### Panel Trenera:
1. **Ustaw czas przerwy** - Wprowadź liczbę minut i naciśnij "Ustaw"
2. **Start przerwy** - Naciśnij "Start Przerwy" aby rozpocząć odliczanie
3. **Kontrola** - Użyj "Stop Przerwy" lub "Reset" do kontrolowania
4. **Okna uczestników** - Otwórz okna dla uczestników przyciskiem "Otwórz Okno Uczestników"

### Okna Uczestników:
- **Duży zegar** - Wyświetla pozostały czas w formacie MM:SS
- **System kolorów**:
  - 🟢 **Zielony** - Początek i środek przerwy
  - 🟡 **Żółty** - Ostatnie 30% czasu przerwy
  - 🔴 **Czerwony** - Ostatnia minuta przerwy
- **Status** - Informuje o stanie przerwy

## Budowanie exe - Szczegóły

Aplikacja używa PyInstaller do konwersji na plik wykonywalny:

- `--onefile`: Tworzy jeden plik exe
- `--windowed`: Bez okna konsoli (tylko GUI)
- `--clean`: Czyści poprzednie budowania
- Automatyczne kopiowanie na pulpit

## Wymagania systemowe

- Windows 10/11
- Python 3.7+ (tylko do budowania)
- Tkinter (wbudowany w Python)

## Rozwiązywanie problemów

### Problem z budowaniem exe
```bash
# Zainstaluj najnowszy PyInstaller
pip install --upgrade pyinstaller

# Uruchom ponownie budowanie
python build_exe.py
```

### Problem z uruchomieniem aplikacji
- Sprawdź czy masz zainstalowany Python z Tkinter
- Uruchom `python main.py` aby przetestować aplikację

## Licencja

Ten projekt jest dostępny na licencji MIT. Możesz go swobodnie używać i modyfikować.
