import tkinter as tk

class FrameScroll(tk.Frame):

    def __init__(self, master, **kwargs):

        bg_color = kwargs.get("bg", kwargs.get("background", "#1e1e1e"))

        super().__init__(master, bg=bg_color)

        self.canvas = tk.Canvas(self, highlightthickness=0, bg=bg_color)

        self.scroll = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scroll.set
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

        self.interior = tk.Frame(self.canvas, **kwargs)

        self.canvas_window = self.canvas.create_window(
            (0,0),
            window=self.interior,
            anchor="nw"
        )

        self.interior.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )