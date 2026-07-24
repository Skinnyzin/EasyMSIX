# EasyMSIX

Uma ferramenta leve e intuitiva para instalação direta de aplicativos nos formatos **.msix**, **.msixbundle** e **.appx** no Windows, sem exibição de janelas de terminal.

---

## Objetivo

A instalação manual de pacotes locais no Windows geralmente requer a abertura do terminal ou a execução manual de comandos no PowerShell. 

O **EasyMSIX** simplifica esse processo:
- **Instalação via duplo clique:** Basta dar dois cliques no arquivo `.msix`, `.msixbundle` ou `.appx` que automaticamente irá instalar.
- **Interface Gráfica Simples:** Exibe uma janela minimalista com status e barra de progresso.

---

## Requisitos

- Windows 10 ou posterior, python 3,8+ para desenvolvimento ou compilação

---

## Configuração

Para que o programa seja executado ao dar dois cliques nos arquivos:
Clique com o botão direito em qualquer arquivo .msix, .msixbundle ou .appx.

**1 -** Selecione Abrir com > Escolher outro aplicativo.

**2 -** Clique em Escolher um aplicativo no seu computador (ou Procurar outro aplicativo neste PC).

**3 -** Navegue até a pasta onde está o programa e selecione-o.

**4 -** Marque a opção "Sempre usar este aplicativo para abrir arquivos [extensão]".
