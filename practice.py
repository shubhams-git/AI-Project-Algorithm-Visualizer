from FileReader import FileReader

if __name__ == "__main__":
    fileReader = FileReader("test.txt")
    fileReader.read()
    print(fileReader.get_goal());