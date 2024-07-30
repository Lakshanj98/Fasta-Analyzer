"""
Author : Lakshan Jayasinghe
Date: 23.04.2023
Project: FASTA processor
Inputs: Single, multiple or a multi-fasta file depending on the method.
Outputs: Single, multiple or a multi-fasta file depending on the method.
  Description:    This program is designed with a simple GUI and methods
            to do the common day-to-day tasks needed by Bio-informaticians c
            while working with FASTA sequences.
"""
# import necessary packages
import tkinter as tk
from tkinter import filedialog
# import tkinter.filedialog as fdg
import os
from tkinter import messagebox


class Fasta:

    def __init__(self):
        self.file_name = ""
        self.file_names = ""
        self.sequence_dictionary = {}

    """------------------------------------------------- basic methods -----------------------------------------"""

    def select_file(self):
        """   method to select a fasta file       """

        # Clear the output on the label
        label1.config(text="")

        self.file_name = filedialog.askopenfilename()

        if self.file_name == "":
            return "invalid"
        elif self.file_name.split(".")[-1] != "fasta":
            return "invalid"

    def select_files(self):
        """    method to select multiple fasta files   """

        # Clear the output on the label
        label1.config(text="")

        self.file_names = filedialog.askopenfilenames()

        if self.file_names == "":
            return "invalid"
        for file_name in self.file_names:
            if file_name.split(".")[-1] != "fasta":
                return "invalid"
        """If the user has chosen only one sequence,
                ask user to select multiple files """
        if len(self.file_names) == 1:
            messagebox.showerror("Input Error", "Please select more than one fasta file")
            return "invalid"

    def separate_header_and_sequence(self, file_name):
        """
        This method reads the given fasta file.
        Separates all headers and sequences and
        add them to the sequence dictionary.
        """

        # create necessary variables
        Header = ""
        sequence = ""

        # reading the multi fasta file
        with open(file_name, "r") as file:
            for line in file:
                # if the line not empty
                if line != "\n":
                    line = line.strip()
                    # separating header and sequence
                    if ">" in line:
                        Header = line
                        sequence = ""
                    else:
                        sequence += line
                    # inserting every fasta  header and sequence(uppercase) into sequence_dictionary.
                    self.sequence_dictionary[Header] = sequence.upper()

    def create_fasta_file_name(self, Header):
        """ Headers with ">" and ":" cause errors when tried to create files including them.
            This method removes >,: and split the header using whitespaces.
            This method splits filepaths using "/".
            Then it creates the output path and fasta file's name.
            """

        if "/" in Header:
            # This means the parameter passed by the name
            # of Header is a filepath. It contains "/" to indicate directories

            # splitting the header using forward slash.
            new_file_name = Header.split("/")

            # using only the accession number as file name
            fasta_file_name = "Output/" + new_file_name[-1]
        else:
            # If "/" is not found, this parameter passed by the name
            # of Header is actually a fasta header.
            # remove ">" from header
            Head = Header.strip(">")
            # remove any colons
            Head = Head.replace(":", " ")

            # splitting the header using whitespaces
            new_file_name = Head.split(" ")

            # using only the accession number as file name
            fasta_file_name = "Output/" + new_file_name[0] + ".fasta"

        return fasta_file_name

    def get_sequence_type(self, sequence):
        """
        This method checks whether the given
        sequence in sequence dictionary is protein, RNA or DNA.
        """

        amino_acids = ["K", "N", "R", "S", "I", "M", "Q", "H", "P", "R", "L", "E", "D", "V", "Y", "S", "W", "F"]
        # sequence_type = ""

        # checking a base in sequence
        for base in sequence:

            """ If the base is in amino acids list, it is a protein."""
            if base in amino_acids:
                sequence_type = "protein"
                return sequence_type

            elif base == "U":
                """ If the base is U, it is mRNA."""
                sequence_type = "RNA"
                return sequence_type

            else:
                """ If both above conditions aren't met, it is DNA."""
                sequence_type = "DNA"
                return sequence_type

    """  -------------------------------------  main methods ------------------------------------------------ """

    def split_multi_Fasta_file(self):
        """
        This method splits a given single multi-Fasta file into separate fasta files
         containing one sequence in each.
        """

        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # writing Fasta sequences in dictionary to separate files.
        for Header in self.sequence_dictionary:
            """ get the fasta file name"""
            fasta_file_name = self.create_fasta_file_name(Header)

            with open(fasta_file_name, "w") as file:
                # writing the header and sequence.
                file.writelines(Header + "\n")
                file.writelines(self.sequence_dictionary[Header] + "\n")

        """ display a confirmation message about the task completion"""
        messagebox.showinfo("Task completed!", "Please check Output folder")

    def number_of_Fasta_sequences(self):
        """
        This method calculates the number of fasta sequences
        in a given multi fasta file.
        """
        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # Display the number of fasta sequences on the label
        number_of_fasta_sequences = len(self.sequence_dictionary)
        label1.config(text="Number of fasta sequences: " + str(number_of_fasta_sequences))

    def combine_multiple_Fasta_files(self):
        """
        This method reads a multiple fasta files  and
        combine the sequences into a multi-fasta file.
        """
        # call the files selecting method but, abort running method if returns invalid.
        if self.select_files() == "invalid":
            return

        # access the selected file list
        for filepath in self.file_names:
            # select one file at a time
            # calling the separate_header_and_sequence method to read the fasta file.
            self.separate_header_and_sequence(filepath)

        # create a new fasta file.
        with open("Output/multifasta file.fasta", "w") as file:

            # writing all fasta headers and sequences to the multi-fasta file.
            for Header in self.sequence_dictionary:
                file.writelines(Header + "\n")
                file.writelines(self.sequence_dictionary[Header] + "\n")

        """ display a confirmation message about the task completion"""
        messagebox.showinfo("Task completed!", "Please check Output folder")


class Sequence(Fasta):

    def remove_unwanted_from_nucleotide(self):
        """
        This method removes unwanted characters from fasta nucleotide sequences
        and write them into separate fasta files.
        """
        bases = ["A", "T", "G", "C", "U"]
        cleansequence = ""

        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # select the header of one sequence
        for Header in self.sequence_dictionary:
            sequence = self.sequence_dictionary[Header]

            # checking sequence base by base for unknown characters
            for base in sequence:
                if base in bases:
                    cleansequence += base
                else:
                    cleansequence += ""

            """ get the fasta file name"""
            fasta_file_name = self.create_fasta_file_name(Header)

            # writing the clean sequence with its header to a fasta file.
            with open(fasta_file_name, "w") as file:
                file.writelines(Header + "\n")
                file.writelines(cleansequence + "\n")

        """ display a confirmation message about the task completion"""
        messagebox.showinfo("Task completed!", "Please check Output folder")

    def remove_unwanted_from_protein(self):
        """
        This method removes unwanted characters from fasta protein sequences
        and write them into separate fasta files.
        """
        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # select the header of a sequence
        for Header in self.sequence_dictionary:
            sequence = self.sequence_dictionary[Header]
            # replace unknown characters
            sequence = sequence.replace("X", "")

            """ get the fasta file name"""
            fasta_file_name = self.create_fasta_file_name(Header)

            # writing the clean sequence with its header to a fasta file.
            with open(fasta_file_name, "w") as file:
                file.writelines(Header + "\n")
                file.writelines(sequence + "\n")

        """ display a confirmation message about the task completion"""
        messagebox.showinfo("Task completed!", "Please check Output folder")

    def add_sequence_length_to_header(self):

        """
        This method to calculates and append the length
        of an input FASTA sequence to its FASTA header.
        """
        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # select the header of a sequence
        for Header in self.sequence_dictionary:
            sequence = self.sequence_dictionary[Header]

            # calculating sequence length
            length = len(sequence)

            # set up unit of length based on the sequence type
            if self.get_sequence_type(sequence) == "protein":
                unit = " aa"
            else:
                unit = " bp"

            """ get the fasta file name"""
            fasta_file_name = self.create_fasta_file_name(Header)

            # writing the sequence length appended header and sequence to a fasta file
            with open(fasta_file_name, "w") as file:
                file.writelines(Header + ", sequence length " + str(length) + unit + "\n")
                file.writelines(sequence + "\n")

        """ display a confirmation message about the task completion"""
        messagebox.showinfo("Task completed!", "Please check Output folder")

    def add_sequence_lengths_to_headers(self):

        """
        This method uses a multi-fasta file as the input,
        calculates and appends the length of each sequence to the respective FASTA header
         and write them into a new multi-fasta file.
        """

        sequence_length_dictionary = {}

        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # select the header of a sequence
        for Header in self.sequence_dictionary:
            sequence = self.sequence_dictionary[Header]

            # calculating sequence length
            length = len(sequence)

            # set up unit of length based on the sequence type
            if self.get_sequence_type(sequence) == "protein":
                unit = " aa"
            else:
                unit = " bp"

            # creating new header with the sequence length
            new_header = Header + ", sequence length " + str(length) + unit

            # insert new headers and sequences to a dictionary.
            sequence_length_dictionary[new_header] = sequence

        """ get the fasta file name"""
        fasta_file_name = self.create_fasta_file_name(self.file_name)

        # writing the sequence length appended header and sequence to a multi-fasta file
        with open(fasta_file_name, "w") as file:

            # write one sequence at a time
            for new_header in sequence_length_dictionary:
                file.writelines(new_header + "\n")
                file.writelines(sequence_length_dictionary[new_header] + "\n")

        """ display a confirmation message about the task completion"""
        messagebox.showinfo("Task completed!", "Please check Output folder")

    def get_AT_content(self):
        """
        This method calculates the AT content of a given nucleotide sequence.
        Then, writes the AT content added header, and sequence to a new fasta file.
        """
        bases = ["A", "T", "U"]
        AT_count = 0
        count = 0

        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # checking whether the file has more than one sequence.
        number_of_sequences = len(self.sequence_dictionary)
        if number_of_sequences > 1:
            messagebox.showerror("Sequence Number Error", "Please select one nucleotide sequence to calculate AT "
                                                          "content")
            return
        else:
            # selecting one header
            for Header in self.sequence_dictionary:
                sequence = self.sequence_dictionary[Header]
                # if the sequence is a protein,
                # display a sequence type error and exit the method.
                if self.get_sequence_type(sequence) == "protein":
                    messagebox.showerror("Sequence Type Error", "Please select a nucleotide sequence to calculate AT "
                                                                "content")
                    return

                else:
                    # counting sequence length
                    for base in sequence:
                        count += 1
                        # counting AT count
                        if base in bases:
                            AT_count += 1
                    """ calculate the AT content"""
                    AT_content = AT_count / count

                    # Display the output on the label
                    label1.config(text="AT content: " + str(round(AT_content, 2)))

    def get_GC_content(self):
        """
        This method calculates the GC content of a given fasta nucleotide sequence.
        Then, writes the GC content added header, and sequence to a new fasta file.
        """

        bases = ["G", "C"]
        GC_count = 0
        count = 0

        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # checking whether the file has more than one sequence.
        number_of_sequences = len(self.sequence_dictionary)
        if number_of_sequences > 1:
            messagebox.showerror("Sequence Number Error", "Please select one nucleotide sequence to calculate GC "
                                                          "content")
            return
        else:
            # selecting one header
            for Header in self.sequence_dictionary:
                sequence = self.sequence_dictionary[Header]
                # if the sequence is a protein,
                # display a sequence type error and exit the method.
                if self.get_sequence_type(sequence) == "protein":
                    messagebox.showerror("Sequence Type Error", "Please select a nucleotide sequence to calculate GC "
                                                                "content")
                    return

                else:
                    # counting sequence length
                    for base in self.sequence_dictionary[Header]:
                        count += 1
                        # counting AT count
                        if base in bases:
                            GC_count += 1
                    """ calculate the GC content"""
                    GC_content = GC_count / count

                    # Display the output on the label
                    label1.config(text="GC content: " + str(round(GC_content, 2)))

    def add_content_to_header_and_write(self, content_type, sequence_type):
        """
        This method calculates and append the AT or GC content of an input DNA or RNA FASTA sequence
         and append it to the FASTA header.
         Then write it to a new fasta file.
        """
        # declare the necessary variables
        bases = []
        content_name = ""

        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # adjust bases list according to the content type and sequence type
        if content_type.get() == "AT" and sequence_type.get() == "DNA":
            bases.extend(["A", "T"])
            content_name = "AT content: "

        elif content_type.get() == "GC" and (sequence_type.get() == "DNA" or sequence_type.get() == "RNA"):
            bases.extend(["G", "C"])
            content_name = "GC content: "

        elif content_type.get() == "AT" and sequence_type.get() == "RNA":
            bases.extend(["A", "U"])
            content_name = "AT content: "

        for Header in self.sequence_dictionary:
            # if the sequence is a protein,
            # display a sequence type error and exit the method.
            if self.get_sequence_type(self.sequence_dictionary[Header]) == "protein":
                messagebox.showerror("Sequence Type Error", "Please select nucleotide sequences to calculate AT/GC "
                                                            "content")
                return

            else:
                count = 0
                content_count = 0
                for base in self.sequence_dictionary[Header]:
                    # calculate the sequence length
                    count += 1
                    # counting content count
                    if base in bases:
                        content_count += 1

                """ calculate the AT content"""
                content = content_count / count

                """ get the fasta file name"""
                fasta_file_name = self.create_fasta_file_name(Header)

                # writing the sequence length appended header and sequence to a fasta file
                with open(fasta_file_name, "w") as file:
                    file.writelines(Header + ", " + content_name + str(round(content, 2)) + "\n")
                    file.writelines(self.sequence_dictionary[Header] + "\n")

        """ display a confirmation message about the task completion"""
        messagebox.showinfo("Task completed!", "Please check Output folder")

    def add_contents_to_headers_and_write(self, content_type, sequence_type):
        """
        This method uses a multi-fasta file to calculate and append the AT or GC content of each sequence
        to the relevant fasta header and write them to a new multi-fasta file.
        """
        # declare the necessary variables
        bases = []
        content_name = ""

        # create a new dictionary
        content_sequence_dictionary = {}

        # call the select file method but, abort running te method if returns invalid.
        if self.select_file() == "invalid":
            return

        # calling the separate_header_and_sequence method to read the fasta file.
        self.separate_header_and_sequence(self.file_name)

        # adjust bases list according to the content type and sequence type
        if content_type.get() == "AT" and sequence_type.get() == "DNA":
            bases.extend(["A", "T"])
            content_name = "AT content: "

        elif content_type.get() == "GC" and (sequence_type.get() == "DNA" or sequence_type.get() == "RNA"):
            bases.extend(["G", "C"])
            content_name = "GC content: "

        elif content_type.get() == "AT" and sequence_type.get() == "RNA":
            bases.extend(["A", "U"])
            content_name = "AT content: "

        for Header in self.sequence_dictionary:

            # if the sequence is a protein,
            # display a sequence type error and exit the method.
            nucleotide_sequence = self.sequence_dictionary[Header]
            if self.get_sequence_type(nucleotide_sequence) == "protein":
                messagebox.showerror("Sequence Type Error", "Please select nucleotide sequences to calculate AT/GC "
                                                            "content")
                return

            else:
                count = 0
                content_count = 0
                for base in self.sequence_dictionary[Header]:
                    # calculate the sequence length
                    count += 1
                    # counting content count
                    if base in bases:
                        content_count += 1

                """ calculate the AT/GC content"""
                content = content_count / count

                # create new header
                new_header = Header + ", " + content_name + str(round(content, 2))

                """ Enter the newheader and sequence to a dictionary"""
                content_sequence_dictionary[new_header] = nucleotide_sequence

        """ get the fasta file name"""
        fasta_file_name = self.create_fasta_file_name(self.file_name)

        # writing the sequence length appended header and sequence to a multi-fasta file
        with open(fasta_file_name, "w") as file:

            for new_header in content_sequence_dictionary:
                file.writelines(str(new_header) + "\n")
                file.writelines(content_sequence_dictionary[new_header] + "\n")

        """ display a confirmation message about the task completion"""
        messagebox.showinfo("Task completed!", "Please check Output folder")


if __name__ == "__main__":
    # Create a tkinter window object
    window = tk.Tk()

    # Set the dimensions of the window
    window.geometry("1000x700")

    # Set the title of the window
    window.title("Fasta Processor")
    # disable window resizable
    window.resizable(False, False)

    # making a directory to store output files.
    Dir = "Output"
    if not os.path.exists(Dir):
        os.mkdir("Output")

    """ ------------set background color using a canvas  -------------------  """

    canvas = tk.Canvas(window, width=1000, height=700)
    canvas.config(background="#4ce44c")
    canvas.pack(fill="both", expand=True)

    """-------------------------buttons and labels---------------------------------------------"""
    # Button background color and font
    bttn_bg_color = "#000000"
    bttn_font_size = "Calibri 13"

    # welcome message label
    label = tk.Label(canvas, text="Welcome to Fasta Processor!", font="Helvetica 35 bold", bg="#4ce44c",
                     foreground="white")

    # GUI buttons
    button1 = tk.Button(canvas, text="Split multi-fasta file \n into separate files"
                        , command=lambda: Fasta().split_multi_Fasta_file(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    button2 = tk.Button(canvas, text="Calculate the number of \n fasta sequences in a file"
                        , command=lambda: Fasta().number_of_Fasta_sequences(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    button3 = tk.Button(canvas, text="Combine multiple fasta files \n into a single multi-fasta file"
                        , command=lambda: Fasta().combine_multiple_Fasta_files(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    button4 = tk.Button(canvas, text="Remove unwanted characters \n from a nucleotide sequence"
                        , command=lambda: Sequence().remove_unwanted_from_nucleotide(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    button5 = tk.Button(canvas, text="Remove unwanted characters \n from a protein sequence"
                        , command=lambda: Sequence().remove_unwanted_from_protein(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    button6 = tk.Button(canvas, text="Add sequence length \n to the fasta header"
                        , command=lambda: Sequence().add_sequence_length_to_header(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    button7 = tk.Button(canvas, text="Add sequence lengths \n to respective fasta headers"
                        , command=lambda: Sequence().add_sequence_lengths_to_headers(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    button8 = tk.Button(canvas, text="Get AT content"
                        , command=lambda: Sequence().get_AT_content(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    button9 = tk.Button(canvas, text="Get GC content"
                        , command=lambda: Sequence().get_GC_content(), foreground=bttn_bg_color,
                        font=bttn_font_size, height=2, width=24)

    # This is the output label
    label1 = tk.Label(canvas, text="", font="Calibri 25 bold", height=1, width=30, background="white",
                      foreground="#4ce44c")

    # Use the grid geometry manager to align the labels and radio buttons
    label.grid(row=0, column=0, columnspan=4, padx=5)
    button1.grid(row=1, column=0, padx=10)
    button2.grid(row=1, column=1, padx=10)
    button3.grid(row=1, column=2, padx=10)
    button4.grid(row=1, column=3, padx=10)
    button5.grid(row=2, column=0, padx=10)
    button6.grid(row=2, column=1, padx=10)
    button7.grid(row=2, column=2, padx=10)
    button8.grid(row=2, column=3, padx=10)
    button9.grid(row=3, column=0, padx=10)
    label1.grid(row=4, column=0, columnspan=4, padx=10)

    # use grid_column and row configure to place
    # the buttons equally spaced.
    canvas.grid_columnconfigure(0, minsize=115, weight=1)
    canvas.grid_columnconfigure(1, minsize=115, weight=1)
    canvas.grid_columnconfigure(2, minsize=115, weight=1)
    canvas.grid_columnconfigure(3, minsize=115, weight=1)

    canvas.grid_rowconfigure(0, minsize=110, weight=1)
    canvas.grid_rowconfigure(1, minsize=110, weight=1)
    canvas.grid_rowconfigure(2, minsize=110, weight=1)
    canvas.grid_rowconfigure(3, minsize=110, weight=1)
    canvas.grid_rowconfigure(4, minsize=110, weight=1)

    """ ---------- Frame 1 contains  add_content_to_header_and_write method and its two radio buttons. ----------"""
    frame1 = tk.Frame(canvas, borderwidth=2, relief="solid", background="#4ce44c")
    frame1.grid(row=3, column=1)
    # select content type
    label2 = tk.Label(frame1, text="Select content type", font="Calibri 12", background="#4ce44c")

    # using tkinter StringVar to select content type
    content_type_1 = tk.StringVar()
    content_type_1.set("AT")  # set the default value to AT content

    radio1 = tk.Radiobutton(frame1, text="AT content", variable=content_type_1, value="AT", background="#4ce44c"
                            , font="Calibri 12")

    radio2 = tk.Radiobutton(frame1, text="GC content", variable=content_type_1, value="GC", background="#4ce44c"
                            , font="Calibri 12")

    # select sequence type
    label3 = tk.Label(frame1, text="Select sequence type", font="Calibri 12", background="#4ce44c")

    # using tkinter StringVar to select sequence type
    sequence_type_1 = tk.StringVar()
    sequence_type_1.set("DNA")  # set the default value to DNA sequence type

    radio3 = tk.Radiobutton(frame1, text="DNA", variable=sequence_type_1, value="DNA", background="#4ce44c"
                            , font="Calibri 12")

    radio4 = tk.Radiobutton(frame1, text="RNA", variable=sequence_type_1, value="RNA", background="#4ce44c"
                            , font="Calibri 12")

    button10 = tk.Button(frame1, text="Add content to header"
                         , command=lambda: Sequence().add_content_to_header_and_write(content_type_1, sequence_type_1)
                         , foreground=bttn_bg_color,
                         font=bttn_font_size, height=1, width=21)

    # Use the grid geometry manager to align the labels and radio buttons
    label2.grid(row=0, column=0, columnspan=2)
    radio1.grid(row=1, column=0, sticky="W")
    radio2.grid(row=1, column=1, sticky="W")

    label3.grid(row=2, column=0, columnspan=2)
    radio3.grid(row=3, column=0, sticky="W")
    radio4.grid(row=3, column=1, sticky="W")
    button10.grid(row=4, column=0, columnspan=2)

    """ ---------- Frame 2 contains  add_contents_to_headers_and_write method and its two radio buttons. ----"""
    frame2 = tk.Frame(canvas, borderwidth=2, relief="solid", background="#4ce44c")
    frame2.grid(row=3, column=2)
    # select content type
    label4 = tk.Label(frame2, text="Select content type", font="Calibri 12", background="#4ce44c")

    # using tkinter StringVar to select content type
    content_type_2 = tk.StringVar()
    content_type_2.set("AT")  # set the default value to AT content

    radio5 = tk.Radiobutton(frame2, text="AT content", variable=content_type_2, value="AT", background="#4ce44c"
                            , font="Calibri 12")

    radio6 = tk.Radiobutton(frame2, text="GC content", variable=content_type_2, value="GC", background="#4ce44c"
                            , font="Calibri 12")

    # select sequence type
    label5 = tk.Label(frame2, text="Select sequence type", font="Calibri 12", background="#4ce44c")

    # using tkinter StringVar to select sequence type
    sequence_type_2 = tk.StringVar()
    sequence_type_2.set("DNA")  # set the default value to DNA sequence type

    radio7 = tk.Radiobutton(frame2, text="DNA", variable=sequence_type_2, value="DNA", background="#4ce44c"
                            , font="Calibri 12")

    radio8 = tk.Radiobutton(frame2, text="RNA", variable=sequence_type_2, value="RNA", background="#4ce44c"
                            , font="Calibri 12")

    button11 = tk.Button(frame2, text=" Add contents to headers "
                         , command=lambda: Sequence().add_contents_to_headers_and_write(content_type_2, sequence_type_2)
                         , foreground=bttn_bg_color,
                         font=bttn_font_size, height=1, width=21)

    # Use the grid geometry manager to align the labels and radio buttons
    label4.grid(row=0, column=0, columnspan=2)
    radio5.grid(row=1, column=0, sticky="W")
    radio6.grid(row=1, column=1, sticky="W")

    label5.grid(row=2, column=0, columnspan=2)
    radio7.grid(row=3, column=0, sticky="W")
    radio8.grid(row=3, column=1, sticky="W")
    button11.grid(row=4, column=0, columnspan=2)

    """ ----------------------last code line    ------------------"""
    # Run the tkinter event loop
    window.mainloop()
