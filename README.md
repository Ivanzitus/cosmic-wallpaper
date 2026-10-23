# COSMIC Wallpaper Manager (Flatpak)

Gerenciador de papéis de parede estáticos e animados para o ambiente desktop **COSMIC** (Pop!_OS / Wayland).

## 🚀 Funcionalidades

- **Papéis de Parede Animados**: Suporte a vídeos MP4, WebM e GIFs na área de trabalho principal usando `mpvpaper`.
- **Sincronização da Tela de Descanso / Bloqueio**: Extração automática do primeiro frame via `ffmpeg` para aplicação estática na tela de bloqueio (`cosmic-greeter`).
- **Papéis de Parede Estáticos**: Configuração direta no backend `cosmic-bg` (formato RON).
- **Interface GTK4/Libadwaita**: Aplicação moderna integrada ao visual do Pop!_OS.

## 📁 Estrutura do Repositório

```text
.
├── com.github.cosmic_wallpaper_manager.yml  # Manifesto de compilação Flatpak
├── README.md                                # Documentação do projeto
├── .gitignore                               # Arquivos ignorados pelo Git
└── src/
    ├── main.py                              # Aplicação principal (GTK4 / Python)
    └── com.github.cosmic_wallpaper_manager.desktop
```

## 🛠️ Como Compilar e Instalar

### Pré-requisitos
Instale o `flatpak` e o `flatpak-builder` no seu sistema:

```bash
sudo apt update
sudo apt install flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.freedesktop.Platform//23.08 org.freedesktop.Sdk//23.08
```

### Compilação e Instalação Local

```bash
flatpak-builder --force-clean build-dir com.github.cosmic_wallpaper_manager.yml
flatpak-builder --user --install build-dir com.github.cosmic_wallpaper_manager.yml
```

### Executando

```bash
flatpak run com.github.cosmic_wallpaper_manager
```

## 📄 Licença

MIT License.
