import string

### HELPER CODE ###
def load_words(file_name):
  '''
  file_name (string): the name of the file containing
  the list of words to load

  Returns: a list of valid words. Words are strings of lowercase letters.

  Depending on the size of the word list, this function may
  take a while to finish.
  '''
  # inFile: file
  inFile = open(file_name, 'r')
  # wordlist: list of strings
  wordlist = []
  for line in inFile:
    wordlist.extend([word.lower() for word in line.split(' ')])
  return wordlist

def is_word(word_list, word):
  '''
  Determines if word is a valid word, ignoring
  capitalization and punctuation

  word_list (list): list of words in the dictionary.
  word (string): a possible word.

  Returns: True if word is in word_list, False otherwise

  For Example: is_word(word_list, 'bat') returns True
  and is_word(word_list, 'asdf') returns False
  '''
  word = word.lower()
  word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
  return word in word_list

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
  def __init__(self, text):
    '''
    Initializes a Message object

    text (string): the message's text

    a Message object has two attributes:
        self.message_text (string, determined by input text)
        self.valid_words (list, determined using helper function load_words)
    '''
    self.message_text = text
    self.valid_words  = load_words(WORDLIST_FILENAME)


  def get_message_text(self):
    '''
    Used to safely access self.message_text outside of the class
    Returns: self.message_text
    '''
    return self.message_text

  def get_valid_words(self):
    '''
    Used to safely access a copy of self.valid_words outside of the class.
    This helps you avoid accidentally mutating class attributes.

    Returns: a COPY of self.valid_words
    '''
    return self.valid_words.copy()

  def shift_letter(self, letter, key):
    '''
    letter (string of length 1)
    key (an integer)
    shifts the letter by key and returns the shifted letter
    '''
    lower_case_letters = string.ascii_lowercase
    upper_case_letters = string.ascii_uppercase
    if letter in lower_case_letters:
      letter_index = lower_case_letters.index(letter) + key
      if (letter_index >= len(lower_case_letters)):
        letter_index -= len(lower_case_letters)
      elif (letter_index < 0):
        letter_index += len(lower_case_letters)
      return lower_case_letters[letter_index]
    elif letter in upper_case_letters:
      letter_index = upper_case_letters.index(letter) + key
      if (letter_index >= len(upper_case_letters)):
        letter_index -= len(upper_case_letters)
      elif (letter_index < 0):
        letter_index += len(upper_case_letters)
      return upper_case_letters[letter_index]
    else:
      return letter

  def apply_vigenere(self, key):
    '''
    Applies the Vigenere Cipher to self.message_text with the input key.
    Creates a new string that is self.message_text such that each letter
    has been shifted by some number of characters determined by key.
    Uses the shift_letter method above.

    key (list of integers): the key to encrypt the message.

    Returns: the message text (string) encrypted by key
    '''
    message_length = len(self.message_text)
    key_length = len(key)
    new_key = []
    for counter in range(message_length):
      new_key.append(key[counter % key_length])

    encrypted_word = []
    for letter,key_index in zip(self.message_text,new_key):
      encrypted_word.append(self.shift_letter(letter,key_index))
    return "".join(encrypted_word)


class PlaintextMessage(Message):
  def __init__(self, text, key):
    '''
    Initializes a PlaintextMessage object

    text (string): the message's text
    key (list of integers): the key associated with this message

    A PlaintextMessage object inherits from Message and has four attributes:
        self.message_text (string, determined by input text)
        self.valid_words (list, determined using helper function load_words)
        self.key (list of integers, determined by input key)
        self.message_text_encrypted (string, created using self.message_text and self.key)

    '''
    self.message_text = text
    self.valid_words = load_words(WORDLIST_FILENAME)
    self.key = key
    self.message_text_encrypted = self.apply_vigenere(key)

  def get_key(self):
    '''
    Used to safely access self.key outside of the class

    Returns: a COPY of self.key
    '''
    return list.copy(self.key)

  def get_message_text_encrypted(self):
    '''
    Used to safely access self.message_text_encrypted outside of the class
    Returns: self.message_text_encrypted
    '''
    return self.message_text_encrypted

  def change_key(self, key):
    '''
    Changes self.key of the PlaintextMessage and updates other
    attributes determined by key.

    key (list of integers): the new key that should be associated with this message.

    Returns: nothing
    '''
    self.key = key
    self.message_text_encrypted = self.apply_vigenere(key)


# def generate_powerset(input_set):
#   if len(input_set) == 0:
#     return [[]]
#   else:
#     powerset_list = generate_powerset(input_set[:-1])  # Recursion
#     for counter in range(len(powerset_list)):
#       powerset_list.append(powerset_list[counter] + [input_set[-1]])
#     return powerset_list


class CiphertextMessage(Message):
  def __init__(self, text):
    '''
    Initializes a CiphertextMessage object

    text (string): the message's text

    a CiphertextMessage object has two attributes:
        self.message_text (string, determined by input text)
        self.valid_words (list, determined using helper function load_words)
    '''
    self.message_text = text
    self.valid_words = load_words(WORDLIST_FILENAME)

  def decrypt_message(self):
    '''
    Decrypt self.message_text by trying every possible key value
    and find the "best" one. We will define "best" as the key that
    creates the maximum number of real words when we use apply_vigenere(key)
    on the message text. If [k0, k1, k2, ...] is the original key used to
    encrypt the message, then we would expect [26-k0, 26-k1, 26-k2,...] to
    be the best key for decrypting it.

    IMPORTANT NOTE1: FOR THIS PART, ONLY CONSIDER THE KEYS WITH LENGTH UP TO 3. ALSO ASSUME THAT EACH VALUE IN THE KEY IS NOT GREATER THAN 12.
    OTHERWISE IT WILL TAKE VERY VERY LONG TIME TO FINISH.

    IMPORTANT NOTE2: RETURN THE SHORTEST FORM OF A KEY. FOR EXAMPLE THE KEYS
    [2,2,2] AND [2] ARE EQUAL. AND IN SUCH CASES YOU SHOULD RETURN THE SHORTER
    ONE.

    Note: if multiple keys are equally good such that they all create
    the maximum number of valid words, you may choose any of those key
    (and their corresponding decrypted messages) to return

    Returns: a tuple of the best key used to decrypt the message
    and the decrypted message text using that key
    '''
    key = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    key_powersets = generate_powerset(key)
    key_list = []
    best_score = 0
    best_key = []
    for value in key_powersets:
      if len(value) > 0 and len(value) <= 3:
        key_list.append(value)
    if [7,8,12] in key_list:
      print("True")
      print(key_list.index([8,11, 12]))
      print(key_list.index([7,8,12]))
      print(len(key_list))
    for key in key_list:
      score = 0
      word_list = []

      negative_key = [element * -1 for element in key]
      decrypted_message = self.apply_vigenere(negative_key)
      word_list.extend([word for word in decrypted_message.split(' ')])
      for word in word_list:
        if is_word(self.valid_words,word):
          score+=1
      if score >= best_score:
        best_score = score
        best_key = key

    negative_key = [element * -1 for element in best_key]
    decrypted_message = self.apply_vigenere(negative_key)

    return (best_key, decrypted_message)



if __name__ == '__main__':    
  '''
  Can you find out what this hidden message says?
  Uncomment the next lines to find out!
  '''
  ciphertext = CiphertextMessage('"Drmu spna vwvu bz ay nbmhd zmqlxbpcbz boo dkg dpli ky ay nbmhd teapmqhxa kvk ijdwyc, mqcstpjiaswu epvt tctz ay arm xmed sodlv" [Jysiu Oyomuo]')
  decrypted = ciphertext.decrypt_message()
  print(decrypted[1])
  pass
