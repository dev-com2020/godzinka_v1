import tkinter as tk
from tkinter import messagebox
import datetime
import os
import sys

class BreakTimerApp:
    def __init__(self):
        # Główne zmienne
        self.break_duration = 15  # domyślnie 15 minut
        self.remaining_time = 0
        self.is_running = False
        
        # Lista okien uczestników
        self.participant_windows = []
        
        # Tworzenie głównego okna
        self.root = tk.Tk()
        self.root.title("Zegar Przerw - Panel Trenera")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Centrowanie okna
        self.center_window(self.root)
        
        # Ustawienie ikony
        try:
            if hasattr(sys, '_MEIPASS'):
                icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
            else:
                icon_path = 'icon.ico'
            self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Konfiguracja interfejsu
        self.setup_ui()
        
    def center_window(self, window):
        """Centruje okno na ekranie"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Konfiguruje interfejs użytkownika"""
        # Główny frame
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tytuł
        title_label = tk.Label(main_frame, text="Panel Trenera - Zegar Przerw", 
                              font=("Arial", 16, "bold"), bg="white")
        title_label.pack(pady=(0, 20))
        
        # Ustawienia czasu przerwy
        settings_frame = tk.LabelFrame(main_frame, text="Ustawienia Przerwy", 
                                      font=("Arial", 10, "bold"), bg="white")
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        settings_inner = tk.Frame(settings_frame, bg="white")
        settings_inner.pack(pady=15, padx=15)
        
        tk.Label(settings_inner, text="Czas przerwy (minuty):", 
                font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=(0, 10))
        
        self.duration_entry = tk.Entry(settings_inner, width=10, font=("Arial", 12))
        self.duration_entry.insert(0, "15")
        self.duration_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(settings_inner, text="Ustaw", 
                 command=self.set_duration).pack(side=tk.LEFT, padx=(0, 20))
        
        # Lista rozwijana ze standardowymi czasami
        tk.Label(settings_inner, text="Szybkie ustawienia:", 
                font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=(0, 10))
        
        self.duration_var = tk.StringVar(value="15")
        self.duration_combo = tk.OptionMenu(settings_inner, self.duration_var, 
                                          "15", "30", "45", "60",
                                          command=self.on_duration_change)
        self.duration_combo.config(font=("Arial", 10), width=8)
        self.duration_combo.pack(side=tk.LEFT)
        
        # Kontrolki timera
        control_frame = tk.LabelFrame(main_frame, text="Kontrola Timera", 
                                     font=("Arial", 10, "bold"), bg="white")
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        button_frame = tk.Frame(control_frame, bg="white")
        button_frame.pack(pady=15)
        
        self.start_button = tk.Button(button_frame, text="Start Przerwy", 
                                     command=self.start_break, font=("Arial", 10))
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(button_frame, text="Stop Przerwy", 
                                    command=self.stop_break, state="disabled", font=("Arial", 10))
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.reset_button = tk.Button(button_frame, text="Reset", 
                                     command=self.reset_break, font=("Arial", 10))
        self.reset_button.pack(side=tk.LEFT)
        
        # Wyświetlacz czasu dla trenera
        self.time_label = tk.Label(control_frame, text="00:00", 
                                  font=("Arial", 20, "bold"), bg="white")
        self.time_label.pack(pady=(10, 15))
        
        # Zarządzanie oknami uczestników
        participants_frame = tk.LabelFrame(main_frame, text="Okna Uczestników", 
                                          font=("Arial", 10, "bold"), bg="white")
        participants_frame.pack(fill=tk.X, pady=(0, 20))
        
        participants_control_frame = tk.Frame(participants_frame, bg="white")
        participants_control_frame.pack(pady=15)
        
        tk.Button(participants_control_frame, text="Otwórz Okno Uczestników", 
                 command=self.open_participant_window, font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(participants_control_frame, text="Zamknij Wszystkie Okna", 
                 command=self.close_all_participant_windows, font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Informacje
        info_frame = tk.Frame(main_frame, bg="white")
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(info_frame, text="Zegar Przerw v2.0", 
                font=("Arial", 8), bg="white").pack(side=tk.LEFT)
        tk.Button(info_frame, text="O aplikacji", 
                 command=self.show_about, font=("Arial", 8)).pack(side=tk.RIGHT)
    
    def create_participant_window(self):
        """Tworzy okno dla uczestników"""
        window = tk.Toplevel(self.root)
        window.title("Zegar Przerwy - Uczestnicy")
        window.geometry("400x300")
        window.resizable(False, False)
        window.configure(bg="white")
        
        # Centrowanie okna
        self.center_window(window)
        
        # Główny frame
        main_frame = tk.Frame(window, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tytuł
        title_label = tk.Label(main_frame, text="Zegar Przerwy", 
                              font=("Arial", 18, "bold"), bg="white")
        title_label.pack(pady=(0, 20))
        
        # Wyświetlacz czasu
        time_label = tk.Label(main_frame, text="00:00", 
                             font=("Arial", 48, "bold"),
                             fg="green", bg="white")
        time_label.pack(pady=(20, 0))
        
        # Zapisz referencje w oknie
        window.time_label = time_label
        
        # Dodaj do listy okien
        self.participant_windows.append(window)
        
        # Obsługa zamknięcia okna
        window.protocol("WM_DELETE_WINDOW", 
                       lambda: self.close_participant_window(window))
        
        return window
    
    def close_participant_window(self, window):
        """Zamyka okno uczestników"""
        if window in self.participant_windows:
            self.participant_windows.remove(window)
        try:
            window.destroy()
        except:
            pass
    
    def close_all_participant_windows(self):
        """Zamyka wszystkie okna uczestników"""
        for window in self.participant_windows[:]:
            self.close_participant_window(window)
    
    def set_duration(self):
        """Ustawia czas trwania przerwy"""
        try:
            duration = int(self.duration_entry.get())
            if duration > 0:
                self.break_duration = duration
                messagebox.showinfo("Sukces", f"Czas przerwy ustawiony na {duration} minut")
            else:
                messagebox.showerror("Błąd", "Czas przerwy musi być większy od 0")
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź prawidłową liczbę minut")
    
    def on_duration_change(self, selected_value):
        """Obsługuje zmianę w liście rozwijanej"""
        duration = int(selected_value)
        self.break_duration = duration
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, str(duration))
        messagebox.showinfo("Sukces", f"Czas przerwy ustawiony na {duration} minut")
    
    def start_break(self):
        """Uruchamia przerwę"""
        if not self.is_running:
            self.remaining_time = self.break_duration * 60
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Usuń komunikaty końcowe z okien uczestników
            for window in self.participant_windows:
                try:
                    if hasattr(window, 'end_message_label'):
                        window.end_message_label.destroy()
                        delattr(window, 'end_message_label')
                except:
                    pass
            
            self.update_timer()
    
    def stop_break(self):
        """Zatrzymuje przerwę"""
        if self.is_running:
            self.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
    
    def reset_break(self):
        """Resetuje przerwę"""
        self.is_running = False
        self.remaining_time = 0
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.time_label.config(text="00:00")
        
        # Aktualizuj wszystkie okna uczestników
        for window in self.participant_windows:
            try:
                if hasattr(window, 'time_label'):
                    window.time_label.config(text="00:00", fg="green")
                # Usuń komunikaty końcowe
                if hasattr(window, 'end_message_label'):
                    window.end_message_label.destroy()
                    delattr(window, 'end_message_label')
            except:
                pass
    
    def update_timer(self):
        """Aktualizuje wyświetlacz czasu"""
        if self.is_running and self.remaining_time > 0:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            
            # Aktualizuj wyświetlacz trenera
            self.time_label.config(text=time_str)
            
            # Aktualizuj wszystkie okna uczestników
            for window in self.participant_windows:
                try:
                    if hasattr(window, 'time_label'):
                        window.time_label.config(text=time_str)
                        
                        # Zmiana koloru na podstawie pozostałego czasu
                        total_time = self.break_duration * 60
                        if self.remaining_time <= (total_time * 0.1):  # ostatnie 10% - czerwony
                            window.time_label.config(fg="red")
                        elif self.remaining_time <= (total_time * 0.5):  # połowa czasu - żółty
                            window.time_label.config(fg="orange")
                        else:  # początek - zielony
                            window.time_label.config(fg="green")
                except:
                    pass
            
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
            
        elif self.is_running and self.remaining_time <= 0:
            # Przerwa się skończyła
            self.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
            # Aktualizuj wszystkie okna uczestników
            for window in self.participant_windows:
                try:
                    if hasattr(window, 'time_label'):
                        window.time_label.config(text="00:00", fg="red")
                        # Dodaj komunikat końcowy
                        if hasattr(window, 'end_message_label'):
                            window.end_message_label.destroy()
                        end_message = tk.Label(window, text="Zapraszamy na dalszą część szkolenia", 
                                             font=("Arial", 14, "bold"), fg="darkgreen", bg="white")
                        end_message.pack(pady=(20, 0))
                        window.end_message_label = end_message
                except:
                    pass
            
            messagebox.showinfo("Koniec przerwy", "Czas przerwy dobiegł końca!")
    
    def open_participant_window(self):
        """Otwiera nowe okno dla uczestników"""
        self.create_participant_window()
    
    def show_about(self):
        """Pokazuje okno informacyjne o aplikacji"""
        about_text = """Zegar Przerw v2.0
        
Aplikacja do zarządzania przerwami podczas szkoleń.

Funkcje:
• Panel trenera z kontrolą czasu
• Okna dla uczestników z wyświetlaniem czasu
• System kolorów (zielony->żółty->czerwony)
• Automatyczne zakończenie przerwy
• Wielokrotne okna uczestników

Stworzone w Python Tkinter"""
        
        messagebox.showinfo("O aplikacji", about_text)
    
    def run(self):
        """Uruchamia aplikację"""
        # Obsługa zamknięcia aplikacji
        def on_closing():
            if self.is_running:
                if messagebox.askokcancel("Zamknij", "Przerwa nadal trwa. Czy na pewno chcesz zamknąć aplikację?"):
                    self.close_all_participant_windows()
                    self.root.destroy()
            else:
                self.close_all_participant_windows()
                self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()

def main():
    """Główna funkcja aplikacji"""
    # Usunięto styl - może powodować dodatkowe okno
    
    # Sprawdź czy już istnieje główne okno
    try:
        app = BreakTimerApp()
        app.run()
    except Exception as e:
        print(f"Błąd: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()