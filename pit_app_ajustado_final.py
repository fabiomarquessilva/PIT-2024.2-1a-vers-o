@echo off
python pit_app_ajustado_final.py
pause

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fpdf import FPDF

class PITApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de PIT")
        self.root.geometry("900x700")

        # Criando o notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Dados consolidados
        self.dados_consolidados = {
            "Atividades de Ensino": {"itens": [], "total": 0, "soma_numeros": 0},
            "Atividades de Pesquisa": {"itens": [], "total": 0, "soma_numeros": 0},
            "Atividades de Extensão": {"itens": [], "total": 0, "soma_numeros": 0},
            "Atividades Administrativas e Representação": {"itens": [], "total": 0, "soma_numeros": 0},
            "Atividades de Monitoria Acadêmica": {"itens": [], "total": 0, "soma_numeros": 0},
            "Orientação de TCC": {"itens": [], "total": 0, "soma_numeros": 0},
            "Produção Intelectual": {"itens": [], "total": 0, "soma_numeros": 0},
            "Outras Atividades": {"itens": [], "total": 0, "soma_numeros": 0},
            "Atividades Pedagógicas Remotas": {"itens": [], "total": 0, "soma_numeros": 0},
        }

        # Criando as abas
        self.create_formulario_tab()
        self.create_activity_tabs()
        self.create_consolidado_tab()

    def create_formulario_tab(self):
        self.formulario_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.formulario_tab, text="Formulário PIT")

        frame = tk.Frame(self.formulario_tab)
        frame.pack(pady=20)

        tk.Label(frame, text="Nome do Professor:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nome_entry = tk.Entry(frame, width=50)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Matrícula SIAPE:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.matricula_entry = tk.Entry(frame, width=50)
        self.matricula_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Unidade Acadêmica:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.unidade_entry = tk.Entry(frame, width=50)
        self.unidade_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame, text="Regime de Trabalho:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.regime_entry = tk.Entry(frame, width=50)
        self.regime_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame, text="Período Letivo:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.periodo_entry = tk.Entry(frame, width=50)
        self.periodo_entry.grid(row=4, column=1, padx=10, pady=5)

    def create_activity_tabs(self):
        activities = {
            "Atividades de Ensino": ["Curso", "Disciplina(s)", "CH Semanal", "Aula/Crédito", "Planejamento"],
            "Atividades de Pesquisa": ["Projeto", "Título", "CH Semanal"],
            "Atividades de Extensão": ["Projeto", "Função", "Título", "CH Semanal"],
            "Atividades Administrativas e Representação": ["Função/Atividade", "CH Semanal"],
            "Atividades de Monitoria Acadêmica": ["Título do Projeto", "Número de Monitores", "CH Semanal"],
            "Orientação de TCC": ["Natureza", "Título", "CH Semanal"],
            "Produção Intelectual": ["Natureza", "Título", "CH Semanal"],
            "Outras Atividades": ["Tipo de Atividade", "CH Semanal"],
            "Atividades Pedagógicas Remotas": ["Período/Data", "Atividade", "Ferramenta", "CH Semanal"]
        }

        for title, columns in activities.items():
            self.create_activity_tab(title, title, columns)

    def create_activity_tab(self, title, activity_key, columns):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)

        frame_inputs = tk.Frame(tab)
        frame_inputs.pack(pady=10)

        entries = {}
        for i, col in enumerate(columns):
            tk.Label(frame_inputs, text=col).grid(row=i, column=0, padx=5, pady=5)
            entries[col] = tk.Entry(frame_inputs, width=30)
            entries[col].grid(row=i, column=1, padx=5, pady=5)

        def add_activity():
            values = [entry.get().strip() for entry in entries.values()]
            if any(not v for v in values):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
                return

            soma_numeros = sum(int(v) for v in values if v.isdigit())
            self.dados_consolidados[activity_key]["itens"].append(values)
            self.dados_consolidados[activity_key]["total"] += soma_numeros
            self.dados_consolidados[activity_key]["soma_numeros"] += soma_numeros

            tree.insert("", "end", values=values + [soma_numeros])
            total_label.config(text=f"Carga Horária Total: {self.dados_consolidados[activity_key]['total']} horas")
            soma_label.config(text=f"Soma dos Valores: {self.dados_consolidados[activity_key]['soma_numeros']}")

            for entry in entries.values():
                entry.delete(0, tk.END)

        tk.Button(frame_inputs, text="Adicionar", command=add_activity).grid(row=len(columns), column=0, columnspan=2, pady=10)

        tree = ttk.Treeview(tab, columns=columns + ["Soma"], show="headings")
        for col in columns + ["Soma"]:
            tree.heading(col, text=col)
        tree.pack(pady=10, fill="both", expand=True)

        total_label = tk.Label(tab, text=f"Carga Horária Total: 0 horas")
        total_label.pack()

        soma_label = tk.Label(tab, text=f"Soma dos Valores: 0")
        soma_label.pack()

    def create_consolidado_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Consolidado e PDF")

        def gerar_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Relatório Final do PIT", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Nome do Docente: {self.nome_entry.get()}", ln=True, align="L")
            pdf.cell(200, 10, txt=f"Matrícula SIAPE: {self.matricula_entry.get()}", ln=True, align="L")
            pdf.cell(200, 10, txt=f"Unidade Acadêmica: {self.unidade_entry.get()}", ln=True, align="L")
            pdf.cell(200, 10, txt=f"Regime de Trabalho: {self.regime_entry.get()}", ln=True, align="L")
            pdf.cell(200, 10, txt=f"Período Letivo: {self.periodo_entry.get()}", ln=True, align="L")

            pdf.ln(10)
            pdf.cell(200, 10, txt="Consolidado das Atividades:", ln=True, align="L")
            for atividade, dados in self.dados_consolidados.items():
                pdf.cell(200, 10, txt=f"{atividade} - Total: {dados['total']} horas - Soma: {dados['soma_numeros']}", ln=True, align="L")
                for item in dados["itens"]:
                    pdf.cell(200, 10, txt=f"  - {' | '.join(item)}", ln=True, align="L")

            total_final = sum(dados["total"] for dados in self.dados_consolidados.values())
            pdf.cell(200, 10, txt=f"Total Geral: {total_final} horas", ln=True, align="L")

            pdf.ln(10)
            pdf.multi_cell(0, 10, txt="Considerações Finais: Este relatório reflete o planejamento do PIT para o período.")

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if file_path:
                pdf.output(file_path)
                messagebox.showinfo("PDF Gerado", "O PDF foi salvo com sucesso!")

        tk.Button(tab, text="Gerar PDF", command=gerar_pdf).pack(pady=20)

@echo off
python pit_app_ajustado_final.py
pause
