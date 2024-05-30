import tkinter as tk
from tkinter import filedialog

#from pynput.mouse import Listener
#
# class GUI:
#
#     def __init__(self):
#         self.startup_window = tk.Tk()
#         self.startup_window.title("Start menu")
#
#         label = tk.Label(text="Welcome to ScreenScanner! \n\n To start, please click the setup button, select a region to scan, and select an image to scan for.")
#         label.pack()
#
#         buttons = tk.Frame(self.startup_window)
#         buttons.pack(pady=5)
#
#         setup_button = tk.Button(
#             buttons,
#             text="Setup",
#             width=25,
#             height=5,
#             bg="blue",
#             fg="yellow",
#             command=self.open_setup_menu,
#         )
#
#         activate_button = tk.Button(
#             buttons,
#             text="Activate Scanning",
#             width=25,
#             height=5,
#             bg="blue",
#             fg="yellow",
#         )
#         setup_button.pack(side="left")
#         activate_button.pack()
#
#         self.startup_window.mainloop()
#
#     def open_setup_menu(self):
#         setup_window = tk.Toplevel(self.startup_window)
#         setup_window.transient(self.startup_window)
#         setup_window.title("Setup Window")
#         return
#
#
#

LARGE_FONT = ("Verdana", 12)


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
        label = tk.Label(self, text="Welcome to ScreenScanner! \n\n To start, please click the setup button, select a region to scan, and select an image to scan for.", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        buttons = tk.Frame(self)
        buttons.pack(pady=5)

        setup_button = tk.Button(buttons, text="Setup Page",
                           width=15,
                           height=5,
                           bg="blue",
                           fg="yellow",
                           command=lambda: controller.show_frame(SetupPage))
        setup_button.pack(side="left")

        scan_button = tk.Button(buttons, text="Start Scanning",
                            width=15,
                            height=5,
                            bg="blue",
                            fg="yellow",
                            command=lambda: controller.show_frame(MonitoringPage))
        scan_button.pack()


class SetupPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        intro_label = tk.Label(self, text="First, please select a region of the screen to scan. \n Then, please upload or screencap the image to scan for.", font=LARGE_FONT)
        intro_label.pack(pady=10, padx=10)

        region_label = tk.Label(self, text="Region to scan:", font=LARGE_FONT)
        region_label.pack(pady=10, padx=10)


        size_entries = tk.Frame(self)
        size_entries.pack(pady=5)
        top_var = tk.StringVar()
        left_var = tk.StringVar()
        width_var = tk.StringVar()
        height_var = tk.StringVar()
        top_label = tk.Label(size_entries, text="top:", font=LARGE_FONT)
        top_label.grid(row=0, column=0)
        top_entry = tk.Entry(size_entries, textvariable=top_var, font=('calibre', 10, 'normal'), width=5)
        top_entry.grid(row=0, column=1)

        left_label = tk.Label(size_entries, text="left:", font=LARGE_FONT)
        left_label.grid(row=0, column=2)
        left_entry = tk.Entry(size_entries, textvariable=left_var, font=('calibre', 10, 'normal'), width=5)
        left_entry.grid(row=0, column=3)

        width_label = tk.Label(size_entries, text="width:", font=LARGE_FONT)
        width_label.grid(row=0, column=4)
        width_entry = tk.Entry(size_entries, textvariable=width_var, font=('calibre', 10, 'normal'), width=5)
        width_entry.grid(row=0, column=5)

        height_label = tk.Label(size_entries, text="height:", font=LARGE_FONT)
        height_label.grid(row=0, column=6)
        height_entry = tk.Entry(size_entries, textvariable=height_var, font=('calibre', 10, 'normal'), width=5)
        height_entry.grid(row=0, column=7)
        submit_button = tk.Button(size_entries, text="Update")
        submit_button.grid(row=0, column=8)

        buttons = tk.Frame(self)
        buttons.pack(pady=5)

        add_button = tk.Button(buttons, text="Add scan",
                                 width=15,
                                 height=5,
                                 bg="blue",
                                 fg="yellow",
                                 command=lambda: controller.show_frame(AddScanPage))
        add_button.pack(side="left")

        scan_button = tk.Button(buttons, text="Remove scan",
                                width=15,
                                height=5,
                                bg="blue",
                                fg="yellow",
                                command=lambda: controller.show_frame(RemoveScanPage))
        scan_button.pack()

        home_button = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        home_button.pack()


class MonitoringPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        top_var = tk.StringVar()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(SetupPage))
        button2.pack()


class AddScanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Please select a title and image location", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        adding_frame = tk.Frame(self)
        adding_frame.pack(pady=5)
        title_var = tk.StringVar()
        title_label = tk.Label(adding_frame, text="Title:", font=LARGE_FONT)
        title_label.grid(row=0, column=0)
        title_entry = tk.Entry(adding_frame, textvariable=title_var, font=('calibre', 20, 'normal'), width=10)
        title_entry.grid(row=0, column=1)
        add_image_button = tk.Button(adding_frame, text="Add image",
                               width=15,
                               height=5,
                               bg="blue",
                               fg="yellow",
                               command=self.import_file)

        add_image_button.grid(row=0, column=2)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Back to Setup",
                            command=lambda: controller.show_frame(SetupPage))
        button2.pack()
    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            # Process the selected file (you can replace this with your own logic)
            print("Selected file:", file_path)


class RemoveScanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(SetupPage))
        button2.pack()


app = GUI()
app.mainloop()