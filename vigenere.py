import string

def load_words(file_name):
  # inFile: file
  inFile = open(file_name, 'r')
  # wordlist: list of strings
  wordlist = []
  for line in inFile:
    wordlist.extend([word.lower() for word in line.split(' ')])
  return wordlist

def is_word(word_list, word):
  word = word.lower()
  word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
  return word in word_list

WORDLIST_FILENAME = 'words.txt'

class Message(object):
  def __init__(self, text):
    self.message_text = text
    self.valid_words  = load_words(WORDLIST_FILENAME)

  def get_message_text(self):
    return self.message_text

  def get_valid_words(self):
    return self.valid_words.copy()

  def shift_letter(self, letter, key):
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
    self.message_text = text
    self.valid_words = load_words(WORDLIST_FILENAME)
    self.key = key
    self.message_text_encrypted = self.apply_vigenere(key)

  def get_key(self):
    return list.copy(self.key)

  def get_message_text_encrypted(self):
    return self.message_text_encrypted

  def change_key(self, key):
    self.key = key
    self.message_text_encrypted = self.apply_vigenere(key)

class CiphertextMessage(Message):
  def __init__(self, text):
    self.message_text = text
    self.valid_words = load_words(WORDLIST_FILENAME)

  def decrypt_message(self):
    key_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    key_list = []
    for first in key_values:
      key_list.append([first])
      for second in key_values:
        if not (first == second):
          key_list.append([first,second])
        for third in key_values:
          if not (first == second and first == third):
            key_list.append([first, second,third])
    best_score = 0
    best_key = []
    for key in key_list:
      score = 0
      word_list = []

      negative_key = [element * -1 for element in key]
      decrypted_message = self.apply_vigenere(negative_key)
      word_list.extend([word for word in decrypted_message.split(' ')])
      for word in word_list:
        if is_word(self.valid_words,word):
          score+=1
      if score > best_score:
        best_score = score
        best_key = key

    negative_key = [element * -1 for element in best_key]
    decrypted_message = self.apply_vigenere(negative_key)
    return (best_key, decrypted_message)



if __name__ == '__main__':    
  ciphertext = CiphertextMessage('"Drmu spna vwvu bz ay nbmhd zmqlxbpcbz boo dkg dpli ky ay nbmhd teapmqhxa kvk ijdwyc, mqcstpjiaswu epvt tctz ay arm xmed sodlv" [Jysiu Oyomuo]')
  decrypted = ciphertext.decrypt_message()
  print(decrypted[1])
  pass
