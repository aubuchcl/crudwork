import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

# in order to create our foreign key relationships / will also be used when we import our mapper
from sqlalchemy.orm import relationship

# used in the configuration code at the end of the file
from sqlalchemy import create_engine

# make an instance of the declarative_base class we just imported
Base = declarative_base()


# create classes that correspond to the tables we want to create in our database
class Restaurant(Base):
	# create a table representation
	__tablename__ = 'restaurant'

	name = Column(String(80), nullable = False)

	id = Column(Integer, primary_key = True)

class MenuItem(Base):
	# create a table representation
	__tablename__ = 'menu_item'

	name = Column(String(80), nullable = False)

	id = Column(Integer, primary_key = True)

	course = Column(String(250))

	description = Column(String(250))

	price = Column(String(8))

	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		return{
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'price': self.price,
			'course': self.course
		}

# end of file
engine = create_engine(
	'sqlite:///restaurantmenu.db')

# go into the database and adds the classes we will soon create as new tables in our database
Base.metadata.create_all(engine)