
import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import os

class PITApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Relatório PIT")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")

        self.total_ch = 0  # Variável para somar as cargas horárias
        self.sections_data = {}  # Dicionário para armazenar dados das seções
        self.section_totals = {}  # Totais por categoria
        self.show_header_form()

    def show_header_form(self):
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg="#003366", pady=20)
        header_frame.pack(fill="x")

        header_text = """
UNIVERSIDADE FEDERAL DE CAMPINA GRANDE
CENTRO DE FORMAÇÃO DE PROFESSORES
UNIDADE ACADÊMICA DE ENFERMAGEM

PLANO INDIVIDUAL DE TRABALHO DOCENTE (PIT)
"""

        header_label = tk.Label(header_frame, text=header_text, font=("Arial", 16, "bold"), fg="white", bg="#003366", justify="center")
        header_label.pack()

        # Formulário
        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(pady=20, fill="x", expand=True)
    
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12), background="#003366", foreground="white")

        # Campo para o nome
        ttk.Label(form_frame, text="Nome do Professor(a):").grid(row=0, column=0, sticky="w", pady=10, padx=10)
        self.name_entry = ttk.Entry(form_frame, width=50)
        self.name_entry.grid(row=0, column=1, pady=10, padx=10)

        # Campo para a matrícula SIAPE
        ttk.Label(form_frame, text="Matrícula SIAPE:").grid(row=1, column=0, sticky="w", pady=10, padx=10)
        self.siape_entry = ttk.Entry(form_frame, width=20)
        self.siape_entry.grid(row=1, column=1, pady=10, padx=10)

        # Campo para o período
        ttk.Label(form_frame, text="Período/Ano:").grid(row=2, column=0, sticky="w", pady=10, padx=10)
        self.period_entry = ttk.Entry(form_frame, width=20)
        self.period_entry.grid(row=2, column=1, pady=10, padx=10)

        # Botão para salvar as informações
        save_button = ttk.Button(form_frame, text="Confirmar e Continuar", command=self.show_teaching_section)
        save_button.grid(row=3, column=0, columnspan=2, pady=20)
    
    def show_teaching_section(self):
        self.show_section_form(
            title="Atividades de Ensino",
            labels=["Curso", "Disciplina", "CH Semanal"],
            next_action=self.show_research_section,
            section_key="teaching"
        )

    def show_research_section(self):
        self.show_section_form(
            title="Atividades de Pesquisa",
            labels=["Projeto", "Título da Pesquisa", "CH Semanal"],
            next_action=self.show_extension_section,
            section_key="research"
        )

    def show_extension_section(self):
        self.show_section_form(
            title="Atividades de Extensão",
            labels=["Projeto", "Função", "CH Semanal"],
            next_action=self.show_monitoring_section,
            section_key="extension"
        )

    def show_monitoring_section(self):
        self.show_section_form(
            title="Atividades de Monitoria Acadêmica",
            labels=["Título do Projeto", "Número de Monitores", "CH Semanal"],
            next_action=self.show_final_summary,
            section_key="monitoring"
        )
    