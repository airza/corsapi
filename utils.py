def valid_login(username,password):
  return any([el[0]==username and el[1]==password for el in user_database])

user_database= [
  ['john_labelle','pizzatime','012401240','super bacon pizza'],
  ['mando_borgowitz','password1','49949','unicorn meat pizza'],
  ['dj_khaleed','4z49~W35^~','23','nineties kid pizza']
]


def return_record(username):
  record = [i for i in user_database if i[0]==username]
  if not record:
    return None
  record = record[0]
  return {
    'username':record[0],
    'pizzaClubId':record[2],
    'favoritePizza':record[3]
  }

