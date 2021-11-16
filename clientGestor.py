from tkinter import *
from tkinter import ttk

from tkinter import messagebox

import sqlite3

root = Tk()
root.title('gestor de clientes')
root.minsize(width=500, height=500)

size = ttk.Sizegrip(root)
size.grid(row=2, column=1, padx=0, pady=0, sticky='se')

conn = sqlite3.connect('contac.db')
c = conn.cursor()

c.execute("""CREATE TABLE if not exists cliente (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			nombre TEXT NOT NULL,
			telefono TEXT NOT NULL,
			empresa TEXT NOT NULL
			);
		 """)


def renderClient():
	rows = c.execute("SELECT * FROM cliente").fetchall()
	tree.delete(*tree.get_children())
	for row in rows:
		tree.insert('', END, row[0], values=(row[1], row[2], row[3]))

def insert(cliente):
	c.execute("INSERT INTO cliente (nombre, telefono, empresa) VALUES (?,?,?)",
			   (cliente['nombre'], cliente['telefono'], cliente['empresa']))

	conn.commit()
	renderClient()

def newClient():

	def saveClient():
		if not Nombre.get():
			messagebox.showerror('Error', 'El Nombre es obligatorio')
			return
		if not Telefono.get():
			messagebox.showerror('Error', 'El Telefono es obligatorio')
			return
		if not Empresa.get():
			messagebox.showerror('Error', 'La empresa es obligatoria')
			return

		cliente = {
			'nombre': Nombre.get(),
			'telefono': Telefono.get(),
			'empresa': Empresa.get(),
		}
		insert(cliente)
		top.destroy()



	top = Toplevel()
	top.title('nuevo cliente')

	lNombre = ttk.Label(top, text='Nombre')
	Nombre = ttk.Entry(top, width=50)
	lNombre.grid(row=0, column=0, padx=8, pady=5)
	Nombre.grid(row=0, column=1, padx=8, pady=5)

	lTelefono = ttk.Label(top, text='Teléfono')
	Telefono = ttk.Entry(top, width=50)
	lTelefono.grid(row=1, column=0, padx=8, pady=5)
	Telefono.grid(row=1, column=1, padx=8, pady=5)

	lEmpresa = ttk.Label(top, text='Empresa')
	Empresa = ttk.Entry(top, width=50)
	lEmpresa.grid(row=2, column=0, padx=8, pady=5)
	Empresa.grid(row=2, column=1, padx=8, pady=5)

	save = ttk.Button(top, text='Guardar', command=saveClient)
	save.grid(row=3, column=1)

	top.mainloop()

def delClient():
	id = tree.selection()
	cliente = c.execute("SELECT * FROM cliente WHERE id=? ",(id))
	respon = messagebox.askokcancel('confirmar','¿Estas seguro que quiere eliminar al cliente?')

	if respon == True:
		c.execute("DELETE FROM cliente WHERE id= ?", (id))
		conn.commit()
		renderClient()
	else:
		pass

btnClient = ttk.Button(root, text='nuevo cliente', command=newClient)
btnClient.grid(column=0, row=0)

btnDelClient = ttk.Button(root, text='borrar cliente', command=delClient)
btnDelClient.grid(column=1, row=0)

tree = ttk.Treeview(root)
tree['columns']=('Nombre','Telefono', 'Empresa')
tree.column('#0', width=0, stretch=NO) # las propiedades width y stretch es para que no aparezca en la ventana
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

tree.heading('Nombre', text='Nombre')
tree.heading('Telefono', text='Teléfono')
tree.heading('Empresa', text='Empresa')
tree.grid(column=0, row=1, columnspan=2, sticky='nswes', padx=15, pady=5)

renderClient()

root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()