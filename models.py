from sqlalchemy import Column, Binary, Integer, String, DateTime
from database import Base
from uuid import uuid4

def generate_uuid():
    return str(uuid4())[:16]

class Patient(Base):
	__tablename__ = 'patients'
	data_id = Column(String(16), primary_key=True)
	name = Column(String(64))
	auth_id = Column(String(16))
	medicine = Column(String(64))
	amount = Column(Integer)

	def __init__(self, name=None, auth_id=None, medicine=None, amount=None):
		self.data_id = generate_uuid()
		self.name = name
		self.auth_id = auth_id
		self.medicine = medicine
		self.amount = amount

	def get_object(self):
		return {
			'data_id': self.data_id,
			'name': self.name,
			'auth_id': self.auth_id,
			'medicine': self.medicine,
			'amount': self.amount
		}


class Authorizer_User(Base):
	__tablename__ = 'auth_users'
	auth_id = Column(String(16), primary_key=True)
	preferred_comms = Column(Integer)
	contact_info = Column(String(255))
	name = Column(String(255))

	def __init__(self, preferred_comms=None, contact_info=None, name=None):
		self.auth_id = generate_uuid()
		self.preferred_comms = preferred_comms
		self.contact_info = contact_info
		self.name = name
		
	def get_object(self):
		return {
			'auth_id': self.auth_id,
			'preferred_comms': self.preferred_comms,
			'contact_info': self.contact_info,
			'name': self.name
		}


class Policy(Base):
	__tablename__ = 'policies'
	policy_id = Column(String(16), primary_key=True)
	data_id = Column(String(16))
	group_id = Column(String(16))
	column_name = Column(String(255))
	table_name = Column(String(255))
	expiration = Column(DateTime())
	policy_bitwise = Column(Integer)

	def __init__(self, data_id=None, authorizers=None, group_id=None, column_name=None, table_name=None, expiration=None, policy_bitwise=None):
		self.policy_id = generate_uuid()
		self.data_id = data_id
		self.group_id = group_id
		self.column_name = column_name
		self.table_name = table_name
		self.expiration = expiration
		self.policy_bitwise = policy_bitwise

	def __repr__(self):
		return '<Policy %r>: %r | %r' % self.policy_id, self.data_id, self.policy_bitwise

	def get_object(self):
		return {
			'policy_id': self.policy_id,
			'data_id': self.data_id,
			'group_id': self.group_id,
			'column_name': self.column_name,
			'table_name': self.table_name,
			'expiration': self.expiration,
			'policy_bitwise': self.policy_bitwise
		}

class Pending_Policy(Base):
	__tablename__ = 'pending_policies'
	pending_id = Column(String(16), primary_key=True)
	policy_id = Column(String(16))
	command = Column(String(255))
	expiration = Column(DateTime)
	auth_group_id = Column(String(16))

	def __init__(self, policy_id, command, expiration, auth_group_id):
		self.pending_id = generate_uuid()
		self.policy_id = policy_id
		self.command = command
		self.expiration = expiration
		self.auth_group_id = auth_group_id


class Group(Base):
	__tablename__ = 'groups'
	group_id = Column(String(16), primary_key=True)
	auth_id = Column(String(16))

	def __init__(self, auth_id=None, group_id=None):
		self.auth_id = auth_id
		self.group_id = group_id

class Pending_Auth(Base):
	__tablename__ = 'pending_auths'
	group_id = Column(String(16), primary_key=True)
	auth_id = Column(String(16))
	comms_info = Column(String(64))

	def __init__(self, auth_id=None, group_id=None, comms_info=None):
		self.auth_id = auth_id
		self.group_id = group_id
		self.comms_info = comms_info

class History(Base):
	__tablename__ = 'history'
	history_id = Column(String(16), primary_key=True)
	data_id = Column(String(16))
	operation = Column(String(16))
	old_value = Column(String(64))
	new_value = Column(String(64))
	time_stamp = Column(DateTime())
	column_name = Column(String(255))
	table_name = Column(String(255))
	auth_id = Column(String(16))

	def __init__(self, data_id=None, operation=None, old_value=None, new_value=None, 
		time_stamp=None, column_name=None, table_name=None, auth_id=None):
		self.data_id = data_id
		self.operation = operation
		self.old_value = old_value
		self.new_value = new_value
		self.time_stamp = time_stamp
		self.column_name = column
		self.table_name = table
		self.auth_id = auth_id

	def get_object(self):
		return {
			"data_id": self.data_id,
			"operation": self.operation,
			"old_value": self.old_value,
			"new_value": self.new_value,
			"time_stamp": self.time_stamp,
			"column": self.column_name,
			"table": self.table_name,
			"auth_id": self.auth_id,
		}

