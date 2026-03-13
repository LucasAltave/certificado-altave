import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path

from cert_gen import generate_certificate_pdf, generate_certificate_png


def _row_entry(parent, label, var, row):
    ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=6)
    ent = ttk.Entry(parent, textvariable=var, width=48)
    ent.grid(row=row, column=1, sticky="w", pady=6)
    return ent


def main():
    root = tk.Tk()
    root.title("Certificado Harpia Altave")
    root.geometry("720x430")
    root.resizable(False, False)

    frm = ttk.Frame(root, padding=16)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Gerador de Certificado Harpia Altave", font=("Segoe UI", 15, "bold")).grid(
        row=0, column=0, columnspan=2, sticky="w", pady=(0, 14)
    )

    full_name_var = tk.StringVar()
    role_var = tk.StringVar()
    company_var = tk.StringVar()
    instructor_var = tk.StringVar(value="Lucas Pereira")
    date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))

    _row_entry(frm, "Nome completo:", full_name_var, 1)
    _row_entry(frm, "Função:", role_var, 2)
    _row_entry(frm, "Empresa:", company_var, 3)
    _row_entry(frm, "Instrutor:", instructor_var, 4)
    _row_entry(frm, "Data:", date_var, 5)

    status = tk.StringVar(value="Pronto.")
    ttk.Label(frm, textvariable=status).grid(row=8, column=0, columnspan=2, sticky="w", pady=(16, 0))

    def _validate():
        if not full_name_var.get().strip():
            messagebox.showwarning("Atenção", "Preencha o nome completo.")
            return False
        if not role_var.get().strip():
            messagebox.showwarning("Atenção", "Preencha a função.")
            return False
        if not company_var.get().strip():
            messagebox.showwarning("Atenção", "Preencha a empresa.")
            return False
        if not instructor_var.get().strip():
            messagebox.showwarning("Atenção", "Preencha o instrutor.")
            return False
        if not date_var.get().strip():
            messagebox.showwarning("Atenção", "Preencha a data.")
            return False
        return True

    def on_preview():
        if not _validate():
            return
        try:
            status.set("Gerando preview...")
            root.update_idletasks()

            out_path = generate_certificate_png(
                full_name=full_name_var.get().strip(),
                role=role_var.get().strip(),
                company_name=company_var.get().strip(),
                date_text=date_var.get().strip(),
                instructor=instructor_var.get().strip(),
            )

            status.set("Preview gerado.")
            messagebox.showinfo("Preview", f"Preview gerado em:\n{out_path}")
        except Exception as e:
            status.set("Erro ❌")
            messagebox.showerror("Erro", f"Ocorreu um erro:\n\n{e}")

    def on_generate_pdf():
        if not _validate():
            return
        try:
            status.set("Gerando PDF...")
            root.update_idletasks()

            pdf_path = generate_certificate_pdf(
                full_name=full_name_var.get().strip(),
                role=role_var.get().strip(),
                company_name=company_var.get().strip(),
                date_text=date_var.get().strip(),
                instructor=instructor_var.get().strip(),
            )

            save_path = filedialog.asksaveasfilename(
                title="Salvar certificado PDF como...",
                defaultextension=".pdf",
                initialfile=Path(pdf_path).name,
                filetypes=[("PDF", "*.pdf")],
            )

            if not save_path:
                status.set("PDF gerado em output/.")
                messagebox.showinfo("PDF gerado", f"Arquivo gerado em:\n{pdf_path}")
                return

            shutil.copy2(pdf_path, save_path)
            status.set("Concluído ✅")
            messagebox.showinfo("Sucesso", f"PDF salvo em:\n{save_path}")

        except Exception as e:
            status.set("Erro ❌")
            messagebox.showerror("Erro", f"Ocorreu um erro:\n\n{e}")

    def on_clear():
        full_name_var.set("")
        role_var.set("")
        company_var.set("")
        instructor_var.set("Lucas Pereira")
        date_var.set(datetime.now().strftime("%d/%m/%Y"))
        status.set("Pronto.")

    btns = ttk.Frame(frm)
    btns.grid(row=7, column=0, columnspan=2, sticky="e", pady=(16, 0))

    ttk.Button(btns, text="Limpar", command=on_clear).pack(side="right", padx=(8, 0))
    ttk.Button(btns, text="Gerar PDF", command=on_generate_pdf).pack(side="right", padx=(8, 0))
    ttk.Button(btns, text="Gerar Preview PNG", command=on_preview).pack(side="right")

    root.mainloop()


if __name__ == "__main__":
    main()
    import tkinter as tk

def criar_interface():
    root = tk.Tk()
    root.title("Minha Aplicação com Tkinter")

    # Criação de widgets
    label = tk.Label(root, text="Bem-vindo ao meu app!")
    label.pack(pady=20)

    # Botão para fechar
    button = tk.Button(root, text="Fechar", command=root.quit)
    button.pack(pady=10)

    root.mainloop()

# Chamar a função para criar a interface
criar_interface()
