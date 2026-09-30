# EasyMSIX

O **EasyMSIX** é uma utilidade leve para Windows desenvolvida para simplificar a instalação de pacotes `.msix`, `.msixbundle`, `.appx` e `.appxbundle`. Criado com Python e CustomTkinter, oferece uma interface gráfica intuitiva com acompanhamento do progresso em tempo real, extração automática de detalhes do pacote e associação de ficheiros no sistema.

---

## Funcionalidades

- **Instalação com Duplo Clique**: Dá um duplo clique em qualquer ficheiro `.msix` ou `.appx` para o instalar instantaneamente.
- **Integração no Menu de Contexto**: Adiciona a opção *"Instalar com EasyMSIX"* ao menu do botão direito no Explorador de Ficheiros do Windows.
- **Extração de Metadados**: Extrai automaticamente o nome da aplicação e o ícone diretamente do manifesto do pacote, sem necessidade de extrair ficheiros temporários para o disco.
- **Progresso em Tempo Real**: Exibe a percentagem precisa do progresso do processo de instalação via PowerShell.
- **Interface Moderna**: Desenvolvida com `CustomTkinter`, adaptando-se automaticamente ao tema claro ou escuro do Windows.
- **Elevação de Privilégios (UAC)**: Solicita permissões de administrador apenas quando estritamente necessário.

---

## Como Começar

### Pré-requisitos

- **Windows 10/11**
- **Python 3.8+** (caso pretendas executar a partir do código-fonte)

### Dependências

Para executar o projeto a partir do código-fonte, instala as bibliotecas necessárias:

```bash
pip install customtkinter pillow
