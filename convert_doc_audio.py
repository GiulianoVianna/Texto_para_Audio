
import os
from gtts import gTTS, lang # Ler arquivos
import PyPDF2 # Para arquivo pdf
#from playsound import playsound # Musica - opção para teste
import pathlib
import docx2txt # Para arquivo docx
from PyQt5 import uic, QtWidgets 
from PyQt5.QtWidgets import QMessageBox
import vlc  # Musica - Achei a funcionalidade melhor do que o playsound

arquivo = ""
filename = ""

# Mensagens de validação

def msg_arquivo_texto():
    msg1 = QMessageBox()
    msg1.setIcon(QMessageBox.Information)
    msg1.setWindowTitle('Atenção')
    msg1.setText('Favor escolher um arquivo de texto!')
    x = msg1.exec_()

def msg_formato_doc():
    msg1 = QMessageBox()
    msg1.setIcon(QMessageBox.Information)
    msg1.setWindowTitle('Atenção')
    msg1.setText('Favor escolher um formato de documento .doc, .pdf ou .txt!')
    x = msg1.exec_()

def msg_extensao():
    msg1 = QMessageBox()
    msg1.setIcon(QMessageBox.Critical)
    msg1.setWindowTitle('Atenção')
    msg1.setText('A aplicação não encontrou a extensão do arquivo selecionado.\nFavor selecionar um arquivo com a extensão .doc, .pdf ou .txt!')
    x = msg1.exec_()

def msg_arquivo_audio():
    msg1 = QMessageBox()
    msg1.setIcon(QMessageBox.Information)
    msg1.setWindowTitle('Informação')
    msg1.setText('Arquivo de audio gerado!')
    x = msg1.exec_()

#################################################################

# Lê o nome do arquivo e endereço do diretório

def abrir_arquivo():

    tela.bt_play.setEnabled(False)

    global arquivo  

    tela.ln_tipo.setText("")
    arquivo = QtWidgets.QFileDialog.getOpenFileName()[0]

    with open(arquivo) as diretorio: 
        tela.ln_diretorio.setText(diretorio.name)
        file_extension = pathlib.Path(arquivo).suffix        
        tela.ln_tipo.setText(file_extension)

#################################################################

# Gera arquivo audio.mp3

def speak(text):

    global filename

    tts = gTTS(text = text, lang = 'pt-br', slow= False)
    filename = 'audio.mp3'
    tts.save(filename)
    size = os.path.getsize('audio.mp3')  
     
    if size > 0:
        msg_arquivo_audio()
        tela.bt_play.setEnabled(True)

#################################################################

# Toca o arquivo audio.mp3

def play_audio():
    #playsound(filename) # opção para teste
    p = vlc.MediaPlayer(filename)
    p.play()
   
#################################################################

# Faz a leitura do arquivo de documento / Chama a função speak

def formato_arquivo():

    if tela.ln_tipo.text() == ".txt":
        with open(arquivo) as text_to_read:
            txt = text_to_read.read()
            speak(txt)

    elif tela.ln_tipo.text() == ".docx":
        docx_text = docx2txt.process(arquivo)
        speak(docx_text)
                
    elif tela.ln_tipo.text() == ".pdf":
        pdfFileObj = open(arquivo, 'rb')

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        pageObj = pdfReader.getPage(0)
                
        pdf_text = pageObj.extractText() 
        speak(pdf_text)                    

        pdfFileObj.close()   
    
#################################################################

# Regra de validação para os campos obrigatórios

def ler_arquivo():    

    if tela.ln_tipo.text() != "":

        if tela.ln_diretorio.text() != "": 

            if tela.ln_tipo.text() == ".docx" or tela.ln_tipo.text() == ".pdf" or tela.ln_tipo.text() == ".txt":

                formato_arquivo()

            else:
                msg_formato_doc()

        else:
            msg_arquivo_texto()

    else:        
        msg_extensao() 


#################################################################

app = QtWidgets.QApplication([])
tela = uic.loadUi("convert_doc_audio.ui")
tela.setFixedSize(593, 274)
tela.bt_diretorio.clicked.connect(abrir_arquivo)
tela.bt_convert.clicked.connect(ler_arquivo)
tela.bt_play.clicked.connect(play_audio)

tela.show()
app.exec()
