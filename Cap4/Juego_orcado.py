def juego_adivinar_palabra():
    palabra_secreta = "Dragonball".upper() 
    vidas = 5  
    letras_adivinadas = ['_'] * len(palabra_secreta)  
    
    print("¡Bienvenido al juego de adivinar la palabra!")
    print(f"La palabra tiene {len(palabra_secreta)} letras: {' '.join(letras_adivinadas)}")
    print(f"Tienes {vidas} vidas.")
    
    while vidas > 0 and '_' in letras_adivinadas:
        suposicion = input("Introduce una letra o la palabra completa: ").upper()
        
        
        if len(suposicion) > 1:
            if suposicion == palabra_secreta:
                print(f"¡Correcto! La palabra era {palabra_secreta}")
                return
            else:
                vidas -= 1
                print(f"Incorrecto. Pierdes una vida. Vidas restantes: {vidas}")
                continue
                
        
        if suposicion in palabra_secreta:
            print("¡Correcto!")
            
            for i in range(len(palabra_secreta)):
                if palabra_secreta[i] == suposicion:
                    letras_adivinadas[i] = suposicion
        else:
            vidas -= 1
            print(f"Letra incorrecta. Pierdes una vida. Vidas restantes: {vidas}")
        
        
        print(f"\nPalabra: {' '.join(letras_adivinadas)}")
        print(f"Vidas restantes: {vidas}\n")
    
    
    if '_' not in letras_adivinadas:
        print(f"¡Felicidades! Adivinaste la palabra: {palabra_secreta}")
    else:
        print(f"¡Game Over! La palabra era: {palabra_secreta}")
juego_adivinar_palabra()
