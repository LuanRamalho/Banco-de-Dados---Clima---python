import tkinter as tk
from tkinter import messagebox, ttk
from statistics import mean
import sqlite3

# Configuração do banco de dados SQLite
conexao = sqlite3.connect("cidades.db")
cursor = conexao.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS cidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cidade TEXT,
    pais TEXT,
    continente TEXT,
    verao REAL,
    outono REAL,
    inverno REAL,
    primavera REAL,
    media REAL
)''')
conexao.commit()

# Função para adicionar uma cidade ao banco de dados
def adicionar_cidade():
    cidade = entrada_cidade.get()
    pais = entrada_pais.get()
    continente = combo_continente.get()
    try:
        verao = float(entrada_verao.get())
        outono = float(entrada_outono.get())
        inverno = float(entrada_inverno.get())
        primavera = float(entrada_primavera.get())
    except ValueError:
        messagebox.showerror("Erro", "As temperaturas devem ser números válidos.")
        return

    media = round(mean([verao, outono, inverno, primavera]), 2)
    cursor.execute('''INSERT INTO cidades (cidade, pais, continente, verao, outono, inverno, primavera, media)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (cidade, pais, continente, verao, outono, inverno, primavera, media))
    conexao.commit()
    atualizar_tabela()
    messagebox.showinfo("Sucesso", f"A cidade {cidade} foi adicionada com sucesso!")
    limpar_campos()

# Função para limpar os campos do formulário
def limpar_campos():
    entrada_cidade.delete(0, tk.END)
    entrada_pais.delete(0, tk.END)
    combo_continente.set('')
    entrada_verao.delete(0, tk.END)
    entrada_outono.delete(0, tk.END)
    entrada_inverno.delete(0, tk.END)
    entrada_primavera.delete(0, tk.END)

# Função para atualizar a tabela de dados na interface
def atualizar_tabela():
    for row in tabela.get_children():
        tabela.delete(row)
    cursor.execute("SELECT cidade, pais, continente, verao, outono, inverno, primavera, media FROM cidades")
    for cidade in cursor.fetchall():
        tabela.insert('', 'end', values=cidade)

# Variável global para armazenar o ID da cidade a ser editada
id_cidade_editar = None

# Função para editar um registro de cidade
def editar_registro():
    global id_cidade_editar  # Utiliza a variável global para o ID
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma cidade para editar.")
        return
    item = tabela.item(selecionado[0])
    valores = item['values']
    entrada_cidade.insert(0, valores[0])
    entrada_pais.insert(0, valores[1])
    combo_continente.set(valores[2])
    entrada_verao.insert(0, valores[3])
    entrada_outono.insert(0, valores[4])
    entrada_inverno.insert(0, valores[5])
    entrada_primavera.insert(0, valores[6])
    id_cidade_editar = valores[0]  # Armazena o nome da cidade para edição

    # Desabilita o botão de adicionar e habilita o de salvar
    btn_adicionar.config(state=tk.DISABLED)
    btn_salvar.config(state=tk.NORMAL)

# Função para salvar as edições feitas em um registro
def salvar_edicoes():
    global id_cidade_editar  # Utiliza a variável global para o ID
    cidade = entrada_cidade.get()
    pais = entrada_pais.get()
    continente = combo_continente.get()
    try:
        verao = float(entrada_verao.get())
        outono = float(entrada_outono.get())
        inverno = float(entrada_inverno.get())
        primavera = float(entrada_primavera.get())
    except ValueError:
        messagebox.showerror("Erro", "As temperaturas devem ser números válidos.")
        return

    media = round(mean([verao, outono, inverno, primavera]), 2)
    cursor.execute('''UPDATE cidades SET cidade = ?, pais = ?, continente = ?, verao = ?, outono = ?, inverno = ?, primavera = ?, media = ?
                      WHERE cidade = ?''', 
                   (cidade, pais, continente, verao, outono, inverno, primavera, media, id_cidade_editar))
    conexao.commit()
    atualizar_tabela()
    messagebox.showinfo("Sucesso", f"A cidade {cidade} foi atualizada com sucesso!")
    limpar_campos()

    # Reabilita o botão de adicionar e desabilita o de salvar
    btn_adicionar.config(state=tk.NORMAL)
    btn_salvar.config(state=tk.DISABLED)
    id_cidade_editar = None  # Reseta o ID

# Função para buscar cidades
def buscar_cidades():
    termo = entrada_busca.get().lower()
    cursor.execute("SELECT cidade, pais, continente, verao, outono, inverno, primavera, media FROM cidades")
    resultados = [cidade for cidade in cursor.fetchall() if termo in cidade[0].lower() or termo in cidade[1].lower() or termo in cidade[2].lower()]
    for row in tabela.get_children():
        tabela.delete(row)
    for cidade in resultados:
        tabela.insert('', 'end', values=cidade)

# Função para excluir um registro
def excluir_registro():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma cidade para excluir.")
        return
    cidade_nome = tabela.item(selecionado[0])['values'][0]
    cursor.execute("DELETE FROM cidades WHERE cidade = ?", (cidade_nome,))
    conexao.commit()
    atualizar_tabela()
    messagebox.showinfo("Sucesso", "A cidade foi excluída com sucesso.")

# Configurando a interface gráfica
root = tk.Tk()
root.title("Banco de Dados de Cidades")
root.geometry("800x600")
root.config(bg="#f0f8ff")

# Criando os frames
frame_form = tk.Frame(root, bg="#f0f8ff", pady=10)
frame_form.pack(fill="x")
frame_tabela = tk.Frame(root)
frame_tabela.pack(fill="both", expand=True)

# Adicionando campos do formulário
tk.Label(frame_form, text="Cidade:", bg="#f0f8ff").grid(row=0, column=0, sticky="e")
entrada_cidade = tk.Entry(frame_form, width=20)
entrada_cidade.grid(row=0, column=1)

tk.Label(frame_form, text="País:", bg="#f0f8ff").grid(row=1, column=0, sticky="e")
entrada_pais = tk.Entry(frame_form, width=20)
entrada_pais.grid(row=1, column=1)

tk.Label(frame_form, text="Continente:", bg="#f0f8ff").grid(row=2, column=0, sticky="e")
combo_continente = ttk.Combobox(frame_form, values=["África", "América", "Ásia", "Europa", "Oceania"], width=18)
combo_continente.grid(row=2, column=1)

tk.Label(frame_form, text="Verão (°C):", bg="#f0f8ff").grid(row=0, column=2, sticky="e")
entrada_verao = tk.Entry(frame_form, width=10)
entrada_verao.grid(row=0, column=3)

tk.Label(frame_form, text="Outono (°C):", bg="#f0f8ff").grid(row=1, column=2, sticky="e")
entrada_outono = tk.Entry(frame_form, width=10)
entrada_outono.grid(row=1, column=3)

tk.Label(frame_form, text="Inverno (°C):", bg="#f0f8ff").grid(row=2, column=2, sticky="e")
entrada_inverno = tk.Entry(frame_form, width=10)
entrada_inverno.grid(row=2, column=3)

tk.Label(frame_form, text="Primavera (°C):", bg="#f0f8ff").grid(row=3, column=2, sticky="e")
entrada_primavera = tk.Entry(frame_form, width=10)
entrada_primavera.grid(row=3, column=3)

# Botões
btn_adicionar = tk.Button(frame_form, text="Adicionar Cidade", command=adicionar_cidade, bg="#28a745", fg="white")
btn_adicionar.grid(row=4, columnspan=3, pady=10)

# Criando o botão "Salvar"
btn_salvar = tk.Button(frame_form, text="Salvar", command=salvar_edicoes, bg="#007bff", fg="white", state=tk.DISABLED)
btn_salvar.grid(row=4, column=3, padx=5)

btn_editar = tk.Button(frame_form, text="Editar Cidade", command=editar_registro, bg="#ffc107", fg="black")
btn_editar.grid(row=4, column=2, padx=5)

btn_excluir = tk.Button(frame_form, text="Excluir Cidade", command=excluir_registro, bg="#dc3545", fg="white")
btn_excluir.grid(row=4, column=10, padx=5)

# Adicionando a tabela para visualização com barras de rolagem
colunas = ["Cidade", "País", "Continente", "Verão (°C)", "Outono (°C)", "Inverno (°C)", "Primavera (°C)", "Média (°C)"]
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
for col in colunas:
    tabela.heading(col, text=col)
tabela.pack(fill="both", expand=True)

# Barra de rolagem vertical
scrollbar_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
scrollbar_y.pack(side="right", fill="y")
tabela.configure(yscrollcommand=scrollbar_y.set)

# Barra de rolagem horizontal
scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tabela.xview)
scrollbar_x.pack(side="bottom", fill="x")
tabela.configure(xscrollcommand=scrollbar_x.set)

# Campo de busca
entrada_busca = tk.Entry(frame_form, width=30)
entrada_busca.grid(row=5, column=0, columnspan=2, pady=10)
btn_buscar = tk.Button(frame_form, text="Buscar", command=buscar_cidades, bg="#007bff", fg="white")
btn_buscar.grid(row=5, column=2, columnspan=2, pady=10)

# Carregar dados iniciais da tabela
atualizar_tabela()

root.mainloop()
conexao.close()
