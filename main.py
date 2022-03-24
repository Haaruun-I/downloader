import lib.ripper, lib.download, os

booklist = [

    "https://hpaudiobooks.club/blood-prince-jim-dale-book/",
    "https://hpaudiobooks.club/jim-dale-harry-potter-and-deathly-hallows-audiobook/"
]

for book in booklist:
    
    title = lib.ripper.getTitle(book)
    print(title)
    basepath =  title + "\\"
    
    try:
        os.mkdir(basepath)
    except FileExistsError:
        pass
    chapters = lib.ripper.getChapters(book)

    for chapter in chapters:
        file = lib.ripper.getFileName(chapter)
        print(file)
        lib.download.downloadFile(chapter, basepath + file)