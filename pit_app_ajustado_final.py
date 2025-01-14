import streamlit as st
from fpdf import FPDF

# Função para gerar o PDF
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Cabeçalho
    pdf.cell(200, 10, txt="UNIVERSIDADE FEDERAL DE CAMPINA GRANDE", ln=True, align="C")
    pdf.cell(200, 10, txt="CENTRO DE FORMAÇÃO DE PROFESSORES", ln=True, align="C")
    pdf.cell(200, 10, txt="UNIDADE ACADÊMICA DE ENFERMAGEM", ln=True, align="C")
    pdf.cell(200, 10, txt="PLANO INDIVIDUAL DE TRABALHO DOCENTE (PIT)", ln=True, align="C")
    pdf.ln(10)

    # Dados do professor
    pdf.cell(200, 10, txt=f"Nome do Professor: {dados['nome']}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Matrícula SIAPE: {dados['siape']}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Unidade Acadêmica: {dados['unidade']}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Regime de Trabalho: {dados['regime']}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Período Letivo: {dados['periodo']}", ln=True, align="L")
    pdf.ln(10)

    # Atividades
    for atividade, itens in dados["atividades"].items():
        pdf.cell(200, 10, txt=f"{atividade}:", ln=True, align="L")
        for item in itens:
            pdf.cell(200, 10, txt=f"  - {item}", ln=True, align="L")
        pdf.ln(5)

    # Salvar PDF
    pdf_path = "pit_relatorio.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Aplicativo Streamlit
st.title("Gerador de PIT")
st.header("Plano Individual de Trabalho Docente (PIT)")

# Dados do professor
st.subheader("Informações do Professor")
nome = st.text_input("Nome do Professor")
siape = st.text_input("Matrícula SIAPE")
unidade = st.text_input("Unidade Acadêmica")
regime = st.text_input("Regime de Trabalho")
periodo = st.text_input("Período Letivo")

# Atividades
atividades = {
    "Atividades de Ensino": st.text_area("Atividades de Ensino (separe por linhas)").split("\n"),
    "Atividades de Pesquisa": st.text_area("Atividades de Pesquisa (separe por linhas)").split("\n"),
    "Atividades de Extensão": st.text_area("Atividades de Extensão (separe por linhas)").split("\n"),
    "Atividades Administrativas": st.text_area("Atividades Administrativas (separe por linhas)").split("\n"),
    "Atividades de Monitoria Acadêmica": st.text_area("Atividades de Monitoria Acadêmica (separe por linhas)").split("\n"),
    "Orientação de TCC": st.text_area("Orientação de TCC (separe por linhas)").split("\n"),
    "Produção Intelectual": st.text_area("Produção Intelectual (separe por linhas)").split("\n"),
    "Outras Atividades": st.text_area("Outras Atividades (separe por linhas)").split("\n"),
    "Atividades Pedagógicas Remotas": st.text_area("Atividades Pedagógicas Remotas (separe por linhas)").split("\n"),
}

# Botão para gerar o PDF
if st.button("Gerar PDF"):
    dados = {
        "nome": nome,
        "siape": siape,
        "unidade": unidade,
        "regime": regime,
        "periodo": periodo,
        "atividades": atividades,
    }
    pdf_path = gerar_pdf(dados)
    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Baixar Relatório em PDF",
            data=pdf_file,
            file_name="PIT_Relatorio.pdf",
            mime="application/pdf",
        )
