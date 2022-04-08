import hashlib
import argparse
import json
import time


def main(args):
    # Check if the input file was provided
    if not args.input:
        print('no input file was given')
        exit(0)
    if not args.difficulty:
        print('no dificulty was given')
        exit(0)
    if not args.balances:
        print('no balances file was given')
        exit(0)
    balances = import_balances(args.balances)
    # Generate a block object that later gets filled from given .json file
    block = Block()
    block.import_from_json(args.input)

    # Calculate nonce to make the block valid
    valid_block = calculate_valid_block(block, args.difficulty, balances)
    print(valid_block.get_json())

def get_diff_mask(bit_base, diff):
    # fill a variable of '1' and make the variable to shift dif times << so that '11111111000'
    # apply the mask with an 'OR' comparison and if the result matches de mask, ok!
    diff_mask = (1 << bit_base) - 1# assuming that int in python is int64
    diff_mask = diff_mask << diff
    # bring the len of the mask back to 64 bits
    diff_mask = 0xFFFFFFFFFFFF & diff_mask
    return diff_mask


def calculate_valid_block(block, diff, input_balances):
    """
    Completar los campos que faltan en la función `calculate_valid_block()` de manera que 
    esta devuelva el objeto Block con un valor de `nonce` valido para que el hash del bloque 
    tenga `X` número de ceros por la derecha. (donde X es la dificultad definida al llamar al script)

    NOTA: Comparadores binarios:
    or -> `|` 
    1111 | 0000 = 1111
    and -> `&`
    1010 & 0101 = 0000
    """

    if not block.check_valid_transactions(input_balances):
        print('some transaction/s are not valid')
        exit(0)
    # Get the base mask that will determine if the hash of the block is valid or not 
    diff_mask = get_diff_mask(64, diff)

    ## --- Espacio para rellenar ---

    h = block.get_hash()

    while ((h | diff_mask) != diff_mask):
        block.increase_nonce()
        # force to sleep 5 secs to avoid burning PCs :)
        time.sleep(1)
        # calculate next hash
        h = block.get_hash()
 
    ## --- Fin de espacio ---

    print('block successfully mined at nonce', block.nonce)
    print('hash hex:         ', hex(h))
    print('matching mask hex:', hex(diff_mask))
    print('hash bin:         ', bin(h))
    print('matching mask bin:', bin(diff_mask))

    return block

class Block():
    
    def __init__(self):
        self.block_number = 0
        self.parent_block = 0
        self.nonce = 0
        self.transactions = []

    def import_from_json(self, file):
        print('loading json file', file)
        # read the json file
        f = open(file, 'r')
        data = json.load(f)
        # compose local struct from json
        self.block_number = data["header"]["block_number"]
        self.parent_block = data["header"]["parent_block"]
        self.nonce = data["header"]["nonce"]
        # import transactions
        for trans in data["body"]["transactions"]:
            t = Transaction(trans["from"], trans["to"], trans["amount"])
            self.transactions.append(t)
        print('block loaded:\n', self.get_json())

        f.close()

    def get_json(self):
        # Rebuild the json from local block info
        block_dict = {
            "header": {
                "block_number": self.block_number,
                "parent_block": self.parent_block,
                "nonce": self.nonce,
            },
            "body": {
                "transactions": [],
            },
        }
        for trans in self.transactions:
            block_dict["body"]["transactions"].append(trans.get_json())
        # TODO: necessary to generate a new file? (json.dump)
        return json.dumps(block_dict).encode("utf-8")

    def increase_nonce(self):
        """
        Completar la funcion increase_nonce() de manera que se incremente
        el valor de la variable `nonce` del objeto Block.
        """
        ## --- Espacio para rellenar ---
        self.nonce += 1

        ## --- Fin de espacio ---

    def get_hash(self):
        """
        Completar la funcion get_hash() del objeto Block para que devuelva el 
        valor hash de la version serializada del bloque.

        Para ello se deberá usar la función `sha256` de la librería `hashlib`

        NOTA: La función contiene 2 líneas extra que se encarga de simplificar 
        el tamaño de las variables que luego se van a usar. Se recomienda no tocar
        nada fuera del espacio asignado para rellenar.
        """

        ## --- Espacio para rellenar ---
        hash = hashlib.sha256(self.get_json())
        
        ## --- Fin de espacio ---

        # Do not touch 
        # Format the hash value into an integer 
        # Apply 64 bit mask to simplify mask operators 
        hash = int('0x'+hash.hexdigest(), 0)
        hash = 0xFFFFFFFFFFFF & hash   
        return hash
    
    def check_valid_transactions(self, balances):

        ## --- Espacio para rellenar ---
        balances_copy = balances.copy()
        for transfer in self.transactions:
            if not transfer.valid(balances_copy):
                return False

        ## --- Fin de espacio ---

        return True

class Transaction():
    t_from = ""
    t_to = ""
    t_amount = 0
    balances_db = ""

    def __init__(self, t_from, t_to, t_amount):
        self.t_from = t_from
        self.t_to = t_to
        self.t_amount = t_amount
    
    # TODO: Could be nice to implement something like that to see if they are valid
    def valid(self, input_balances):
        """
        This method will receive the balances dictionary as an input.
        Then, it needs to check if all transactions can be executed according to the current balances.
        It returns true if all transactions can be executed or false if any cannot be executed.
        """

        ## --- Espacio para rellenar ---

        if input_balances[self.t_from] < self.t_amount:
            # if the balance is less than the transfer amount, the transaction is not valid
            return False
        
        # update balances for each person
        input_balances[self.t_from] = input_balances[self.t_from] - self.t_amount
        input_balances[self.t_to] = input_balances[self.t_to] + self.t_amount
        
        
        ## --- Fin de espacio ---

        return True


    def get_json(self):
        return {
            "from": self.t_from,
            "to": self.t_to,
            "amount": self.t_amount,
        }
    
    def __str__(self):
        return str(self.get_json())

def import_balances(input_file):

    """
    This method will import a json containing the balances of the different participants of the blockchain
    """
    # read the json file
    print('loading json file', input_file)
    f = open(input_file, 'r') # open in read mode
    data = json.load(f) # load json format
    print('balances loaded:\n', data)
    return data

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='PoW example')
    parser.add_argument('--input', type=str,
                        help='input file to generate the hash')
    parser.add_argument('--difficulty', type=int, 
                        help='define the difficulty level of PoW')
    parser.add_argument('--balances', type=str, 
                        help='define the balances file')
    args = parser.parse_args()
    main(args)
