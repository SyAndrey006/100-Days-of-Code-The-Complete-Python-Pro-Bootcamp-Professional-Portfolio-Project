from PyPDF2 import PdfReader
from gtts import gTTS

reader = PdfReader("book.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()

print(text)

text = text.replace("\n", " ")
text = text.replace("  ", " ")

gtts = gTTS(text = text, lang = "en")

gtts.save("audiobook.mp3")

print("Everything is ready.")