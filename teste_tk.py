import tkinter as tk

root = tk.Tk()
root.title("Teste Tkinter")
root.geometry("300x120")
tk.Label(root, text="Tkinter OK").pack(pady=20)
root.mainloop()
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
