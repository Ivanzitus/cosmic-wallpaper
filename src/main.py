#!/usr/bin/env python3
import os
import subprocess
import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

CONFIG_DIR = os.path.expanduser("~/.config/cosmic/com.system76.CosmicBackground/v1")
CONFIG_FILE = os.path.join(CONFIG_DIR, "all")
LOCKSCREEN_FRAME = os.path.expanduser("~/.config/cosmic/lockscreen_frame.png")

class CosmicWallpaperApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.cosmic_wallpaper_manager",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = Adw.ApplicationWindow(application=self, title="COSMIC Wallpaper Manager")
        win.set_default_size(500, 400)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)

        header = Gtk.Label(label="Gerenciador de Wallpaper para Pop!_OS COSMIC")
        header.add_css_class("title-2")
        box.append(header)

        # Botão para Wallpaper Estático
        btn_static = Gtk.Button(label="Selecionar Imagem Estática (Desktop & Lock)")
        btn_static.connect("clicked", self.on_select_static)
        box.append(btn_static)

        # Botão para Wallpaper Animado
        btn_animated = Gtk.Button(label="Selecionar Vídeo Animado (Desktop & Frame Lock)")
        btn_animated.connect("clicked", self.on_select_animated)
        box.append(btn_animated)

        # Botão de Parar Animação
        btn_stop = Gtk.Button(label="Parar Wallpaper Animado")
        btn_stop.connect("clicked", self.stop_animated)
        box.append(btn_stop)

        win.set_content(box)
        win.present()

    def set_cosmic_static_background(self, image_path):
        """Atualiza o arquivo de configuração RON do cosmic-bg"""
        os.makedirs(CONFIG_DIR, exist_ok=True)
        ron_content = f"""(
    output: "all",
    filter_by_theme: false,
    rotation_frequency: 0,
    background: Image("{image_path}"),
)"""
        with open(CONFIG_FILE, "w") as f:
            f.write(ron_content)

    def on_select_static(self, button):
        dialog = Gtk.FileChooserNative.new(
            "Escolha uma Imagem", None,
            Gtk.FileChooserAction.OPEN, "Abrir", "Cancelar"
        )
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Imagens")
        filter_img.add_mime_type("image/jpeg")
        filter_img.add_mime_type("image/png")
        filter_img.add_mime_type("image/webp")
        dialog.add_filter(filter_img)

        def on_response(dialog, response):
            if response == Gtk.ResponseType.ACCEPT:
                file_path = dialog.get_file().get_path()
                self.stop_animated(None)
                self.set_cosmic_static_background(file_path)
            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.show()

    def on_select_animated(self, button):
        dialog = Gtk.FileChooserNative.new(
            "Escolha um Vídeo (MP4/WebM/GIF)", None,
            Gtk.FileChooserAction.OPEN, "Abrir", "Cancelar"
        )
        filter_vid = Gtk.FileFilter()
        filter_vid.set_name("Vídeos / Animações")
        filter_vid.add_mime_type("video/mp4")
        filter_vid.add_mime_type("video/webm")
        filter_vid.add_mime_type("image/gif")
        dialog.add_filter(filter_vid)

        def on_response(dialog, response):
            if response == Gtk.ResponseType.ACCEPT:
                video_path = dialog.get_file().get_path()
                
                # 1. Extrai o 1º frame para a Tela de Descanso / Bloqueio
                subprocess.run([
                    "ffmpeg", "-y", "-i", video_path,
                    "-vframes", "1", LOCKSCREEN_FRAME
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # 2. Define o frame estático no cosmic-bg (usado na Lock Screen)
                self.set_cosmic_static_background(LOCKSCREEN_FRAME)

                # 3. Executa o mpvpaper por cima para animar a Área de Trabalho Principal
                self.stop_animated(None)
                subprocess.Popen([
                    "mpvpaper", "-o", "no-audio --loop-playlist=inf",
                    "*", video_path
                ])

            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.show()

    def stop_animated(self, button):
        subprocess.run(["killall", "-9", "mpvpaper"], stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    app = CosmicWallpaperApp()
    app.run(sys.argv)
