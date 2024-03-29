
import traceback, logging, sys


def pr(message):
    stack = traceback.extract_stack()
    filename, codeline, funcName, text = stack[-2]
   
#     print('filename:', filename)
#     print('codeline:', codeline)
#     print('funcName:', funcName)
#     print('text:', text)
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info(" " + str(codeline) + " " + funcName + " " + message)

    return funcName



def stringNumericalValue(input):
    
    input = input.lower()
    output = []
    sum = 0
    
    for character in input:
        number = ord(character) - 96
        output.append(number)
        sum = sum + number
        
#     print(output)
#     print('sum: ', sum)
    
    return sum

    

def numberToLetterASCII(num):

    return chr(num + ord('A'))



def save_uploaded_file(file, full_file_name):

    try:

        with open(full_file_name, 'wb+') as destination:

            for chunk in file.chunks():

                destination.write(chunk)

        return True

    except Exception:

        print('exception: ', sys.exc_info)
        traceback.print_exc()

        return False