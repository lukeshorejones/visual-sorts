import sorts
import tkinter as tk
import tkinter.ttk as ttk
import colorsys
import math
import random


class GUI:
    def __init__(self, master):
        self.master = master

        default_list_size = 50
        padding = 4
        self.canvas_size = (600, 600)

        self.numbers = []
        self.colours = []

        self.sort_index_0 = 0
        self.sort_index_0_2 = 0
        self.sort_index_1 = 1
        self.pass_swaps = 0
        self.min_i = 0
        self.ordered = True
        self.sublist_end = 2
        self.left = []
        self.right = []
        self.merge = []

        self.comparisons = 0
        self.swaps = 0
        self.compared = None
        self.swapped = None

        self.bar_width = 1
        self.bar_height = 0
        self.sorting = False

        self.master.title("Visual Sorts")

        favicon = tk.PhotoImage(file="favicon.gif")
        self.master.tk.call("wm", "iconphoto", self.master._w, favicon)

        self.algorithms = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Bogosort", "Bogobogosort"]
        self.algorithm = tk.StringVar(self.master)
        self.algorithm.set(self.algorithms[0])

        self.list_types = ["Distributed", "Random"]
        self.list_type = tk.StringVar(self.master)
        self.list_type.set(self.list_types[0])

        self.displays = ["Bars (Black on White)", "Bars (White on Black)", "Bars (Coloured)", "Colours"]
        self.display = tk.StringVar(self.master)
        self.display.set(self.displays[0])

        self.pause_text = tk.StringVar(self.master)
        self.pause_text.set("Play")

        self.bottom_text_content = tk.StringVar(self.master)
        self.bottom_text_content.set("")
        self.status = ""

        self.canvas = tk.Canvas(width=self.canvas_size[0], height=self.canvas_size[1], bg='white')
        self.title_text = tk.Label(self.master, text="Options", font=("Arial", 10))
        self.separator = ttk.Separator(self.master)
        self.algorithm_text = tk.Label(self.master, text="Algorithm")
        self.algorithm_menu = tk.OptionMenu(self.master, self.algorithm, *tuple(self.algorithms))
        self.list_type_text = tk.Label(self.master, text="List Type")
        self.list_type_menu = tk.OptionMenu(self.master, self.list_type, *tuple(self.list_types))
        self.list_size_text = tk.Label(self.master, text="List Size")
        self.list_size = tk.Scale(self.master, from_=2, to=self.canvas_size[0], orient=tk.HORIZONTAL, length=151)
        self.display_text = tk.Label(self.master, text="Display")
        self.display_menu = tk.OptionMenu(self.master, self.display, *tuple(self.displays))
        self.delay_text = tk.Label(self.master, text="Delay (s)")
        self.delay = tk.Scale(self.master, from_=0.001, to=0.5, resolution=0.001, orient=tk.HORIZONTAL, length=151)
        self.pause_button = tk.Button(self.master, textvariable=self.pause_text, command=self.toggle_pause, width=9)
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset, width=9)
        self.bottom_text = tk.Label(self.master, textvariable=self.bottom_text_content, anchor=tk.NW, justify=tk.LEFT, relief=tk.GROOVE, padx=padding, pady=padding)
        self.bottom_frame = tk.Frame()

        self.list_size.set(default_list_size)
        self.delay.set(0.001)

        self.canvas.grid(row=1, column=0, padx=padding, pady=padding, rowspan=9, sticky=tk.N+tk.W)
        self.title_text.grid(row=1, column=1, columnspan=3, padx=padding, pady=(padding, 0), sticky=tk.W)
        self.separator.grid(row=2, column=1, columnspan=3, padx=padding, pady=(0, padding), sticky=tk.W+tk.E)
        self.algorithm_text.grid(row=3, column=1, padx=padding, pady=padding, sticky=tk.W)
        self.algorithm_menu.grid(row=3, column=2, columnspan=2, padx=padding, pady=padding, sticky=tk.W)
        self.list_type_text.grid(row=4, column=1, padx=padding, pady=padding, sticky=tk.W)
        self.list_type_menu.grid(row=4, column=2, columnspan=2, padx=padding, pady=padding, sticky=tk.W)
        self.list_size_text.grid(row=5, column=1, padx=padding, pady=padding, sticky=tk.W)
        self.list_size.grid(row=5, column=2, columnspan=2, padx=padding, pady=padding, sticky=tk.W)
        self.display_text.grid(row=6, column=1, padx=padding, pady=padding, sticky=tk.W)
        self.display_menu.grid(row=6, column=2, columnspan=2, padx=padding, pady=padding, sticky=tk.W)
        self.delay_text.grid(row=7, column=1, padx=padding, pady=padding, sticky=tk.W)
        self.delay.grid(row=7, column=2, columnspan=2, padx=padding, pady=padding, sticky=tk.W)
        self.pause_button.grid(row=8, column=2, padx=padding, pady=padding, sticky=tk.W)
        self.reset_button.grid(row=8, column=3, padx=padding, pady=padding, sticky=tk.W)
        self.bottom_text.grid(row=9, column=1, columnspan=3, padx=padding, pady=padding, sticky=tk.N+tk.S+tk.E+tk.W)
        self.bottom_frame.grid(row=10, column=0, columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W)

        self.master.grid_rowconfigure(9, weight=1)
        self.master.grid_rowconfigure(10, weight=999)

        self.new()

    def new(self):
        if self.list_type.get() == "Distributed":
            self.numbers = list(range(1, self.list_size.get() + 1))
            random.shuffle(self.numbers)
            self.bar_height = self.canvas_size[1] / self.list_size.get()

        elif self.list_type.get() == "Random":
            min_value = 1
            max_value = 50

            self.numbers = []
            for i in range(self.list_size.get()):
                self.numbers.append(random.randint(min_value, max_value))
            self.bar_height = self.canvas_size[1] / max_value

        self.bar_width = max(math.floor(self.canvas_size[0] / len(self.numbers)), 1)

        self.colours = []
        for i in range(self.list_size.get()):
            colour = list(colorsys.hsv_to_rgb(i / self.list_size.get(), 1, 1))
            for j in range(len(colour)):
                colour[j] = int(colour[j] * 255)
            self.colours.append("#%02x%02x%02x" % tuple(colour))

        self.status = "Press Play to start sorting."
        self.sort_index_0 = 0
        self.sort_index_0_2 = 0
        self.sort_index_1 = 1
        self.pass_swaps = 0
        self.min_i = 0
        self.ordered = True
        self.sublist_end = 2
        self.left = []
        self.right = []
        self.merge = []

        self.comparisons = 0
        self.swaps = 0
        self.compared = None
        self.swapped = None

        self.bottom_text_content.set(self.status + "\n\nComparisons: " + str(self.comparisons) + "\nSwaps: " + str(self.swaps))
        self.draw(self.numbers)

    def run(self):
        if self.sorting:
            self.sort()
            if not self.sorting:
                self.pause_text.set('Play')
                self.status = "Done! Press Play to sort again."
                self.algorithm_menu.config(state=tk.NORMAL)
                self.list_type_menu.config(state=tk.NORMAL)
                self.list_size.config(state=tk.NORMAL)

            self.draw(self.numbers)
            self.bottom_text_content.set(self.status + "\n\nComparisons: " + str(self.comparisons) + "\nSwaps: " + str(self.swaps))

        delay_time = int(self.delay.get() * 1000)
        self.master.after(delay_time, self.run)

    def sort(self):
        if self.algorithm.get() == "Bubble Sort":
            self.numbers, self.sort_index_0, self.pass_swaps, self.comparisons, self.swaps, self.compared, self.swapped, self.sorting = sorts.bubble_sort(
                self.numbers,
                self.sort_index_0,
                self.pass_swaps,
                self.comparisons,
                self.swaps,
            )

        elif self.algorithm.get() == "Selection Sort":
            self.numbers, self.sort_index_0, self.sort_index_0_2, self.min_i, self.comparisons, self.swaps, self.compared, self.swapped, self.sorting = sorts.selection_sort(
                self.numbers,
                self.sort_index_0,
                self.sort_index_0_2,
                self.min_i,
                self.comparisons,
                self.swaps,
            )

        elif self.algorithm.get() == "Insertion Sort":
            self.numbers, self.sort_index_0, self.sort_index_1, self.comparisons, self.swaps, self.compared, self.swapped, self.sorting = sorts.insertion_sort(
                self.numbers,
                self.sort_index_0,
                self.sort_index_1,
                self.comparisons,
                self.swaps,
            )

        elif self.algorithm.get() == "Merge Sort":
            self.numbers, self.sort_index_1, self.sort_index_0, self.sublist_end, self.left, self.right, self.merge, self.comparisons, self.swaps, self.compared, self.swapped, self.sorting = sorts.merge_sort(
                self.numbers,
                self.sort_index_1,
                self.sort_index_0,
                self.sublist_end,
                self.left,
                self.right,
                self.merge,
                self.comparisons,
                self.swaps
            )

        elif self.algorithm.get() == "Bogosort":
            self.numbers, self.sort_index_1, self.ordered, self.comparisons, self.swaps, self.compared, self.sorting = sorts.bogosort(
                self.numbers,
                self.sort_index_1,
                self.ordered,
                self.comparisons,
                self.swaps,
            )

        elif self.algorithm.get() == "Bogobogosort":
            self.numbers, self.sublist_end, self.sort_index_1, self.ordered, self.comparisons, self.swaps, self.compared, self.sorting = sorts.bogobogosort(
                self.numbers,
                self.sublist_end,
                self.sort_index_1,
                self.ordered,
                self.comparisons,
                self.swaps,
            )

    def draw(self, sublist):
        self.canvas.delete('all')

        if self.display.get() == "Colours":
            self.canvas.config(bg="white")
            for i in range(len(sublist)):
                self.canvas.create_line(
                    (i + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2, (i + 0.5) * self.bar_width + 2, 2,
                    width=self.bar_width, fill=self.colours[sublist[i] - 1]
                )

        if self.display.get() == "Bars (Black on White)":
            if self.sorting:
                if self.compared is not None:
                    self.canvas.create_line(
                        (self.compared[0] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.compared[0] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#00FFFF"
                    )
                    self.canvas.create_line(
                        (self.compared[1] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.compared[1] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#00FFFF"
                    )

                if self.swapped is not None:
                    self.canvas.create_line(
                        (self.swapped[0] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.swapped[0] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#00FF00"
                    )
                    self.canvas.create_line(
                        (self.swapped[1] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.swapped[1] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#00FF00"
                    )

            self.canvas.config(bg="white")
            for i in range(len(sublist)):
                self.canvas.create_line(
                    (i + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2, (i + 0.5) * self.bar_width + 2,
                    self.canvas_size[1] - (sublist[i] * self.bar_height) + 2, width=self.bar_width
                )

        elif self.display.get() == "Bars (White on Black)":
            if self.sorting:
                if self.compared is not None:
                    self.canvas.create_line(
                        (self.compared[0] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.compared[0] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#008080"
                    )
                    self.canvas.create_line(
                        (self.compared[1] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.compared[1] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#008080"
                    )

                if self.swapped is not None:
                    self.canvas.create_line(
                        (self.swapped[0] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.swapped[0] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#008000"
                    )
                    self.canvas.create_line(
                        (self.swapped[1] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.swapped[1] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#008000"
                    )

            self.canvas.config(bg="black")
            for i in range(len(sublist)):
                self.canvas.create_line(
                    (i + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2, (i + 0.5) * self.bar_width + 2,
                    self.canvas_size[1] - (sublist[i] * self.bar_height) + 2, width=self.bar_width, fill="white"
                )

        elif self.display.get() == "Bars (Coloured)":
            if self.sorting:
                if self.compared is not None:
                    self.canvas.create_line(
                        (self.compared[0] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.compared[0] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#000000"
                    )
                    self.canvas.create_line(
                        (self.compared[1] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.compared[1] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#000000"
                    )

                if self.swapped is not None:
                    self.canvas.create_line(
                        (self.swapped[0] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.swapped[0] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#C0C0C0"
                    )
                    self.canvas.create_line(
                        (self.swapped[1] + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2,
                        (self.swapped[1] + 0.5) * self.bar_width + 2, 2, width=self.bar_width,
                        fill="#C0C0C0"
                    )

            self.canvas.config(bg="white")
            for i in range(len(sublist)):
                self.canvas.create_line(
                    (i + 0.5) * self.bar_width + 2, self.canvas_size[1] + 2, (i + 0.5) * self.bar_width + 2,
                    self.canvas_size[1] - (sublist[i] * self.bar_height) + 2, width=self.bar_width,
                    fill=self.colours[sublist[i] - 1]
                )

    def reset(self):
        self.set_sorting(False)
        self.algorithm_menu.config(state=tk.NORMAL)
        self.list_type_menu.config(state=tk.NORMAL)
        self.list_size.config(state=tk.NORMAL)
        self.new()

    def toggle_pause(self):
        self.set_sorting(not self.sorting)
        if self.sorting:
            if self.status == "Done! Press Play to sort again.":
                self.sort_index_0 = 0
                self.sort_index_0_2 = 0
                self.sort_index_1 = 1
                self.pass_swaps = 0
                self.min_i = 0
                self.ordered = True
                self.sublist_end = 2
                self.left = []
                self.right = []
                self.merge = []

                self.comparisons = 0
                self.swaps = 0
                self.compared = None
                self.swapped = None
            self.status = "Sorting..."
        else:
            self.status = "Paused. Reset to configure sort."

        self.bottom_text_content.set(self.status + "\n\nComparisons: " + str(self.comparisons) + "\nSwaps: " + str(self.swaps))

    def set_sorting(self, s):
        self.sorting = s
        if self.sorting:
            self.pause_text.set("Pause")
            self.algorithm_menu.config(state=tk.DISABLED)
            self.list_type_menu.config(state=tk.DISABLED)
            self.list_size.config(state=tk.DISABLED)
        else:
            self.pause_text.set("Play")


def main():
    root = tk.Tk()
    gui = GUI(root)
    root.after(0, gui.run)
    root.mainloop()


if __name__ == '__main__':
    main()
