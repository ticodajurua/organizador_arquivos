import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


tipos_de_arquivo = {
    'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Documentos': ['.pdf', '.docx', '.doc', '.txt'],
    'Planilhas': ['.xls', '.xlsx', '.csv'],
    'Apresentacoes': ['.ppt', '.pptx', '.odp', '.key'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Musicas': ['.mp3', '.wav', '.flac', '.aac'],
    'Arquivos Compactados': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css', '.java', '.c', '.cpp'],
    'Imagens de Disco': ['.iso', '.dmg'],
    'Executaveis': ['.exe', '.msi', '.bat', '.sh'],
    'Outros': []
}

def escanear_arquivos(diretorio):
    contagem = {tipo: 0 for tipo in tipos_de_arquivo}
    contagem['Outros'] = 0
    total = 0
    for arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, arquivo)
        if os.path.isfile(caminho_completo):
            extensao = os.path.splitext(arquivo)[1].lower()
            encontrado = False
            for tipo, extensoes in tipos_de_arquivo.items():
                if extensao in extensoes:
                    contagem[tipo] = contagem.get(tipo, 0) + 1
                    encontrado = True
                    break
            if not encontrado:
                contagem['Outros'] += 1
            total += 1
    return contagem, total

def organizar_arquivos(diretorio):
    try:

        for arquivo in os.listdir(diretorio):
            caminho_completo = os.path.join(diretorio, arquivo)
            if os.path.isfile(caminho_completo):
                extensao = os.path.splitext(arquivo)[1].lower()
                categoria = 'Outros'
                for tipo, extensoes in tipos_de_arquivo.items():
                    if extensao in extensoes:
                        categoria = tipo
                        break
                pasta_destino = os.path.join(diretorio, categoria)
                os.makedirs(pasta_destino, exist_ok=True)
                shutil.move(caminho_completo, os.path.join(pasta_destino, arquivo))
        status_var.set('Organizacao concluida com sucesso!')
        perguntar_nova_pasta()
    except Exception as e:
        status_var.set(f'Erro ao organizar arquivos: {e}')

def perguntar_nova_pasta():
    resposta = messagebox.askyesno('Nova Pasta', 'Arquivos organizados! Deseja organizar arquivos em uma nova pasta?')
    if resposta:
        selecionar_diretorio()
    else:
        janela.destroy()

def selecionar_diretorio():
    caminho = filedialog.askdirectory()
    if caminho: 
        contagem, total = escanear_arquivos(caminho)
        resumo = f'Total de arquivos: {total}\n'
        for tipo, quantidade in contagem.items():
            if quantidade > 0:
                resumo += f'{tipo}: {quantidade}\n'
        status_var.set(resumo)
        botao_organizar.config(state='normal')
        janela.diretorio_selecionado = caminho


janela = tk.Tk()
janela.title('OCTA - Organizador de Arquivos')
janela.geometry('430x300')
janela.resizable(False, False)

status_var = tk.StringVar()
janela.diretorio_selecionado = None

tk.Label(janela, text = 'Organize seus arquivos por tipo.').pack(pady=10)
tk.Button(janela, text = 'Selecionar Diretório', command=selecionar_diretorio).pack(pady=10)
botao_organizar = tk.Button(janela, text='Iniciar Organizacao', command=lambda: organizar_arquivos(janela.diretorio_selecionado), state='disabled')
botao_organizar.pack(pady=5)
tk.Label(janela, textvariable=status_var, font=('Arial', 10), justify='left').pack(pady=10)


janela.mainloop()

