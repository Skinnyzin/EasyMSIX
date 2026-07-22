import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox

def executar_instalacao(caminho_arquivo, janela, barra_progresso, label_status):
    # Comando do PowerShell montado com o caminho dinâmico
    comando = f'Add-AppxPackage -Path "{caminho_arquivo}"'
    
    # Flags para ocultar a janela do prompt/PowerShell no Windows
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    try:
        # Inicia o processo em segundo plano (totalmente oculto)
        processo = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", comando],
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguarda a finalização do processo
        stdout, stderr = processo.communicate()
        
        # Para a animação da barra
        barra_progresso.stop()
        
        if processo.returncode == 0:
            label_status.config(text="Instalação concluída com sucesso!")
            messagebox.showinfo("Sucesso", "O pacote foi instalado com sucesso!")
        else:
            label_status.config(text="Erro na instalação.")
            messagebox.showerror("Erro de Instalação", f"Ocorreu um erro:\n{stderr.strip()}")
            
    except Exception as e:
        barra_progresso.stop()
        label_status.config(text="Erro ao executar o instalador.")
        messagebox.showerror("Erro", f"Falha ao iniciar o processo:\n{str(e)}")
    
    finally:
        # Fecha a janela após a conclusão
        janela.destroy()

def iniciar_interface():
    # Verifica se algum arquivo foi passado via linha de comando
    if len(sys.argv) < 2:
        # Se nenhum arquivo for passado, encerra (ou exibe um aviso)
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Aviso", "Nenhum arquivo de pacote foi selecionado.")
        sys.exit()

    caminho_arquivo = sys.argv[1]

    # Configuração da janela do Tkinter
    janela = tk.Tk()
    janela.title("Instalador de Pacotes")
    janela.geometry("380x130")
    janela.resizable(False, False)
    
    # Centraliza a janela na tela
    janela.eval('tk::PlaceWindow . center')

    # Rótulo de texto
    label_status = tk.Label(janela, text="Instalando, aguarde...", font=("Arial", 11))
    label_status.pack(pady=(20, 10))

    # Barra de progresso (modo indeterminado para animação contínua)
    barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=300, mode="indeterminate")
    barra_progresso.pack(pady=5)
    barra_progresso.start(12)  # Velocidade da animação

    # Executa a instalação em uma Thread separada para não travar a janela
    thread = threading.Thread(
        target=executar_instalacao, 
        args=(caminho_arquivo, janela, barra_progresso, label_status)
    )
    thread.daemon = True
    thread.start()

    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface()