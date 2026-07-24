import sys
import os
import subprocess
import threading
import ctypes
import logging
import re
import tempfile
import zipfile
import winreg
from xml.etree import ElementTree as ET
from shutil import copyfileobj

try:
    import customtkinter as ctk
    from PIL import Image
except ImportError:
    print("Erro ao importar bibliotecas. Execute no terminal: pip install customtkinter pillow")
    sys.exit(1)

# --- CONFIGURAÇÃO DE LOGS ---
LOG_FILE = "easymsix_installer.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def elevate_privileges():
    logging.info("Solicitando elevação de privilégios (UAC)...")
    try:
        parametros = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, parametros, None, 1
        )
        sys.exit(0)
    except Exception as e:
        logging.error(f"Falha ao solicitar elevação de privilégios: {e}")

def get_app_details(caminho_arquivo):
    """Extrai o nome real e o ícone do aplicativo de forma aprofundada."""
    # Define o nome inicial como o nome limpo do próprio arquivo
    nome_base_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]
    app_name = nome_base_arquivo
    icon_dest_path = None

    if not os.path.exists(caminho_arquivo) or not zipfile.is_zipfile(caminho_arquivo):
        return app_name, icon_dest_path

    temp_dir = tempfile.gettempdir()

    try:
        with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            
            # Normalizar caminhos dos arquivos dentro do ZIP para letras minúsculas
            file_list_lower = {f.lower().replace('\\', '/'): f for f in file_list}

            manifest_file = None
            for f in file_list:
                if f.lower().endswith('appxmanifest.xml'):
                    manifest_file = f
                    break

            if manifest_file:
                manifest_data = zip_ref.read(manifest_file)
                root = ET.fromstring(manifest_data)

                # 1. Tentar obter o Nome do Aplicativo
                for elem in root.iter():
                    # Procura por DisplayName no manifesto
                    if elem.tag.endswith('DisplayName') and elem.text:
                        texto = elem.text.strip()
                        # Se não for uma variável de recurso (ex: ms-resource: ou $Resources:)
                        if not texto.startswith('$') and not texto.startswith('ms-resource:'):
                            app_name = texto
                            break

                # 2. Tentar obter a Tag de Logotipo do Manifesto
                possible_logo_paths = []
                for elem in root.iter():
                    if elem.tag.endswith('VisualElements') or elem.tag.endswith('Properties'):
                        for attr, val in elem.attrib.items():
                            if 'logo' in attr.lower() and val:
                                possible_logo_paths.append(val.replace('\\', '/'))

                # Busca imagens dentro do pacote
                target_file_in_zip = None

                # Tentar casar as rotas encontradas no manifesto
                for logo_path in possible_logo_paths:
                    base_logo_name = os.path.splitext(os.path.basename(logo_path))[0].lower()
                    for norm_path, orig_path in file_list_lower.items():
                        if base_logo_name in norm_path and norm_path.endswith(('.png', '.jpg')):
                            target_file_in_zip = orig_path
                            break
                    if target_file_in_zip:
                        break

                # Fallback: Se não achou pelo manifesto, procura qualquer imagem com 'logo' ou 'icon' na pasta Assets/
                if not target_file_in_zip:
                    for norm_path, orig_path in file_list_lower.items():
                        if ('logo' in norm_path or 'icon' in norm_path or 'appicon' in norm_path) and norm_path.endswith(('.png', '.jpg')):
                            target_file_in_zip = orig_path
                            break

                # Extrai a imagem se tiver encontrado
                if target_file_in_zip:
                    icon_dest_path = os.path.join(temp_dir, f"easymsix_temp_{os.path.basename(target_file_in_zip)}")
                    with zip_ref.open(target_file_in_zip) as source, open(icon_dest_path, 'wb') as target:
                        copyfileobj(source, target)

    except Exception as e:
        logging.warning(f"Erro ao tentar extrair informações do arquivo MSIX: {e}")

    return app_name, icon_dest_path

def register_context_menu():
    exe_path = sys.executable
    extensions = ['.msix', '.msixbundle', '.appx', '.appxbundle']

    try:
        for ext in extensions:
            class_name = f"EasyMSIX{ext}"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{ext}") as key:
                winreg.SetValue(key, "", winreg.REG_SZ, class_name)

            key_path = f"Software\\Classes\\{class_name}\\shell\\Instalar com EasyMSIX"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, "Instalar com EasyMSIX")
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f'"{exe_path}"')

            cmd_path = f"{key_path}\\command"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')

        logging.info("Menu de contexto registrado com sucesso.")
        return True
    except Exception as e:
        logging.error(f"Erro ao registrar menu de contexto: {e}")
        return False

def executar_instalacao(caminho_arquivo, janela, barra_progresso, label_status, label_porcentagem):
    logging.info(f"Iniciando instalação do arquivo: {caminho_arquivo}")

    caminho_limpo = caminho_arquivo.replace("'", "''")
    comando = f"Add-AppxPackage -Path '{caminho_limpo}' -Verbose"

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        processo = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", comando],
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='cp850',
            bufsize=1
        )

        padrao_porcentagem = re.compile(r'(\d+)%')

        while True:
            linha = processo.stdout.readline()
            if not linha and processo.poll() is not None:
                break

            if linha:
                match = padrao_porcentagem.search(linha)
                if match:
                    porcentagem = int(match.group(1))
                    val_float = porcentagem / 100.0
                    janela.after(0, lambda v=val_float, p=porcentagem: [
                        barra_progresso.set(v),
                        label_porcentagem.configure(text=f"{p}%")
                    ])

        _, stderr = processo.communicate()

        if processo.returncode == 0:
            logging.info("Instalação concluída com sucesso!")
            janela.after(0, lambda: [
                barra_progresso.set(1.0),
                label_porcentagem.configure(text="100%"),
                label_status.configure(text="Instalação concluída com sucesso!"),
                exibir_mensagem(janela, "Sucesso", "O pacote foi instalado com sucesso!", "info")
            ])
        else:
            erro_msg = stderr.strip() if stderr else "Erro desconhecido."
            logging.error(f"Erro na instalação: {erro_msg}")
            janela.after(0, lambda: [
                label_status.configure(text="Erro na instalação."),
                exibir_mensagem(janela, "Erro de Instalação", f"Ocorreu um erro:\n{erro_msg}", "error")
            ])

    except Exception as e:
        logging.error(f"Falha de execução: {str(e)}")
        janela.after(0, lambda: [
            label_status.configure(text="Erro ao executar."),
            exibir_mensagem(janela, "Erro", f"Falha ao iniciar o processo:\n{str(e)}", "error")
        ])

def exibir_mensagem(janela, titulo, mensagem, tipo):
    icon = "info" if tipo == "info" else "error"
    janela.tk.call('tk_messageBox', '-type', 'ok', '-icon', icon, '-title', titulo, '-message', mensagem)
    janela.destroy()

def iniciar_interface():
    logging.info("EasyMSIX iniciado.")

    if len(sys.argv) > 1 and sys.argv[1] == "--register":
        if register_context_menu():
            root = ctk.CTk()
            root.withdraw()
            root.tk.call('tk_messageBox', '-type', 'ok', '-icon', 'info', '-title', 'EasyMSIX', '-message', 'Menu de contexto do botão direito registrado com sucesso!')
        sys.exit()

    if len(sys.argv) < 2:
        logging.warning("Nenhum arquivo de pacote foi informado.")
        root = ctk.CTk()
        root.withdraw()
        resposta = root.tk.call('tk_messageBox', '-type', 'yesno', '-icon', 'question', '-title', 'EasyMSIX', 
                                '-message', 'Nenhum pacote selecionado.\n\nDeseja adicionar a opção "Instalar com EasyMSIX" no menu do botão direito do Windows?')
        if resposta == 'yes':
            register_context_menu()
            root.tk.call('tk_messageBox', '-type', 'ok', '-icon', 'info', '-title', 'EasyMSIX', '-message', 'Opção adicionada com sucesso ao menu do botão direito!')
        sys.exit()

    if not is_admin():
        elevate_privileges()

    caminho_arquivo = sys.argv[1]

    # Extrai o nome e o ícone
    app_name, app_icon_path = get_app_details(caminho_arquivo)

    janela = ctk.CTk()
    janela.title("EasyMSIX")

    caminho_icone = resource_path("logo.ico")
    if os.path.exists(caminho_icone):
        janela.iconbitmap(caminho_icone)

    janela.geometry("420x240")
    janela.resizable(False, False)

    screen_w = janela.winfo_screenwidth()
    screen_h = janela.winfo_screenheight()
    x = int((screen_w / 2) - (420 / 2))
    y = int((screen_h / 2) - (240 / 2))
    janela.geometry(f"+{x}+{y}")

    # Exibe o ícone se encontrou
    if app_icon_path and os.path.exists(app_icon_path):
        try:
            img_pil = Image.open(app_icon_path)
            app_icon_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(48, 48))
            lbl_icon = ctk.CTkLabel(janela, image=app_icon_img, text="")
            lbl_icon.pack(pady=(15, 0))
        except Exception as e:
            logging.warning(f"Não foi possível carregar a imagem do ícone: {e}")

    # Exibe o nome (se não achar no manifesto, usa o nome do arquivo .msix)
    label_app_name = ctk.CTkLabel(janela, text=app_name, font=("Arial", 16, "bold"))
    label_app_name.pack(pady=(10, 2))

    label_status = ctk.CTkLabel(janela, text="Instalando, aguarde...", font=("Arial", 12))
    label_status.pack(pady=(2, 5))

    label_porcentagem = ctk.CTkLabel(janela, text="0%", font=("Arial", 11, "bold"))
    label_porcentagem.pack(pady=(0, 5))

    barra_progresso = ctk.CTkProgressBar(janela, orientation="horizontal", width=340, mode="determinate")
    barra_progresso.pack(pady=5)
    barra_progresso.set(0)

    thread = threading.Thread(
        target=executar_instalacao,
        args=(caminho_arquivo, janela, barra_progresso, label_status, label_porcentagem),
        daemon=True
    )
    thread.start()

    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface()