# gui.py

import json
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from language import LANGUAGES
from validator import SoundValidator
from exporter import SoundpackExporter
from utils import resource_path


class SoundpackBuilderApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==================================================
        # CONFIGURACIÓN VENTANA
        # ==================================================

        self.title("TICO Soundpack Builder")
        self.iconbitmap(resource_path("assets/tsb.ico"))
        self.geometry("1000x800")
        self.resizable(False, False)

        # ==================================================
        # ESTADO
        # ==================================================

        self.current_language = "es"

        self.formats = self.load_formats()

        self.sound_files = {}
        self.select_buttons = {}
        self.file_labels = {}

        # ==================================================
        # UI
        # ==================================================

        self.create_widgets()

    # ==================================================
    # DATOS
    # ==================================================

    def load_formats(self):

        with open(
            resource_path("assets/formats.json"),
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def change_language(self, language):

        language_map = {
            "Español": "es",
            "English": "en",
            "Português": "pt"
        }

        self.current_language = language_map[language]

        lang = LANGUAGES[self.current_language]

        # ------------------------------
        # Header
        # ------------------------------

        self.language_label.configure(
            text=lang["language"]
        )

        self.title_label.configure(
            text=lang["title"]
        )

        # ------------------------------
        # Nombre del paquete
        # ------------------------------

        self.pack_name_label.configure(
            text=lang["pack_name"]
        )

        # ------------------------------
        # Botón exportar
        # ------------------------------

        self.export_button.configure(
            text=lang["create_pack"]
        )

        # ------------------------------
        # Botones de archivos
        # ------------------------------

        for sound_name, button in self.select_buttons.items():

            if self.sound_files[sound_name] is None:

                button.configure(
                    text=lang["select_file"]
                )

            else:

                button.configure(
                    text=lang["change_file"]
                )

        for sound_name, label in self.file_labels.items():

            filepath = self.sound_files[sound_name]

            if filepath is None:

                label.configure(
                    text=f"❌ {lang['status_missing']}"
                )

            else:

                filename = Path(filepath).name

                label.configure(
                    text=f"✅ {lang['status_selected']} - {filename}"
                )
    # ==================================================
    # WIDGETS
    # ==================================================

    def create_widgets(self):

        self.create_header()
        self.create_pack_name()
        self.create_sound_rows()
        self.create_export_button()

    # ==================================================
    # HEADER
    # ==================================================

    def create_header(self):

        header_frame = ctk.CTkFrame(self)

        header_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # ------------------------------
        # Lado izquierdo
        # ------------------------------

        left_frame = ctk.CTkFrame(
            header_frame,
            fg_color="transparent"
        )

        left_frame.pack(
            side="left",
            padx=10,
            pady=10
        )

        image = Image.open(resource_path("assets/tico_logo.png"))

        logo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(200, 100)
        )

        self.logo_label = ctk.CTkLabel(
            left_frame,
            image=logo,
            text=""
        )

        self.logo_label.pack(
            anchor="w"
        )

        self.title_label = ctk.CTkLabel(
            left_frame,
            text=LANGUAGES[self.current_language]["title"],
            font=("Arial", 24, "bold")
        )

        self.title_label.pack(
            anchor="w",
            pady=(10, 0)
        )

        # ------------------------------
        # Lado derecho
        # ------------------------------

        right_frame = ctk.CTkFrame(
            header_frame,
            fg_color="transparent"
        )

        right_frame.pack(
            side="right",
            padx=10
        )

        self.language_label = ctk.CTkLabel(
            right_frame,
            text=LANGUAGES[self.current_language]["language"]
        )

        self.language_label.pack(
            pady=(10, 5)
        )

        self.language_menu = ctk.CTkOptionMenu(
                right_frame,
                values=[
                    "Español",
                    "English",
                    "Português"
                ],
                command=self.change_language
            )

        self.language_menu.pack()

    # ==================================================
    # NOMBRE DEL PAQUETE
    # ==================================================

    def create_pack_name(self):

        frame = ctk.CTkFrame(self)

        frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.pack_name_label = ctk.CTkLabel(
            frame,
            text=LANGUAGES[self.current_language]["pack_name"]
        )

        self.pack_name_label.pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        self.pack_name_entry = ctk.CTkEntry(
            frame
        )

        self.pack_name_entry.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

    # ==================================================
    # SONIDOS
    # ==================================================

    def create_sound_rows(self):

        self.sounds_frame = ctk.CTkFrame(self)

        self.sounds_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        for sound_name in self.formats:

            self.sound_files[sound_name] = None

            row = ctk.CTkFrame(self.sounds_frame)

            row.pack(
                fill="x",
                pady=4,
                padx=5
            )

            # ----------------------------------
            # Nombre
            # ----------------------------------

            name_label = ctk.CTkLabel(
                row,
                text=sound_name,
                width=220,
                anchor="w"
            )

            name_label.pack(
                side="left",
                padx=10
            )

            # ----------------------------------
            # Botón
            # ----------------------------------

            select_button = ctk.CTkButton(
                row,
                text=LANGUAGES[self.current_language]["select_file"],
                width=170,
                command=lambda name=sound_name:
                self.select_file(name)
            )

            select_button.pack(
                side="left",
                padx=10
            )

            # ----------------------------------
            # Estado / archivo
            # ----------------------------------

            file_label = ctk.CTkLabel(
                row,
                text=f"❌ {LANGUAGES[self.current_language]['status_missing']}",
                anchor="w"
            )

            file_label.pack(
                side="left",
                padx=15
            )

            self.select_buttons[sound_name] = select_button
            self.file_labels[sound_name] = file_label

    # ==================================================
    # SELECCIÓN DE ARCHIVOS
    # ==================================================

    def select_file(self, sound_name):

        filepath = filedialog.askopenfilename()

        if not filepath:
            return

        expected_extension = self.formats[sound_name]

        if not SoundValidator.validate_extension(
            filepath,
            expected_extension
        ):

            messagebox.showerror(
                LANGUAGES[self.current_language]["validation_error"],
                LANGUAGES[self.current_language]["invalid_file"]
            )

            return

        self.sound_files[sound_name] = filepath

        filename = Path(filepath).name

        self.file_labels[sound_name].configure(
            text=f"✅ {LANGUAGES[self.current_language]['status_selected']} - {filename}"
        )

        self.select_buttons[sound_name].configure(
            text=LANGUAGES[self.current_language]["change_file"]
        )

    # ==================================================
    # EXPORTAR
    # ==================================================

    def create_soundpack(self):

        # ----------------------------------
        # Validar nombre
        # ----------------------------------

        soundpack_name = (
            self.pack_name_entry.get().strip()
        )

        if not soundpack_name:

            messagebox.showerror(
                LANGUAGES[self.current_language]["validation_error"],
                LANGUAGES[self.current_language]["empty_name"]
            )

            return

        # ----------------------------------
        # Validar archivos
        # ----------------------------------

        missing_sounds = []

        for sound_name, filepath in self.sound_files.items():

            if filepath is None:

                missing_sounds.append(
                    sound_name
                )

        if missing_sounds:

            messagebox.showerror(
                LANGUAGES[self.current_language]["validation_error"],
                LANGUAGES[self.current_language]["missing_files"]
            )

            return

        # ----------------------------------
        # Elegir carpeta destino
        # ----------------------------------

        destination_folder = (
            filedialog.askdirectory()
        )

        if not destination_folder:

            return

        # ----------------------------------
        # Exportar
        # ----------------------------------

        try:

            soundpack_path = (
                SoundpackExporter.create_soundpack(
                    destination_folder,
                    soundpack_name,
                    self.sound_files
                )
            )

            SoundpackExporter.create_zip(
                soundpack_path
            )

            messagebox.showinfo(
                LANGUAGES[self.current_language]["success"],
                LANGUAGES[self.current_language]["export_success"]
            )

        except Exception as error:

            messagebox.showerror(
                LANGUAGES[self.current_language]["export_error"],
                str(error)
            )

    def create_export_button(self):

        self.export_button = ctk.CTkButton(
            self,
            text=LANGUAGES[self.current_language]["create_pack"],
            height=40,
            command=self.create_soundpack
            )

        self.export_button.pack(
            pady=20
        )