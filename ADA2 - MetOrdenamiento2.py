import tkinter as tk
from tkinter import messagebox, ttk


# ==========================================
# LGICA DE LOS ALGORITMOS DE ORDENAMIENTO
# ==========================================
def shell_sort(arr):
  arr = arr.copy()
  n = len(arr)
  gap = n // 2
  while gap > 0:
    for i in range(gap, n):
      temp = arr[i]
      j = i
      while j >= gap and arr[j - gap] > temp:
        arr[j] = arr[j - gap]
        j -= gap
      arr[j] = temp
    gap //= 2
  return arr


def quick_sort(arr):
  arr = arr.copy()
  if len(arr) <= 1:
    return arr
  pivot = arr[len(arr) // 2]
  left = [x for x in arr if x < pivot]
  middle = [x for x in arr if x == pivot]
  right = [x for x in arr if x > pivot]
  return quick_sort(left) + middle + quick_sort(right)


def heapify(arr, n, i):
  largest = i
  l = 2 * i + 1
  r = 2 * i + 2

  if l < n and arr[l] > arr[largest]:
    largest = l
  if r < n and arr[r] > arr[largest]:
    largest = r

  if largest != i:
    arr[i], arr[largest] = arr[largest], arr[i]
    heapify(arr, n, largest)


def heap_sort(arr):
  arr = arr.copy()
  n = len(arr)
  for i in range(n // 2 - 1, -1, -1):
    heapify(arr, n, i)
  for i in range(n - 1, 0, -1):
    arr[i], arr[0] = arr[0], arr[i]
    heapify(arr, i, 0)
  return arr


def counting_sort_for_radix(arr, exp):
  n = len(arr)
  output = [0] * n
  count = [0] * 10

  for i in range(n):
    index = arr[i] // exp
    count[index % 10] += 1

  for i in range(1, 10):
    count[i] += count[i - 1]

  i = n - 1
  while i >= 0:
    index = arr[i] // exp
    output[count[index % 10] - 1] = arr[i]
    count[index % 10] -= 1
    i -= 1

  for i in range(n):
    arr[i] = output[i]


def radix_sort(arr):
  arr = arr.copy()
  if any(x < 0 for x in arr):
    raise ValueError(
        "Radix Sort requiere números enteros no menores a 0 (no acepta"
        " negativos)."
    )
  if not arr:
    return arr
  max_val = max(arr)
  exp = 1
  while max_val // exp > 0:
    counting_sort_for_radix(arr, exp)
    exp *= 10
  return arr


# ==========================================
# INTERFAZ GRÁFICA (TKINTER)
# ==========================================
class AppOrdenamiento:

  def __init__(self, root):
    self.root = root
    self.root.title("Simulador de Algoritmos de Ordenamiento")
    self.root.geometry("620x520")
    self.root.config(bg="#f4f6f9")

    # Estilo general
    style = ttk.Style()
    style.theme_use("clam")

    # Título Principal
    titulo = tk.Label(
        root,
        text="Métodos de Ordenamiento en Python",
        font=("Arial", 16, "bold"),
        bg="#f4f6f9",
        fg="#2c3e50",
    )
    titulo.pack(pady=15)

    # Marco de Configuración
    frame_opciones = ttk.LabelFrame(
        root, text=" Parámetros de Entrada ", padding=15
    )
    frame_opciones.pack(fill="x", padx=20, pady=5)

    # Selector de Método
    ttk.Label(
        frame_opciones, text="Método de ordenamiento:", font=("Arial", 10, "bold")
    ).grid(row=0, column=0, sticky="w", pady=8)

    self.combo_metodo = ttk.Combobox(
        frame_opciones,
        values=["ShellSort", "Quicksort", "Heapsort", "Radix Sort"],
        state="readonly",
        width=25,
        font=("Arial", 10),
    )
    self.combo_metodo.grid(row=0, column=1, padx=10, pady=8)
    self.combo_metodo.current(0)

    # Campo de Entrada de Números
    ttk.Label(
        frame_opciones,
        text="Números (separados por espacio):",
        font=("Arial", 10, "bold"),
    ).grid(row=1, column=0, sticky="w", pady=8)

    self.entry_numeros = ttk.Entry(
        frame_opciones, width=28, font=("Arial", 10)
    )
    self.entry_numeros.grid(row=1, column=1, padx=10, pady=8)

    # Marco de Botones de Acción
    frame_botones = tk.Frame(root, bg="#f4f6f9")
    frame_botones.pack(pady=15)

    btn_ordenar = tk.Button(
        frame_botones,
        text="▶ Ejecutar Ordenamiento",
        bg="#27ae60",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=12,
        pady=6,
        relief="flat",
        cursor="hand2",
        command=self.realizar_ordenamiento,
    )
    btn_ordenar.grid(row=0, column=0, padx=8)

    btn_ejemplo = tk.Button(
        frame_botones,
        text="💡 Cargar Ejemplo",
        bg="#2980b9",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=12,
        pady=6,
        relief="flat",
        cursor="hand2",
        command=self.cargar_ejemplo,
    )
    btn_ejemplo.grid(row=0, column=1, padx=8)

    btn_limpiar = tk.Button(
        frame_botones,
        text="🧹 Limpiar",
        bg="#e67e22",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=12,
        pady=6,
        relief="flat",
        cursor="hand2",
        command=self.limpiar_campos,
    )
    btn_limpiar.grid(row=0, column=2, padx=8)

    # Marco de Resultados (Pantalla de consola interna)
    frame_resultados = ttk.LabelFrame(root, text=" Resultado ", padding=15)
    frame_resultados.pack(fill="both", expand=True, padx=20, pady=5)

    self.txt_resultado = tk.Text(
        frame_resultados,
        height=7,
        font=("Consolas", 10),
        bg="#1e1e1e",
        fg="#00ffcc",
        insertbackground="white",
    )
    self.txt_resultado.pack(fill="both", expand=True)

  def cargar_ejemplo(self):
    """Carga un ejemplo predeterminado según el método seleccionado."""
    metodo = self.combo_metodo.get()
    if metodo == "Radix Sort":
      ejemplo = "170 45 75 90 802 24 2 66"
    else:
      ejemplo = "23 11 75 15 36 5"
    self.entry_numeros.delete(0, tk.END)
    self.entry_numeros.insert(0, ejemplo)

  def limpiar_campos(self):
    """Limpia la entrada y la caja de resultados."""
    self.entry_numeros.delete(0, tk.END)
    self.txt_resultado.delete("1.0", tk.END)

  def realizar_ordenamiento(self):
    """Valida los datos y ejecuta el algoritmo seleccionado mostrando el resultado."""
    metodo = self.combo_metodo.get()
    texto_entrada = self.entry_numeros.get().strip()

    if not texto_entrada:
      messagebox.showwarning(
          "Campo Vacío",
          "Por favor ingresa algunos números o usa 'Cargar Ejemplo'.",
      )
      return

    try:
      # Convertir los valores ingresados a una lista de enteros
      numeros = [int(x) for x in texto_entrada.split()]
    except ValueError:
      messagebox.showerror(
          "Error de Formato",
          "Asegúrate de ingresar únicamente números enteros separados por"
          " espacios.",
      )
      return

    # Limpiar pantalla de resultados y mostrar traza
    self.txt_resultado.delete("1.0", tk.END)
    self.txt_resultado.insert(tk.END, f"[*] Método: {metodo}\n")
    self.txt_resultado.insert(tk.END, f"[*] Entrada: {numeros}\n")
    self.txt_resultado.insert(tk.END, "-" * 45 + "\n")

    try:
      if metodo == "ShellSort":
        resultado = shell_sort(numeros)
      elif metodo == "Quicksort":
        resultado = quick_sort(numeros)
      elif metodo == "Heapsort":
        resultado = heap_sort(numeros)
      elif metodo == "Radix Sort":
        resultado = radix_sort(numeros)

      self.txt_resultado.insert(
          tk.END, f"[✔] Ordenado: {resultado}\n", "exito"
      )
    except Exception as e:
      messagebox.showerror("Error de Ejecución", str(e))


if __name__ == "__main__":
  root = tk.Tk()
  app = AppOrdenamiento(root)
  root.mainloop()