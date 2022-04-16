import json
import sys
import readchar
import clipboard

class Translator:
    def __init__(self, upper_lower, end_symbol, char_map):
        self.upper_lower = upper_lower
        if self.upper_lower:
            self.parity = True
         
        self.end_symbol = end_symbol
   
        self.char_map = char_map
    
    def translateText(self, text):
        textResult = ""
        for char in text:
            textResult+=self.translateChar(char)
        
        return textResult

    def translateChar(self, char):
        result = char
        if(self.upper_lower):
            result = self.upper_or_lower(result)
        
        result = self.translate_map(result)

        if(self.end_symbol):
            result = self.ends_with_symbol(result)

        return result
        
    def translate_map(self,char):
        if char in self.char_map:
            return self.char_map[char]
        else:
            return char
    
    def upper_or_lower(self,char):
        self.parity = not self.parity

        if self.parity:
            return char.upper()
        else:
            return char.lower()
    
    def ends_with_symbol(self,char):
        return char+self.end_symbol


def checkAlphabet(bindings, alphabet, lang):
    translatedAlphabet = ""
    counter=0
    for char in alphabet:
        try:

            if char.isupper():
                output_symbol = bindings[lang]["upper"][char]
            elif char.islower():
                output_symbol = bindings[lang]["lower"][char]

            # print(output_symbol, end=end_symbol, flush=True)
            counter+=1
            translatedAlphabet+=output_symbol
        
        except KeyError as e:
            print("\nНе указан бинд для", e)

    return(translatedAlphabet, counter)
        

def checkRuAlphabet(bindings): 
    ru_alphabet = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    translated,counter  = checkAlphabet(bindings, ru_alphabet,"ru")
    print(f"Символов в алфавите: {len(ru_alphabet)}, переведено {counter}")
    print(f"{translated}")

def validate(config):
    try:
        print(f"Название конфига {config['name']}")
        print(f"Языки {config['lang']}")
        print(f"Символ после буквы: \"{config['endSymbol']}\"")
        print(f"НиЖнИй И вЕрХнИй РеГиСтРы: {config['upperLower']}")
        checkRuAlphabet(config)
    except KeyError as e:
            print("\nНе указано поле", e)


def read(config):
    end_symbol = bindings['endSymbol']
    upper_lower = bindings['upperLower']
   
    char_map = bindings['ru']['upper']
    char_map.update(bindings['ru']['lower'])
    
    return upper_lower, end_symbol, char_map
    

if __name__ == '__main__':
    config_path = ""
    if sys.argv[1:]==[]:
        print("Конфиг не указан укажите конфиг при запуске: \n\n\tpython3 main.py characters/config.json\n\n")
        print("использовать config.json?[Y/n]")
        yes = input()
        if (yes.upper()=='Y'):
            config_path = "config.json"
        else:
            print("Введите путь до конфигурации:")
            config_path = input()

    else:
        config_path = sys.argv[1]
        print(f"Переданный конфиг {sys.argv[1]}")
    
    with open(config_path) as config:
        bindings = json.load(config)
        validate(bindings)

        upper_lower, end_symbol, char_map = read(bindings)

        translator = Translator(upper_lower, end_symbol, char_map)

        text = ""
        
        print("✂️ [Ctrl+c] - скопировать\n❌ [Ctrl+x] - выйти")
        while True:
            c = readchar.readchar()
            if(ord(c) == 3):
                clipboard.copy(translator.translateText(text))
            if(ord(c) == 24):
                quit()
            if(ord(c) == 127):
                print(' '*len(text)*2, end="")
                text = text[:-1]
                
                print('\r', end="")
               
            else:
                text+=c
        
            print(translator.translateText(text), end="")
            print("\r", end="")
            
            # print(translator.translateText(text),end='', flush=True)

            # if c==" ":
            #     print(" ",end='',flush=True)
            #     continue
            # try:
            #     if(upperLOWER):
            #         if parity:
            #             c=c.upper()
            #         else: 
            #             c=c.lower()
            #         parity = not parity
                
            #     if c.isupper():
            #         output_symbol = bindings["ru"]["upper"][c]
            #     elif c.islower():
            #         output_symbol = bindings["ru"]["lower"][c]

            #     print(output_symbol, end=end_symbol, flush=True)

            # except KeyError: 
            #     print(c,end=end_symbol, flush=True)