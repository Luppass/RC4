import codecs
import sys
MOD = 256
def ksa(key, rep):
    key_length = len(key)
    S = list(range(MOD))  # [0,1,2, ... , 255]
    if rep == 0:
        print(f'Valor inicial de S: {(dec2Bin(S))}')
    # create the array "S"
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values
    if rep == 0:    
        print(f'\nValor de S después de la fase inicial: {dec2Bin(S)}\n')
    rep = rep + 1
    return S


def dec2Bin(S):
    B = []
    for i in S:
        B.append(bin(i))
    return B

def pgra(S, lentext):
    i = 0
    j = 0
    ay = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % MOD]
        ay+=1
        if ay == lentext:
            print(f'\nValor del keystream en binario: {bin(K)}')
            print(f'Valor de S según la generación del keystream {dec2Bin(S)}')   
        yield K
    

def get_keystream(key, lentext, rep):

    S = ksa(key, rep)
    return pgra(S, lentext)

def show_S(key, rep):
    key = codecs.decode(key, 'hex_codec')
    ksa(key, rep)
   
    
def encrypt_logic(key, text, lentext, rep):
    
    key = codecs.decode(key, 'hex_codec')
    key = [c for c in key]
    keystream = get_keystream(key, lentext, rep)
    res = []
    for c in text:
        ks = next(keystream)
        val = ("%02X" % (c ^ ks))  # XOR and taking hex
        res.append(val)
    print("\nValores del último character introducido:")
    print(f'Codificación ASCII: {chr(text[-1])}')
    print(f'Valor en binario: {bin(text[-1])}')
    return ''.join(res)

def decrypt_logic(key,text, lentext, rep):
    key = codecs.decode(key, 'hex_codec')
    key = [c for c in key]
    keystream = get_keystream(key, lentext, rep)
    #print(keystream)
    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
        res.append(val)
    return ''.join(res)


def encrypt(key, plaintext, lentext, rep):
    ''' :key -> encryption key used for encrypting, as hex string
        :plaintext -> plaintext string to encrpyt
    '''
    plaintext = [ord(c) for c in plaintext]
    return encrypt_logic(key, plaintext, lentext, rep)


def decrypt(key,text, lentext, rep):
    text = codecs.decode(text,'hex_codec')
    res = decrypt_logic(key,text, lentext, rep)
    return codecs.decode(res,'hex_codec').decode('utf-8')


def help():

  if len(sys.argv) == 2 and sys.argv[1] == '--help':
      print("   python3 RC4.py < -c | -d > \n\t-c: Cifra el archivo pasado por comando la clave en hexadecimal y cada caracter que deseemos cifrar\n\t-d: Descifra el archivo pasado por comandos clave y mensaje a descifrar, ambos en decimal")                           
      print(" La opción -c cifra tal y como se indica en el enunciado mostrando su codificación en ASCII, en binario, el  valor  del  keystream  en  binario  y  el  resultado  de  la  operación  de  cifrado  en binario y en hexadecimal ")
      print(" La opción -d descifra tal y como se indica en el enunciado monstrando el mensaje original en ASCII")
      print(" La clave debe estar en HEXADECIMAL. Previo a cifrar y descifrar se muestra :valor inicial de S, el valor de S después de la fase inicial y cómo va cambiando S con la generación del keystream. Todo en binario")
      print(" Para terminar la ejecución escriba FIN ")
      return -1

def ishex(s):
    return not set(s) - set("ABCDEF0123456789")  

if __name__ == '__main__':
    help()
    
    if len(sys.argv) != 2:
        print("Se requieren 1 argumento, usted introdujo %d\nPara mas ayuda la opción --help" % (len(sys.argv) - 1))
        exit()
    elif ((sys.argv[1] != '-c') and (sys.argv[1] != '-d')):
          print("Mal uso del comando. Introduzca la opcion -c o -d\nPara más ayuda utilice la opción --help")
          exit()
          
    if(sys.argv[1] == "-c") : 
        
        while(1):
            key = input("Introduce la clave en hexadecimal o introduce FIN o un espacio para terminar:")
            if key == '':
                exit()
            elif ishex(key):
                show_S(key, rep=0)
                break
            else:
                print(f'Formato de clave erróneo, utilice una clave en hexadecimal. Clave introducida: "{key}"')
                
        
        char = ''
        rep = 1
        while(1):
            
            if char == '':
                char = input("\nIntroduce el siguiente caracter o introduce FIN o un espacio para terminar: ")
                if char == '':
                    exit()
                cifrado = encrypt(key,char, lentext=len(char), rep=1)
            else:
                char2 = input("\nIntroduce el siguiente caracter o introduce FIN o un espacio para terminar: ")
                if(char2 == "FIN" or char2 == ''): exit()
                char += char2
                lentext = len(char)
                cifrado = encrypt(key,char, lentext, rep)
            print(f'Valor del resultado de cifrado en binario: {bin(int(cifrado, base=16))}')
            print(f'Valor del resultado de cifrado en hexadecimal: {cifrado}')
  
    if(sys.argv[1] == "-d"):
        while(1):
            key = input("Introduce la clave en hexadecimal:")
            if(key == "FIN"): exit()
            if ishex(key):
                show_S(key, rep=1)
                break
            else:
                print(f'Formato de clave erróneo, utilice una clave en hexadecimal. Clave introducida: "{key}"')
        ciphertext = input("Introduzca el texto cifrado en hexadecimal o introduce FIN o un espacio para terminar: ")
        lentext = len(ciphertext)
        plaintext = decrypt(key,ciphertext, lentext, rep=1)
        print(f'El texto descifrado es: {plaintext}')

    
     


    
        
