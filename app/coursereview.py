

class Department(object):
  def __init__(self, code, name):
    self.code = code
    self.name = name

class Course(object):
  def __init__(self, number, title, description):
    self.number = number
    self.title = title
    self.description = description

class Instructor(object):
  def __init__(self, name, title, address, phone, email):
    self.name = name
    self.title = title
    self.address = address
    self.phone = phone
    self.email = email
