import pyautogui
from time import sleep

# Abrir janela
pyautogui.click(840,774, duration=1)

# Conectar ao banco
pyautogui.click(606,208, duration=0.5)

# Criar tabela
pyautogui.click(613,254, duration=0.5)

# Digitar nome e email
with open("usuario.txt", "r") as arquivo:
    for linha in arquivo:
        nome = linha.split(",")[0]
        email = linha.split(",")[1]
        
        pyautogui.click(306,208, duration=0.5)
        pyautogui.write(nome)
        pyautogui.click(302,252, duration=0.5)
        pyautogui.write(email)
        
        # Registrar usuário
        pyautogui.click(623,295, duration=0.2)
        sleep(1)
