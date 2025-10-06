from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.pickers import MDDatePicker
import sqlite3
from db import init_db
from kivy.core.window import Window
import evofunction as evf #funções do sistema


Window.size = (350, 580)

class SaidaScreen(MDScreen):
    def on_pre_enter(self, *args):

        self.Confirmar = evf
        self.Confirmar.confirmacao('Deseja sair do aplicativo?')
        #MDApp.get_running_app().root.current = 'home'
        

class HomeScreen(MDScreen):

    Confirmar = evf
    
    def on_pre_enter(self, *args):
    
        Window.bind(on_keyboard=self.voltar) 
        
        self.carregar_pacientes()

    def carregar_pacientes(self):
        #self.ids.lista_pacientes.clear_widgets()
        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Nome, CPF FROM Paciente ORDER BY Nome")
        qtdeLinhas = cursor.rowcount
        if qtdeLinhas > 0:
            for nome, cpf in cursor.fetchall():
                self.ids.lista_pacientes.add_widget(
                    OneLineListItem(text=f"{nome} - CPF: {cpf}")
                )
        conn.close()
    
    def voltar(self,window, key, *args):
        if key == 27:
            self.Confirmar.confirmacao('Deseja sair do aplicativo?')
            return True        

    def login(self):
        print('Digite a senha de acesso ao sistema:')
        
        #MDApp.get_running_app().root.current = 'home'  

class PacienteScreen(MDScreen):
    def salvar(self):
        dados = {k: self.ids[k].text for k in self.ids if k not in ["container"]}
        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO Paciente VALUES 
            (:data,:nome,:cpf,:dtnasc,:email,:contato,:responsavel,:cpf_responsavel,
             :hipotese,:email_responsavel,:contato_responsavel,:logradouro,:numero,
             :complemento,:bairro,:cep,:uf,:cp)
        """, {
            "data": dados["data"], "nome": dados["nome"], "cpf": dados["cpf"], "dtnasc": dados["dtnasc"],
            "email": dados["email"], "contato": dados["contato"], "responsavel": dados["responsavel"],
            "cpf_responsavel": dados["cpf_responsavel"], "hipotese": dados["hipotese"],
            "email_responsavel": dados["email_responsavel"], "contato_responsavel": dados["contato_responsavel"],
            "logradouro": dados["logradouro"], "numero": dados["numero"], "complemento": dados["complemento"],
            "bairro": dados["bairro"], "cep": dados["cep"], "uf": dados["uf"], "cp": dados["cp"]
        })
        conn.commit()
        conn.close()
        print("Paciente salvo!")


class ConvenioScreen(MDScreen):
    def salvar(self):
        dados = {k: self.ids[k].text for k in self.ids if k not in ["container"]}
        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Convenio (CPF,Convenio,Plano,Carteirinha,Reembolso) 
            VALUES (:cpf,:convenio,:plano,:carteirinha,:reembolso)
        """, dados)
        conn.commit()
        conn.close()
        print("Convênio salvo!")


class ClinicoScreen(MDScreen):
    def salvar(self):
        dados = {k: self.ids[k].text for k in self.ids if k not in ["container"]}
        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clinico (CPF,DtCadastro,Diagnostico,Indicacao,Avaliacao,Alta,DtAlta)
            VALUES (:cpf,:dtcadastro,:diagnostico,:indicacao,:avaliacao,:alta,:dtalta)
        """, dados)
        conn.commit()
        conn.close()
        print("Clínico salvo!")


class SessaoScreen(MDScreen):
    def salvar(self):
        dados = {k: self.ids[k].text for k in self.ids if k not in ["container"]}
        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Sessao (CPF,Clinico,QueixaSintoma,Consciencia,Nutricional,Mobilidade,Data,
                                TerapiasAplicadas,Realizado,Evolucao,Observacao,NomeProfissional,
                                Conselho,Assinatura)
            VALUES (:cpf,:clinico,:queixa,:consciencia,:nutricional,:mobilidade,:data,
                    :terapias,:realizado,:evolucao,:observacao,:nomeprof,:conselho,:assinatura)
        """, dados)
        conn.commit()
        conn.close()
        print("Sessão salva!")


class EvolucaoScreen(MDScreen):

    def on_pre_enter(self, *args):
        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        # Chama a função para obter os dados do SQL
        sql_data = cursor.execute("SELECT Nome FROM Paciente")
        print(sql_data)
        #self.ids.combo_box.values = sql_data # Define os valores do dropdown
        conn.close()


    def salvar(self):
        dados = {k: self.ids[k].text for k in self.ids if k not in ["container"]}
        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Evolucao (CPF,Data,Observacao,Evolucao)
            VALUES (:cpf,:data,:observacao,:evolucao)
        """, dados)
        conn.commit()
        conn.close()
        print("Evolução salva!")

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_ok=self.on_date_ok) # Opcional: Define o que acontece quando a data é selecionada
        date_dialog.open()

    def on_date_ok(self, instance_date_picker):
        # Esta função é chamada quando o usuário clica em 'OK' no calendário
        print(f"Data selecionada: {instance_date_picker.get_date()}")
        # instance_date_picker.get_date() retorna uma tupla (ano, mês, dia)


class MainApp(MDApp):
    
    def build(self):
        init_db()
        return Builder.load_file("telas.kv")
    
    def sair(self):
        self.Confirmar = evf
        self.Confirmar.confirmacao('Deseja sair do aplicativo?')

    def show_date_picker(self):
        date_dialog = MDDatePicker( size=(50,50))
        date_dialog.bind(on_ok=self.on_date_ok) # Opcional: Define o que acontece quando a data é selecionada
        date_dialog.open()

    def on_date_ok(self, instance_date_picker):
        # Esta função é chamada quando o usuário clica em 'OK' no calendário
        print(f"Data selecionada: {instance_date_picker.get_date()}")
        # instance_date_picker.get_date() retorna uma tupla (ano, mês, dia)


if __name__ == "__main__":
    MainApp().run()
