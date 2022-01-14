"""Validate Zipf's Law.

!!!! PROBLEMS !!!!

* labels in the plottings does not show, why is that? Fix needed.
"""

from textract import process as prc
import re
from collections import Counter
import matplotlib.pyplot as plt
import math
import os

COLORS = ['b', 'g', 'r', 'c', 'y', 'm']
COLORS_IDTF = COLORS + [color + 'o' for color in COLORS]


class NoFileError(Exception):
    """Create custom Exception."""

    pass


class Zipfs():
    """Check if .pdf documents abide Zipf's law."""

    def __init__(self, num, pdf_Folder='PDFs'):
        """Construct."""
        self.CWD = re.sub(
                      '\\\\',  # pattern
                      '/',     # replace
                      os.getcwd()  # string
                      )

        self.pdfFolderPath = self.CWD + '/' + pdf_Folder
        if os.path.isdir(self.pdfFolderPath) is False:
            os.makedirs(pdf_Folder)

        self.pdfFileNamesList = [(self.pdfFolderPath
                                  + '/'
                                  + pdfFileName)
                                 for pdfFileName in
                                 os.listdir(self.pdfFolderPath)
                                 ]
        if len(self.pdfFileNamesList) < 1:
            raise NoFileError(
                """There is no files in the
                folder named: {}.""".format(pdf_Folder)
                             )
        self.num = num

    def load_text(self):
        """Get raw text from pdf file."""
        self.rawTextList = [
                            prc(pdfFile)
                            for pdfFile in self.pdfFileNamesList
                            ]

    def find_words(self):
        """Find words and their respective occurence count."""
        self.wordsList = [
                          (
                           re.findall(r"[^\W_]+",
                                      rawText.decode('UTF-8'),
                                      re.MULTILINE | re.IGNORECASE)
                           )
                          for rawText in self.rawTextList
                          ]

        self.eachWordCountList = [
                              Counter([
                                       word.upper()
                                       for word in wordList
                                       ])

                              for wordList in self.wordsList
                                 ]

    def sort_words(self):
        """Sort words from most occured to least."""
        self.sortedWordCountList = [
                                sorted(
                                       eachWordCountList.items(),
                                       key=lambda x: x[1],
                                       reverse=True
                                       )

                                for eachWordCountList
                                in self.eachWordCountList
                                   ]

    def create_names_ocurrence(self):
        """Create arrays ready to plot by mapping."""
        # self.namesOrdered = [self.sortedWordCountList[:][t][0]
        #               for t in range(self.num)
        #               ]
        # NOT SURE IF THE ABOVE SNIPPET WORKS NOT A CONCERN CURRENTLY

        self.occurenceList = [
                [
                 self.sortedWordCountList[i][t][1]
                 for t in range(self.num)
                 ]
                for i in range(len(self.sortedWordCountList))
                              ]

    def print_pdf2num(self):
        """Print the pdf file names with their corresponding number."""
        self.pdfFileNames = os.listdir(self.pdfFolderPath)
        _ = [
             print("Number {} refers to file {}".format(
                    i, self.pdfFileNames[i]
                                                       )
                   )

             for i in range(len(self.pdfFileNames))
             ]

    def plot_graph(self):
        """Plot results.

        Later it will turn into its own class,
        with methods for each process below.
        """
        # Initialize ideal function parameters

        self.maxOcc = max(max(self.occurenceList))
        X = [i+1 for i in range(self.num)]
        Xlog = [math.log(_) for _ in X]

        # First plot ##

        plt.figure(1)
        plt.xlabel("Distinct Words")
        plt.ylabel("Occurence Count")

        y = [self.maxOcc * 1/i for i in X]
        ylog = [math.log(_) for _ in y]
        plt.plot(X, y, 'k', label='ideal')

        for writing in range(len(self.occurenceList)):
            plt.plot(
                     X, self.occurenceList[writing],  # x and y
                     COLORS_IDTF[writing], label=str(writing)  # options
                     )

        # Second Plot ##

        plt.figure(2)
        plt.xlabel("Distinct Words")
        plt.ylabel("log(Occurence Count)")

        y = [math.log(self.maxOcc * 1/i) for i in X]
        plt.plot(X, ylog, 'k', label='ideal')

        for writing in range(len(self.occurenceList)):
            Ylog = [
                 math.log(self.occurenceList[writing][i])
                 for i in range(len(self.occurenceList[writing]))
                 ]

            plt.plot(
                     X, Ylog,  # x and y
                     COLORS_IDTF[writing], label=str(writing)  # options
                     )

        # Third Plot ##

        plt.figure(3)
        plt.xlabel("log(Distinct Words)")
        plt.ylabel("log(Occurence Count)")

        plt.plot(Xlog, ylog, 'k', label='ideal')

        for writing in range(len(self.occurenceList)):
            Ylog = [
                 math.log(self.occurenceList[writing][i])
                 for i in range(len(self.occurenceList[writing]))
                 ]

            plt.plot(
                     Xlog, Ylog,  # x and y
                     COLORS_IDTF[writing], label=str(writing)  # options
                     )

    def process(self):
        """Process all."""
        self.load_text()
        self.find_words()
        self.sort_words()
        self.create_names_ocurrence()
        self.print_pdf2num()
        self.plot_graph()
