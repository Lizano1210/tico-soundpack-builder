# gui.py

from PIL import Image, ImageTk
import sys
import json
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from language import LANGUAGES
from validator import SoundValidator
from exporter import SoundpackExporter
from utils import resource_path
import webbrowser

from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

from audio_preview import AudioPreview
from project_manager import ProjectManager
from drag_drop import DragDropManager

from utils import (
    resource_path,
    assign_file
)

APP_VERSION = "1.2.0"

class SoundpackBuilderApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==================================================
        # CONFIGURACIÓN VENTANA
        # ==================================================

        self.title("TICO Soundpack Builder")
        if sys.platform == "win32":
            self.iconbitmap(resource_path("assets/tsb.ico"))
        else:
            self.iconphoto(True, ImageTk.PhotoImage(Image.open(resource_path("assets/tico_logo.png"))))
        self.minsize(900, 700)
        self.resizable(True, True)
        from tkinterdnd2 import TkinterDnD

        self.TkdndVersion = TkinterDnD._require(self)

        print(
            f"TkDnD cargado: {self.TkdndVersion}"
        )

        # ==================================================
        # ESTADO
        # ==================================================

        self.current_language = "en"

        self.formats = self.load_formats()

        self.sound_files = {}
        self.audio_preview = AudioPreview()
        self.drag_drop = DragDropManager()
        self.play_buttons = {}
        self.stop_buttons = {}
        self.select_buttons = {}
        self.file_labels = {}
        self.logo_pil = Image.open(resource_path("assets/tico_logo.png"))

        # ==================================================
        # UI
        # ==================================================

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(
        self
    ):

        self.audio_preview.cleanup()

        self.destroy()

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

        """self.language_label.configure(
            text=lang["language"]
        )"""

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

        self.file_button.configure(
            text=lang["file_menu"]
        )

        self.help_button.configure(
            text=lang["help_menu"]
        )

    def handle_drop(
        self,
        sound_name,
        filepath
    ):

        assign_file(
            self,
            sound_name,
            filepath
        )

    def play_sound(
        self,
        sound_name
    ):

        filepath = self.sound_files.get(
            sound_name
        )

        if not filepath:
            return

        self.audio_preview.play(
            filepath
        )

    def stop_sound(
        self
    ):

        self.audio_preview.stop()

    def load_project_files(
        self,
        sound_files
    ):

        for (
            sound_name,
            filepath
        ) in sound_files.items():

            if not filepath:
                continue

            if not Path(filepath).exists():
                continue

            assign_file(
                self,
                sound_name,
                filepath
            )

    def open_project(
        self
    ):

        filepath = filedialog.askopenfilename(
            filetypes=[
                (
                    "TSB Project",
                    "*.tsbp"
                )
            ]
        )

        if not filepath:
            return

        project = (
            ProjectManager.load_project(
                filepath
            )
        )

        if project is None:

            messagebox.showerror(
                LANGUAGES[self.current_language]["error"],
                LANGUAGES[self.current_language]["project_load_error"]
            )

            return

        if not ProjectManager.validate_project(
            project
        ):

            messagebox.showerror(
                LANGUAGES[self.current_language]["error"],
                LANGUAGES[self.current_language]["invalid_project"]
            )

            return

        self.pack_name_entry.delete(
            0,
            "end"
        )

        self.pack_name_entry.insert(
            0,
            project["project_name"]
        )

        self.load_project_files(
            project["files"]
        )

        missing = (
            ProjectManager.get_missing_files(
                project["files"]
            )
        )

        if missing:

            messagebox.showwarning(
                LANGUAGES[self.current_language]["missing_files"],
                "\n".join(missing)
            )

    def save_project(
        self
    ):

        project_name = (
            self.pack_name_entry
            .get()
            .strip()
        )

        if not project_name:

            messagebox.showerror(
                LANGUAGES[self.current_language]["error"],
                LANGUAGES[self.current_language]["project_name"]
            )

            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".tsbp",
            filetypes=[
                (
                    "TSB Project",
                    "*.tsbp"
                )
            ]
        )

        if not filepath:
            return

        success = (
            ProjectManager.save_project(
                filepath,
                project_name,
                self.sound_files
            )
        )

        if success:

            messagebox.showinfo(
                LANGUAGES[self.current_language]["success"],
                LANGUAGES[self.current_language]["project_saved"]
            )
    # ==================================================
    # WIDGETS
    # ==================================================

    def create_widgets(self):

        self.create_top_bar()
        self.create_header()
        self.create_pack_name()
        self.create_sound_rows()
        self.create_footer()
        """self.header_frame
        self.pack_name_frame
        self.sounds_frame
        self.footer_frame"""

    def create_top_bar(self):

        self.top_bar = ctk.CTkFrame(
            self,
            height=40
        )

        self.top_bar.pack(
            fill="x",
            padx=20,
            pady=(10, 0)
        )

        self.file_button = ctk.CTkButton(
            self.top_bar,
            text=LANGUAGES[self.current_language]["file_menu"],
            width=80,
            command=self.show_file_menu
        )

        self.file_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.help_button = ctk.CTkButton(
            self.top_bar,
            text=LANGUAGES[self.current_language]["help_menu"],
            width=80,
            command=self.show_help_menu
        )

        self.help_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        
        # ------------------------------
        # Lado derecho
        # ------------------------------


        """self.language_label = ctk.CTkLabel(
            self.top_bar,
            text=LANGUAGES[self.current_language]["language"]
        )

        self.language_label.pack(
            side="right",
            pady=(10, 5),
            padx = 15
        )"""

        self.language_menu = ctk.CTkOptionMenu(
                self.top_bar,
                values=[
                    "English",
                    "Español",
                    "Português"
                ],
                command=self.change_language
            )

        self.language_menu.pack(
            side="right",
            padx=5,
            pady=5
        )

        self.small_logo = ctk.CTkImage(
            light_image=self.logo_pil,
            dark_image=self.logo_pil,
            size=(90, 45)
        )

        self.logo_label = ctk.CTkLabel(
            self.top_bar,
            text="",
            image=self.small_logo
        )

        self.logo_label.pack(
            side="right",
            padx=(0, 10),
            pady = 5
        )

    def show_file_menu(self):

        menu = tk.Menu(
            self,
            tearoff=0
        )

        menu.add_command(
            label=LANGUAGES[self.current_language]["new_project"],
            command=self.new_project
        )

        menu.add_command(
            label=LANGUAGES[self.current_language]["open_project"],
            command=self.open_project
        )

        menu.add_command(
            label=LANGUAGES[self.current_language]["save_project"],
            command=self.save_project
        )

        menu.add_separator()

        menu.add_command(
            label=LANGUAGES[self.current_language]["export_portable"],
            command=self.export_portable_project
        )

        menu.add_command(
            label=LANGUAGES[self.current_language]["import_portable"],
            command=self.import_portable_project
        )

        menu.add_separator()

        menu.add_command(
            label=LANGUAGES[self.current_language]["exit"],
            command=self.on_closing
        )

        menu.post(
            self.file_button.winfo_rootx(),
            self.file_button.winfo_rooty()
            + self.file_button.winfo_height()
        )
    
    def show_help_menu(self):
        menu = tk.Menu(
            self,
            tearoff=0
        )

        menu.add_command(
            label=LANGUAGES[self.current_language]["github"],
            command=self.open_github
        )

        menu.add_command(
            label=LANGUAGES[self.current_language]["install_guide"],
            command=self.show_install_guide
        )

        menu.add_separator()

        menu.add_command(
            label=LANGUAGES[self.current_language]["about"],
            command=self.show_about
        )

        menu.post(
            self.help_button.winfo_rootx(),
            self.help_button.winfo_rooty()
            + self.help_button.winfo_height()
        )

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
            pady= 5
        )

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

        self.sounds_frame = ctk.CTkScrollableFrame(self)

        self.sounds_frame.pack(
            fill="both",
            expand=True,
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

            play_button = ctk.CTkButton(
                    row,
                    text="▶",
                    width=40,
                    command=lambda s=sound_name:
                    self.play_sound(s)
                )

            play_button.pack(
                side="left",
                padx=5
            )

            stop_button = ctk.CTkButton(
                row,
                text="■",
                width=40,
                command=self.stop_sound
            )

            stop_button.pack(
                side="left",
                padx=5
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
            self.play_buttons[sound_name] = play_button
            self.stop_buttons[sound_name] = stop_button
            self.drag_drop.register_target(
                row,
                sound_name,
                self.handle_drop
            )
    # ==================================================
    # SELECCIÓN DE ARCHIVOS
    # ==================================================

    def select_file(
            self,
            sound_name
        ):

            filepath = filedialog.askopenfilename()

            if not filepath:
                return

            assign_file(
                self,
                sound_name,
                filepath
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

    def create_footer(self):
        self.footer_frame = ctk.CTkFrame(self)

        self.footer_frame.pack(
            fill="x",
            side="bottom",
            padx=20,
            pady=10
        )

        self.export_button = ctk.CTkButton(
            self.footer_frame,
            text=LANGUAGES[self.current_language]["create_pack"],
            height=40,
            command=self.create_soundpack
        )

        self.export_button.pack(
            pady=10
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

    def new_project(self):
        pass


    def export_portable_project(self):
        pass


    def import_portable_project(self):
        pass


    def open_github(self):
        webbrowser.open(
        "https://github.com/Lizano1210/tico-soundpack-builder"
    )
        


    def show_install_guide(self):
        guide_window = ctk.CTkToplevel(self)

        guide_window.title(
            LANGUAGES[self.current_language]["install_guide_title"]
        )

        guide_window.geometry("650x450")

        guide_window.transient(self)

        guide_window.grab_set()

        content_frame = ctk.CTkFrame(
            guide_window
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        guide_label = ctk.CTkLabel(
            content_frame,
            text=LANGUAGES[self.current_language]["install_guide_text"],
            justify="left",
            anchor="nw"
        )

        guide_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        logo_label = ctk.CTkLabel(
            content_frame,
            text="",
            image=self.small_logo
        )

        logo_label.pack(
            anchor="se",
            padx=10,
            pady=10
        )


    def show_about(self):
        about_window = ctk.CTkToplevel(self)

        about_window.title(
            LANGUAGES[self.current_language]["about_title"]
        )

        about_window.geometry("650x400")

        about_window.transient(self)

        about_window.grab_set()

        content_frame = ctk.CTkFrame(
            about_window
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        about_text = LANGUAGES[
            self.current_language
        ]["about_text"].format(
            version=APP_VERSION
        )

        about_label = ctk.CTkLabel(
            content_frame,
            text=about_text,
            justify="left",
            anchor="nw"
        )

        about_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        logo_label = ctk.CTkLabel(
            content_frame,
            text="",
            image=self.small_logo
        )

        logo_label.pack(
            anchor="se",
            padx=10,
            pady=10
        )