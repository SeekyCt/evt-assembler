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
        parser.add_argument("--assembly", "-a", action="store_true")
        args = parser.parse_args()
        
        # --infile path, -o path
        # Path to the text file containing the evt script
        if args.infile is not None:
            self.inPath = args.infile
        else:
            self.inPath = input("script path: ")

        # --outfile path, -o path
        # Disassembly is stored to a text file instead of being printed to the console
        if args.outfile is not None:
            self.toFile = True
            self.outPath = args.outfile
        else:
            self.toFile = False
            self.outPath = None

        # --symbol name
        # Sets the name for the symbol created
        if args.symbol is None:
            self.outName = "script"
        else:
            self.outName = args.symbol

        # --assembly, -a
        # Outputs asm pseudo-ops instead of a C array
        self.asm = args.assembly