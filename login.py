import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class LoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.usuario_actual = None
        
        # Crear ventana de login
        self.login_window = tk.Toplevel(parent)
        self.login_window.title("Iniciar Sesión - Sistema MYPYME")
        self.login_window.geometry("400x300")
        self.login_window.resizable(False, False)
        self.login_window.transient(parent)
        self.login_window.grab_set()
        
        # Centrar ventana
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.login_window.winfo_screenheight() // 2) - (300 // 2)
        self.login_window.geometry(f"400x300+{x}+{y}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interfaz de login"""
        # Frame principal
        main_frame = tk.Frame(self.login_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="SISTEMA MYPYME", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        # Frame del formulario
        form_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título del formulario
        tk.Label(form_frame, text="Iniciar Sesión", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=20)
        
        # Campos
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(pady=20)
        
        # Usuario
        tk.Label(fields_frame, text="Usuario:", bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.username_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.username_var, width=25).grid(row=0, column=1, pady=5, padx=10)
        
        # Contraseña
        tk.Label(fields_frame, text="Contraseña:", bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=10)
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(fields_frame, textvariable=self.password_var, show="*", width=25)
        password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Botones
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Iniciar Sesión", command=self.login,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancelar", command=self.cancelar,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'), width=15).pack(side=tk.LEFT, padx=5)
        
        # Información de usuario por defecto
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text="Usuario por defecto: admin / admin123", 
                font=('Arial', 8), bg='#f0f0f0', fg='gray').pack()
        
        # Enfocar en el campo de usuario
        self.username_var.set("admin")
        password_entry.focus()
        
        # Bind Enter key
        password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Procesar login"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        # Autenticar usuario
        usuario = self.db.autenticar_usuario(username, password)
        
        if usuario:
            self.usuario_actual = {
                'id': usuario[0],
                'username': usuario[1],
                'nombre_completo': usuario[2],
                'rol': usuario[3]
            }
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario[2]}!")
            self.login_window.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def cancelar(self):
        """Cancelar login"""
        self.login_window.destroy()
    
    def get_usuario_actual(self):
        """Retornar información del usuario autenticado"""
        return self.usuario_actual 