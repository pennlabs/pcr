

def capitalize(name):
  """Capitalize but account for roman numerals, so no "Calculus Iii" """
  roman_numerals = set(['I', 'II', 'III', 'IV']) 
  def cap_word(word): 
    return word.upper() if word.upper() in roman_numerals else word.capitalize()

  return " ".join(cap_word(word) for word in name.split(" "))
