from shutil import copyfile

class FileUtils:
    @staticmethod
    def stripExtension(filename):
        lastDot = filename.find(".")
        if lastDot != -1:
            return filename[:lastDot]
        else:
            return filename

    #fromFile and toFile are pathnames given as strings
    @staticmethod
    def copy(fromFile, toFile):
        copyfile(fromFile, toFile)
