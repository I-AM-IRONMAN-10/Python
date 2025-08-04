import tkinter as tk
import time
import threading

class VellaiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vellai - To Do & Focus Timer")
        self.tasks = []

        # To-Do List Frame
        self.task_frame = tk.Frame(root)
        self.task_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.task_frame, width=30)
        self.task_entry.grid(row=0, column=0)
        tk.Button(self.task_frame, text="Add Task", command=self.add_task).grid(row=0, column=1)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        tk.Button(root, text="Delete Selected Task", command=self.delete_task).pack()

        # Focus Timer Frame
        self.timer_label = tk.Label(root, text="25:00", font=("Helvetica", 30))
        self.timer_label.pack(pady=20)

        self.timer_running = False
        tk.Button(root, text="Start Focus Timer", command=self.start_timer).pack()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            self.tasks.pop(selected[0])
            self.listbox.delete(selected[0])

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            threading.Thread(target=self.run_timer).start()

    def run_timer(self):
        total_seconds = 25 * 60
        while total_seconds > 0 and self.timer_running:
            mins, secs = divmod(total_seconds, 60)
            time_str = f"{mins:02}:{secs:02}"
            self.timer_label.config(text=time_str)
            time.sleep(1)
            total_seconds -= 1
        self.timer_label.config(text="Time's up!")
        self.timer_running = False

root = tk.Tk()
app = VellaiApp(root)
root.mainloop()