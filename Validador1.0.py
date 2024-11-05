from bs4 import BeautifulSoup
from unidecode import unidecode

def ler_arquivo_html(caminho_arquivo):
    # Tenta abrir o arquivo com codificação UTF-8
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        print("Erro de codificação com UTF-8. Tentando com ISO-8859-1...")
        # Se ocorrer um erro de codificação, tenta com ISO-8859-1 (latin1)
        with open(caminho_arquivo, 'r', encoding='ISO-8859-1') as file:
            return file.read()

def normalizar_texto(texto):
    # Remove acentuação, converte para minúsculas, remove espaços extras e pontuação indesejada
    texto_normalizado = unidecode(texto.strip().lower())
    # Remove pontos finais (ou outras pontuações) que podem aparecer no final
    return texto_normalizado.rstrip('.').strip()

def separar_riscos(risco_string):
    # Apenas separa por vírgula, sem dividir os riscos com "e"
    riscos = [normalizar_texto(risco) for risco in risco_string.split(',') if risco.strip()]
    return riscos

def buscar_td_com_riscos(html, risco_label):
    soup = BeautifulSoup(html, 'lxml')

    # Encontra o <td> que contém <span> com o nome do risco, como "Perigos / Fatores de Risco", "Físicos", "Químicos", etc.
    td_risco = soup.find('td', string=lambda text: text and risco_label in text)
    
    if not td_risco:
        print(f"Não encontrou '{risco_label}'.")
        return None, None

    # Encontra o próximo <td> com o texto do risco
    td_risco_seguinte = td_risco.find_next('td')
    if not td_risco_seguinte:
        print(f"Não encontrou os riscos para '{risco_label}'.")
        return None, None

    # Extrai os riscos, removendo linhas vazias ou excessos de espaço
    riscos = separar_riscos(td_risco_seguinte.text)
    return td_risco, riscos

def comparar_riscos(riscos_encontrados, riscos_usuario):
    # Converte os riscos encontrados e os informados pelo usuário em conjuntos, ignorando acentuação, espaços e maiúsculas
    riscos_encontrados_set = set(riscos_encontrados)
    riscos_usuario_set = set(riscos_usuario)

    print("Riscos encontrados:", riscos_encontrados_set)
    print("Riscos fornecidos pelo usuário:", riscos_usuario_set)

    riscos_faltando = riscos_encontrados_set - riscos_usuario_set
    riscos_extra = riscos_usuario_set - riscos_encontrados_set

    if not riscos_faltando and not riscos_extra:
        print("Tudo certo! Os riscos estão corretos.")
    else:
        if riscos_faltando:
            print("Riscos faltando:")
            for risco in riscos_faltando:
                print(f"- {risco}")
        if riscos_extra:
            print("Riscos extras informados:")
            for risco in riscos_extra:
                print(f"- {risco}")

def main():
    caminho_arquivo = input("Digite o caminho do arquivo HTML: ")
    html = ler_arquivo_html(caminho_arquivo)

    # Processar os riscos Físicos
    td_perigos, riscos_fisicos = buscar_td_com_riscos(html, "Físicos")
    if riscos_fisicos:
        print("Riscos físicos encontrados:")
        for risco in riscos_fisicos:
            print(f"- {risco}")
        
        # Perguntar ao usuário quais riscos ele considera corretos
        riscos_usuario = input("Digite os riscos físicos corretos separados por vírgula: ").split(',')
        riscos_usuario = [normalizar_texto(r.strip()) for r in riscos_usuario]
        
        # Comparar os riscos encontrados com os riscos fornecidos pelo usuário
        comparar_riscos(riscos_fisicos, riscos_usuario)

    # Processar os riscos Químicos
    td_quimicos, riscos_quimicos = buscar_td_com_riscos(html, "Químicos")
    if riscos_quimicos:
        print("Riscos químicos encontrados:")
        for risco in riscos_quimicos:
            print(f"- {risco}")
        
        # Perguntar ao usuário quais riscos ele considera corretos
        riscos_usuario = input("Digite os riscos químicos corretos separados por vírgula: ").split(',')
        riscos_usuario = [normalizar_texto(r.strip()) for r in riscos_usuario]
        
        # Comparar os riscos encontrados com os riscos fornecidos pelo usuário
        comparar_riscos(riscos_quimicos, riscos_usuario)

    # Processar os riscos Biológicos
    td_biologicos, riscos_biologicos = buscar_td_com_riscos(html, "Biológicos")
    if riscos_biologicos:
        print("Riscos biológicos encontrados:")
        for risco in riscos_biologicos:
            print(f"- {risco}")
        
        # Perguntar ao usuário quais riscos ele considera corretos
        riscos_usuario = input("Digite os riscos biológicos corretos separados por vírgula: ").split(',')
        riscos_usuario = [normalizar_texto(r.strip()) for r in riscos_usuario]
        
        # Comparar os riscos encontrados com os riscos fornecidos pelo usuário
        comparar_riscos(riscos_biologicos, riscos_usuario)

    # Processar os riscos Ergonômicos
    td_ergonomicos, riscos_ergonomicos = buscar_td_com_riscos(html, "Ergonômicos")
    if riscos_ergonomicos:
        print("Riscos ergonômicos encontrados:")
        for risco in riscos_ergonomicos:
            print(f"- {risco}")
        
        # Perguntar ao usuário quais riscos ele considera corretos
        riscos_usuario = input("Digite os riscos ergonômicos corretos separados por vírgula: ").split(',')
        riscos_usuario = [normalizar_texto(r.strip()) for r in riscos_usuario]
        
        # Comparar os riscos encontrados com os riscos fornecidos pelo usuário
        comparar_riscos(riscos_ergonomicos, riscos_usuario)

if __name__ == "__main__":
    main()
