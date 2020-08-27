import argparse

class Config:
    _sInstance = None
    @staticmethod
    def getStaticInstance():
        if Config._sInstance is None:
            Config._sInstance = Config()
        return Config._sInstance
    @staticmethod
    def destroyStaticInstance():
        del Config._sInstance

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--infile", "-i")
        parser.add_argument("--outfile", "-o")
        parser.add_argument("--symbol", "-s")
        parser.add_argument("--binary", "-b", action="store_true")
        args = parser.parse_args()
        
        # --infile path, -i path
        # Path to the text file containing the evt script
        if args.infile is None:
            self.inPath = input("script path: ")
        else:
            self.inPath = args.infile

        # --outfile path, -o path
        # Output is stored to a file instead of being printed to the console
        if args.outfile is None:
            self.toFile = False
            self.outPath = None
        else:
            self.toFile = True
            self.outPath = args.outfile

        # --symbol name, -s name
        # Sets the name for the symbol created (ignored for binary format)
        if args.symbol is None:
            self.symbol = "script"
        else:
            self.symbol = args.symbol

        # --binary, -b
        # Makes the output plain binary (or hex in the console if no outfile is specified) instead of a C/C++ array
        self.binary = args.binary