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


class Authorizer_User(Base):
	__tablename__ = 'auth_users'
	auth_id = Column(String(16), primary_key=True)
	preferred_comms = Column(Integer)
	contact_info = Column(String(255))

	def __init__(self, preferred_comms=None, contact_info=None):
		self.auth_id = generate_uuid()
		self.preferred_comms = preferred_comms
		self.contact_info = contact_info

	def __repr__(self):
		return '<User %r>: %r: %r' % self.data_id, self.preferred_comms, self.contact_info


class Policy(Base):
	__tablename__ = 'policies'
	policy_id = Column(String(16), primary_key=True)
	data_id = Column(String(16))
	group_id = Column(String(16))
	column_name = Column(String(255))
	table_name = Column(String(255))
	expiration = Column(DateTime())
	policy_bitwise = Column(Integer)

	def __init__(self, data_id=None, authorizers=None, column_name=None, table_name=None, expiration=None, policy_bitwise=None):
		self.policy_id = generate_uuid()
		self.data_id = data_id
		self.group_id = generate_uuid()
		self.column_name = column_name
		self.table_name = table_name
		self.expiration = expiration
		self.policy_bitwise = policy_bitwise

	def __repr__(self):
		return '<Policy %r>: %r | %r' % self.policy_id, self.data_id, self.policy_bitwise

class Pending_Policy(Base):
	__tablename__ = 'pending_policies'
	id = Column(String(16), primary_key=True)
	policy_id = Column(String(16))
	command = Column(String(255))
	expiration = Column(DateTime)
	authGroupId = Column(String(16))

class Group(Base):
	__tablename__ = 'groups'
	group_id = Column(String(16), primary_key=True)
	auth_id = Column(String(16))

	def __init__(self, auth_id=None, group_id=None):
		self.auth_id = auth_id
		self.group_id = group_id

class Pending_Auths(Base):
	__tablename__ = 'pending_auths'
	group_id = Column(String(16), primary_key=True)
	auth_id = Column(String(16))

	def __init__(self, auth_id=None, group_id=None):
		self.auth_id = auth_id
		self.group_id = group_id
