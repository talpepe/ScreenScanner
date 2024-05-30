import tkinter as tk
from tkinter import filedialog, messagebox

from screen_scanner import ScreenScanner
from template_handler import TemplateHandler

LARGE_FONT = ("Verdana", 12)
monitor = {"top": 0, "left": 2500, "width": 900, "height": 300}
class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SetupPage, MonitoringPage, AddScanPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to ScreenScanner! \n\nTo start, please click the setup button, select a region to scan, and select an image to scan for.", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        buttons = tk.Frame(self)
        buttons.pack(pady=5)

        setup_button = tk.Button(buttons, text="Setup Page", width=15, height=2, command=lambda: controller.show_frame(SetupPage))
        setup_button.pack(side="left", padx=5)

        scan_button = tk.Button(buttons, text="Start Scanning", width=15, height=2, command=lambda: controller.show_frame(MonitoringPage))
        scan_button.pack(side="left", padx=5)


class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        intro_label = tk.Label(self, text="First, please select a region of the screen to scan. \nThen, please upload or screencap the image to scan for.", font=LARGE_FONT)
        intro_label.pack(pady=10, padx=10)

        region_label = tk.Label(self, text="Region to scan:", font=LARGE_FONT)
        region_label.pack(pady=10, padx=10)

        size_entries = tk.Frame(self)
        size_entries.pack(pady=5)

        self.top_var = tk.StringVar()
        self.left_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()

        labels = ["top:", "left:", "width:", "height:"]
        vars = [self.top_var, self.left_var, self.width_var, self.height_var]

        for i, (label_text, var) in enumerate(zip(labels, vars)):
            tk.Label(size_entries, text=label_text, font=LARGE_FONT).grid(row=0, column=i*2)
            tk.Entry(size_entries, textvariable=var, font=('calibre', 10, 'normal'), width=5).grid(row=0, column=i*2 + 1)

        submit_button = tk.Button(size_entries, text="Update", command=self.update_region)
        submit_button.grid(row=0, column=len(labels) * 2)

        buttons = tk.Frame(self)
        buttons.pack(pady=5)

        add_button = tk.Button(buttons, text="Add scan", width=15, height=2, command=lambda: controller.show_frame(AddScanPage))
        add_button.pack(side="left", padx=5)

        remove_button = tk.Button(buttons, text="Remove scan", width=15, height=2, command=lambda: controller.show_frame(RemoveScanPage))
        remove_button.pack(side="left", padx=5)

        home_button = tk.Button(self, text="Back to Home", width=15, height=2, command=lambda: controller.show_frame(StartPage))
        home_button.pack(pady=5)

    def update_region(self):
        try:
            top = int(self.top_var.get())
            left = int(self.left_var.get())
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            #{"top": 0, "left": 2500, "width": 900, "height": 300}
            monitor.update({"top": top})
            monitor.update({"left": left})
            monitor.update({"width": width})
            monitor.update({"height": height})
            # Save the region settings somewhere or process them as needed
            print(f"Updated region: top={top}, left={left}, width={width}, height={height}")
            messagebox.showinfo("Info", "Region updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for the region dimensions.")


class MonitoringPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Monitoring in progress...", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button0 = tk.Button(self, text="Start Monitoring", width=15, height=2, command=lambda: self.initiate_scanning())
        button0.pack(pady=5)

        button1 = tk.Button(self, text="Back to Home", width=15, height=2, command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=5)

        button2 = tk.Button(self, text="Back to Setup", width=15, height=2, command=lambda: controller.show_frame(SetupPage))
        button2.pack(pady=5)

    def initiate_scanning(self):
        scanner = ScreenScanner(templates_handler.get_templates(), monitor)
        scanner.start_scanning()


class AddScanPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Please select a title and image location", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.image_path = None
        adding_frame = tk.Frame(self)
        adding_frame.pack(pady=5)
        title_var = tk.StringVar()
        title_label = tk.Label(adding_frame, text="Title:", font=LARGE_FONT)
        title_label.grid(row=0, column=0)
        title_entry = tk.Entry(adding_frame, textvariable=title_var, font=('calibre', 10, 'normal'), width=20)
        self.image_title = title_entry.get()
        title_entry.grid(row=0, column=1)

        add_image_button = tk.Button(adding_frame, text="Add image", width=15, height=2, command=lambda: self.import_image())
        add_image_button.grid(row=0, column=2)

        add_to_monitoring_button = tk.Button(adding_frame, text="Add to monitoring", width=15, height=2, command=lambda: self.add_template(self.image_path, title_entry.get()))
        add_to_monitoring_button.grid(row=0, column=3)

        button1 = tk.Button(self, text="Back to Home", width=15, height=2, command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=5)

        button2 = tk.Button(self, text="Back to Setup", width=15, height=2, command=lambda: controller.show_frame(SetupPage))
        button2.pack(pady=5)

    def import_image(self):
        image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("PNG","*.png"),("JPG","*.jpg"),("JPEG","*.jpeg")])
        if image_path:
            # Process the selected file (you can replace this with your own logic)
            print("Selected image:", image_path)
            self.image_path = image_path

    def add_template(self, image_path, image_title):
        if image_path and image_title:
            templates_handler.add_template(image_path, image_title)
            print("template added", image_path, image_title)
            self.image_path = None



class RemoveScanPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Remove scan page (Under construction)", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home", width=15, height=2, command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=5)

        button2 = tk.Button(self, text="Back to Setup", width=15, height=2, command=lambda: controller.show_frame(SetupPage))
        button2.pack(pady=5)


if __name__ == "__main__":
    templates_handler = TemplateHandler()
    app = GUI()
    app.mainloop()
