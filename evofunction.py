from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button as Botao
#from kivy.app import App
from kivymd.app import MDApp


import sqlite3

banco = sqlite3.connect('evolution.db')
popSound =  SoundLoader.load('sounds/pop.wav')
papaSound = SoundLoader.load('sounds/papa.wav')

cursor = banco.cursor()

def criar_tabelas():
    cursor.execute( 'CREATE TABLE IF NOT EXISTS pacientes (id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT NOT NULL,cpf  TEXT,rg TEXT,telefone TEXT,nascimento TEXT,email TEXT)' )

def insert_paciente(nome, cpf, rg, telefone, nascimento, email):
    cursor.execute('INSERT INTO pacientes(nome, cpf, rg, telefone, nascimento, email) VALUES (?, ?, ?, ?, ?, ?)',
                   (nome, cpf, rg, telefone, nascimento, email))
    banco.commit()           

def delete_paciente(id):
    try:
        cursor.execute('DELETE FROM pacientes WHERE id = ?', (id,))
        banco.commit()
        print(f"Paciente com ID {id} deletado com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao deletar paciente: {e}")

def update_paciente(id, nome, cpf, rg, telefone, nascimento, email):
    cursor.execute('UPDATE pacientes SET nome = ?, cpf = ?, rg = ?, telefone = ?, nascimento = ?, email = ? WHERE id = ?',
                   (nome, cpf, rg, telefone, nascimento, email, id))
    banco.commit()        

def select_paciente_ID(id):
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id,))
    paciente = cursor.fetchone()
    if paciente:
        return paciente
    else:
        print(f"Paciente com ID {id} não encontrado.")
        return None
    
#insert_paciente(
#    'João do Pulo',
#    '123.456.789-00','12.345.678-X','+55 11 91234-5678','01/01/1990','teste1@gmail.com')
def select_all_pacientes():  
    cursor.execute('select * from pacientes')
    #print(cursor.fetchall())
    pacientes = cursor.fetchall()
    for paciente in pacientes:
        print(paciente)

class Janela():
    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)

def confirmacao(msg):
    global popSound
    popSound.play()
    box= BoxLayout(orientation='vertical', padding=10, spacing=10)
    botoes = BoxLayout(padding=10, spacing=10)

    pop = Popup(title=msg, content=box, size_hint=(None,None), 
                    size = (150, 100))
        
    sim = Botao(text='Sim', on_release=MDApp.get_running_app().stop)
    nao = Botao(text='Não', on_release=pop.dismiss)
        
    botoes.add_widget(sim)
    botoes.add_widget(nao)

    atencao = Image(source='img/atencao.png')

    box.add_widget(atencao)
    box.add_widget(botoes)

    animText = Animation(color=(0,0,0,1)) + Animation(color=(1,1,1,1))
    animText.repeat = True
    animText.start(sim)
    anim = Animation(size=(300, 200), duration=0.2,t='out_back') 
    anim.start(pop)
    pop.open()
    return True

def OK(msg):
    global popSound
    popSound.play()
    box= BoxLayout(orientation='vertical', padding=10, spacing=10)
    botoes = BoxLayout(padding=10, spacing=10)

    pop = Popup(title= msg, content=box, size_hint=(None,None), size = (150, 100))
        
    #sim = Botao(text='Sim', on_release=MDApp.get_running_app().stop)
    ok = Botao(text='OK', on_release=pop.dismiss)
        
    botoes.add_widget(ok)
    #botoes.add_widget(nao)

    atencao = Image(source='img/atencao.png')

    box.add_widget(atencao)
    box.add_widget(botoes)

    animText = Animation(color=(0,0,0,1)) + Animation(color=(1,1,1,1))
    animText.repeat = True
    animText.start(ok)
    anim = Animation(size=(300, 200), duration=0.2,t='out_back') 
    anim.start(pop)
    pop.open()
    return True
