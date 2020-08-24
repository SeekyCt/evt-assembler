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
        parser.add_argument("--binary", "-b", action="store_true")
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

        # --binary, -b
        # Outputs to direct binary instead of code
        self.binary = args.binary