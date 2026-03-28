import tkinter as tk
from tkinter import messagebox, ttk
from statistics import mean
import json
import os

# Nome do arquivo de banco de dados JSON
ARQUIVO_JSON = "cidades.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_JSON):
        return []
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return []

def salvar_no_arquivo(dados):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def adicionar_cidade():
    cidade = entrada_cidade.get().strip()
    pais = entrada_pais.get().strip()
    continente = combo_continente.get()
    
    if not cidade:
        messagebox.showwarning("Aviso", "O nome da cidade é obrigatório.")
        return

    try:
        verao = round(float(entrada_verao.get()), 1)
        outono = round(float(entrada_outono.get()), 1)
        inverno = round(float(entrada_inverno.get()), 1)
        primavera = round(float(entrada_primavera.get()), 1)
    except ValueError:
        messagebox.showerror("Erro", "As temperaturas devem ser números válidos.")
        return

    media = round(mean([verao, outono, inverno, primavera]), 1)
    
    dados = carregar_dados()
    if any(item['cidade'].lower() == cidade.lower() for item in dados):
        messagebox.showwarning("Aviso", "Esta cidade já está cadastrada.")
        return

    nova_cidade = {
        "cidade": cidade, "pais": pais, "continente": continente,
        "verao": verao, "outono": outono, "inverno": inverno, 
        "primavera": primavera, "media": media
    }
    
    dados.append(nova_cidade)
    salvar_no_arquivo(dados)
    atualizar_tabela()
    messagebox.showinfo("Sucesso", f"A cidade {cidade} foi adicionada!")
    limpar_campos()

def limpar_campos():
    entrada_cidade.delete(0, tk.END)
    entrada_pais.delete(0, tk.END)
    combo_continente.set('')
    entrada_verao.delete(0, tk.END)
    entrada_outono.delete(0, tk.END)
    entrada_inverno.delete(0, tk.END)
    entrada_primavera.delete(0, tk.END)

def atualizar_tabela():
    for row in tabela.get_children():
        tabela.delete(row)
    
    dados = carregar_dados()
    for item in dados:
        tabela.insert('', 'end', values=(
            item['cidade'], 
            item['pais'], 
            item['continente'],
            f"{float(item['verao']):.1f}", 
            f"{float(item['outono']):.1f}", 
            f"{float(item['inverno']):.1f}", 
            f"{float(item['primavera']):.1f}", 
            f"{float(item['media']):.1f}"
        ))

cidade_referencia_editar = None

def editar_registro():
    global cidade_referencia_editar
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma cidade para editar.")
        return
    
    item = tabela.item(selecionado[0])
    valores = item['values']
    
    limpar_campos()
    entrada_cidade.insert(0, valores[0])
    entrada_pais.insert(0, valores[1])
    combo_continente.set(valores[2])
    entrada_verao.insert(0, valores[3])
    entrada_outono.insert(0, valores[4])
    entrada_inverno.insert(0, valores[5])
    entrada_primavera.insert(0, valores[6])
    
    cidade_referencia_editar = valores[0] 
    btn_adicionar.config(state=tk.DISABLED)
    btn_salvar.config(state=tk.NORMAL)

def salvar_edicoes():
    global cidade_referencia_editar
    cidade = entrada_cidade.get().strip()
    pais = entrada_pais.get().strip()
    continente = combo_continente.get()
    
    try:
        verao = round(float(entrada_verao.get()), 1)
        outono = round(float(entrada_outono.get()), 1)
        inverno = round(float(entrada_inverno.get()), 1)
        primavera = round(float(entrada_primavera.get()), 1)
    except ValueError:
        messagebox.showerror("Erro", "As temperaturas devem ser números válidos.")
        return

    media = round(mean([verao, outono, inverno, primavera]), 1)
    
    dados = carregar_dados()
    for item in dados:
        if item['cidade'] == cidade_referencia_editar:
            item.update({
                "cidade": cidade, "pais": pais, "continente": continente,
                "verao": verao, "outono": outono, "inverno": inverno, 
                "primavera": primavera, "media": media
            })
            break
            
    salvar_no_arquivo(dados)
    atualizar_tabela()
    messagebox.showinfo("Sucesso", "Registro atualizado!")
    limpar_campos()
    btn_adicionar.config(state=tk.NORMAL)
    btn_salvar.config(state=tk.DISABLED)
    cidade_referencia_editar = None

def buscar_cidades():
    termo = entrada_busca.get().lower()
    dados = carregar_dados()
    for row in tabela.get_children():
        tabela.delete(row)
    for item in dados:
        if termo in item['cidade'].lower() or termo in item['pais'].lower():
            tabela.insert('', 'end', values=(
                item['cidade'], item['pais'], item['continente'],
                f"{item['verao']:.1f}", f"{item['outono']:.1f}", f"{item['inverno']:.1f}", 
                f"{item['primavera']:.1f}", f"{item['media']:.1f}"
            ))

def excluir_registro():
    selecionado = tabela.selection()
    if not selecionado: return
    cidade_nome = tabela.item(selecionado[0])['values'][0]
    if messagebox.askyesno("Confirmar", f"Excluir {cidade_nome}?"):
        dados = carregar_dados()
        dados = [c for c in dados if c['cidade'] != cidade_nome]
        salvar_no_arquivo(dados)
        atualizar_tabela()

# --- INTERFACE ---
root = tk.Tk()
root.title("Clima Mundial - Banco JSON")
root.geometry("850x600")
root.config(bg="#f0f8ff")

frame_form = tk.Frame(root, bg="#f0f8ff", pady=10)
frame_form.pack(fill="x")
frame_tabela = tk.Frame(root)
frame_tabela.pack(fill="both", expand=True)

tk.Label(frame_form, text="Cidade:", bg="#f0f8ff").grid(row=0, column=0, sticky="e")
entrada_cidade = tk.Entry(frame_form, width=20)
entrada_cidade.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_form, text="País:", bg="#f0f8ff").grid(row=1, column=0, sticky="e")
entrada_pais = tk.Entry(frame_form, width=20)
entrada_pais.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Continente:", bg="#f0f8ff").grid(row=2, column=0, sticky="e")
combo_continente = ttk.Combobox(frame_form, values=["África", "América", "Ásia", "Europa", "Oceania"], width=18)
combo_continente.grid(row=2, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Verão (°C):", bg="#f0f8ff").grid(row=0, column=2, sticky="e")
entrada_verao = tk.Entry(frame_form, width=10)
entrada_verao.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_form, text="Outono (°C):", bg="#f0f8ff").grid(row=1, column=2, sticky="e")
entrada_outono = tk.Entry(frame_form, width=10)
entrada_outono.grid(row=1, column=3, padx=5, pady=2)

tk.Label(frame_form, text="Inverno (°C):", bg="#f0f8ff").grid(row=2, column=2, sticky="e")
entrada_inverno = tk.Entry(frame_form, width=10)
entrada_inverno.grid(row=2, column=3, padx=5, pady=2)

tk.Label(frame_form, text="Primavera (°C):", bg="#f0f8ff").grid(row=3, column=2, sticky="e")
entrada_primavera = tk.Entry(frame_form, width=10)
entrada_primavera.grid(row=3, column=3, padx=5, pady=2)

btn_adicionar = tk.Button(frame_form, text="Adicionar Cidade", command=adicionar_cidade, bg="#28a745", fg="white", width=15)
btn_adicionar.grid(row=4, column=0, columnspan=2, pady=15)

btn_editar = tk.Button(frame_form, text="Editar", command=editar_registro, bg="#ffc107", width=10)
btn_editar.grid(row=4, column=2)

btn_salvar = tk.Button(frame_form, text="Salvar Alteração", command=salvar_edicoes, bg="#007bff", fg="white", state=tk.DISABLED, width=15)
btn_salvar.grid(row=4, column=3)

btn_excluir = tk.Button(frame_form, text="Excluir", command=excluir_registro, bg="#dc3545", fg="white", width=10)
btn_excluir.grid(row=4, column=4, padx=5)

tk.Label(frame_form, text="Buscar:", bg="#f0f8ff").grid(row=5, column=0, sticky="e")
entrada_busca = tk.Entry(frame_form, width=30)
entrada_busca.grid(row=5, column=1, columnspan=2, pady=10)
btn_buscar = tk.Button(frame_form, text="Filtrar", command=buscar_cidades, bg="#6c757d", fg="white")
btn_buscar.grid(row=5, column=3)

colunas = ["Cidade", "País", "Continente", "Verão", "Outono", "Inverno", "Primavera", "Média"]
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
for col in colunas:
    tabela.heading(col, text=col)
    tabela.column(col, width=100, anchor="center")
tabela.pack(fill="both", expand=True, side="left")

sc_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
sc_y.pack(side="right", fill="y")
tabela.configure(yscrollcommand=sc_y.set)

atualizar_tabela()
root.mainloop()
