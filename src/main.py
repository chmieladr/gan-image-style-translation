from warnings import filterwarnings

from gui import GUI

filterwarnings("ignore")

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
