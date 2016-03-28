class FileUtils:
    @staticmethod
    def stripExtension(filename):
        lastDot = filename.find(".")
        if lastDot != -1:
            return filename[:lastDot]
        else:
            return filename
