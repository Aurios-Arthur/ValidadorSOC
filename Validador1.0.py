import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from bs4 import BeautifulSoup
from unidecode import unidecode

# Variável global para armazenar o widget arquivo_label
arquivo_label = None

# Funções de processamento (ler, normalizar, separar riscos, etc)
def ler_arquivo_html(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        print("Erro de codificação com UTF-8. Tentando com ISO-8859-1...")
        with open(caminho_arquivo, 'r', encoding='ISO-8859-1') as file:
            return file.read()

def normalizar_texto(texto):
    texto_normalizado = unidecode(texto.strip().lower())
    return texto_normalizado.rstrip('.').strip()

def separar_riscos(risco_string):
    riscos = [normalizar_texto(risco) for risco in risco_string.split(',') if risco.strip()]
    return riscos

def buscar_riscos(html):
    soup = BeautifulSoup(html, 'lxml')

    # Função para encontrar o risco em um dado texto
    def encontrar_riscos(tipo_risco):
        td_risco = soup.find('td', string=lambda text: text and tipo_risco in text.lower())
        if td_risco:
            td_riscos = td_risco.find_next('td')
            if td_riscos:
                return separar_riscos(td_riscos.get_text())
        return []

    # Buscar os riscos
    riscos_fisicos = encontrar_riscos("físicos")
    riscos_quimicos = encontrar_riscos("químicos")
    riscos_biologicos = encontrar_riscos("biológicos")
    riscos_ergonomicos = encontrar_riscos("ergonômicos")

    return riscos_fisicos, riscos_quimicos, riscos_biologicos, riscos_ergonomicos

# Função de comparar riscos
def comparar_riscos(riscos_encontrados, riscos_usuario):
    riscos_encontrados_set = set(riscos_encontrados)
    riscos_usuario_set = set(riscos_usuario)

    riscos_faltando = riscos_encontrados_set - riscos_usuario_set
    riscos_extra = riscos_usuario_set - riscos_encontrados_set

    return riscos_faltando, riscos_extra

# Função para abrir seletor de arquivos
def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
    if caminho_arquivo:
        arquivo_label.config(text=caminho_arquivo)  # Exibe o caminho do arquivo selecionado
        return caminho_arquivo
    return None

# Função para iniciar a análise de riscos
def iniciar_analise():
    caminho_arquivo = arquivo_label.cget("text")
    if not caminho_arquivo:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo HTML primeiro!")
        return

    html = ler_arquivo_html(caminho_arquivo)
    riscos_fisicos, riscos_quimicos, riscos_biologicos, riscos_ergonomicos = buscar_riscos(html)

    # Exibir todos os riscos em uma única janela organizada
    exibir_todos_os_riscos(riscos_fisicos, riscos_quimicos, riscos_biologicos, riscos_ergonomicos)

# Função para exibir todos os riscos em uma única janela
def exibir_todos_os_riscos(riscos_fisicos, riscos_quimicos, riscos_biologicos, riscos_ergonomicos):
    janela_riscos = tk.Toplevel()
    janela_riscos.title("Todos os Riscos Encontrados")

    # Alterando a cor de fundo da janela e fontes
    janela_riscos.configure(bg="#f4f4f9")  # Cor de fundo suave
    cor_fonte = "#333333"  # Cor das fontes
    cor_botao = "#4CAF50"  # Cor dos botões

    # Título geral da janela
    tk.Label(janela_riscos, text="Análise de Riscos Encontrados", font=("Arial", 14, "bold"), fg=cor_fonte, bg="#f4f4f9").pack(pady=10)

    # Função auxiliar para criar uma seção de risco
    def criar_secao_risco(titulo, riscos):
        frame = tk.Frame(janela_riscos, bg="#f4f4f9")
        frame.pack(pady=5, padx=20, fill="both", expand=True)
        
        tk.Label(frame, text=f"{titulo} encontrados:", font=("Arial", 12, "bold"), fg=cor_fonte, bg="#f4f4f9").pack(anchor="w", pady=5)
        
        if riscos:
            for risco in riscos:
                tk.Label(frame, text=f"- {risco}", font=("Arial", 10), fg=cor_fonte, bg="#f4f4f9").pack(anchor="w", pady=2)
        else:
            tk.Label(frame, text="Nenhum risco encontrado", font=("Arial", 10), italic=True, fg="#888888", bg="#f4f4f9").pack(anchor="w", pady=2)

    # Criar seções para cada tipo de risco
    criar_secao_risco("Riscos Físicos", riscos_fisicos)
    criar_secao_risco("Riscos Químicos", riscos_quimicos)
    criar_secao_risco("Riscos Biológicos", riscos_biologicos)
    criar_secao_risco("Riscos Ergonômicos", riscos_ergonomicos)

    # Adicionar um campo para o usuário digitar os riscos corretos
    tk.Label(janela_riscos, text="Digite os riscos corretos separados por vírgula:", font=("Arial", 12), fg=cor_fonte, bg="#f4f4f9").pack(pady=10)
    riscos_usuario = tk.Entry(janela_riscos, width=60, font=("Arial", 12))
    riscos_usuario.pack(pady=10)

    # Função para comparar os riscos
    def comparar():
        riscos_usuario_texto = riscos_usuario.get()
        riscos_usuario_lista = [normalizar_texto(r.strip()) for r in riscos_usuario_texto.split(',')]
        riscos_faltando, riscos_extra = comparar_riscos(riscos_fisicos + riscos_quimicos + riscos_biologicos + riscos_ergonomicos, riscos_usuario_lista)

        resultado = ""
        if riscos_faltando:
            resultado += "Riscos faltando:\n" + "\n".join([f"- {r}" for r in riscos_faltando]) + "\n"
        if riscos_extra:
            resultado += "Riscos extras informados:\n" + "\n".join([f"- {r}" for r in riscos_extra]) + "\n"
        
        if not resultado:
            resultado = "Tudo certo! Os riscos estão corretos."
        
        messagebox.showinfo("Resultado da Comparação", resultado)

    # Botão para iniciar a comparação dos riscos
    tk.Button(janela_riscos, text="Comparar Riscos", command=comparar, bg=cor_botao, fg="white", font=("Arial", 12, "bold")).pack(pady=15)

# Função para iniciar a interface principal
def iniciar_interface():
    global arquivo_label  # Tornando a variável global acessível na função

    janela = tk.Tk()
    janela.title("Validador de Riscos")

    # Alterando a cor de fundo da janela principal
    janela.configure(bg="#f4f4f9")

    # Layout aprimorado
    tk.Label(janela, text="Selecione um arquivo HTML para análise:", font=("Arial", 12, "bold"), fg="#333333", bg="#f4f4f9").pack(pady=10)
    
    arquivo_label = tk.Label(janela, text="Nenhum arquivo selecionado", fg="blue", cursor="hand2", font=("Arial", 10), bg="#f4f4f9")
    arquivo_label.pack(pady=10)
    arquivo_label.bind("<Button-1>", lambda event: selecionar_arquivo())

    tk.Button(janela, text="Iniciar Análise de Riscos", command=iniciar_analise, bg="#008CBA", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

    janela.geometry("500x300")
    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface()
