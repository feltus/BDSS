from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer, String, Text

from .common import BaseModel

class SSHKey(BaseModel):

    __tablename__ = 'ssh_keys'

    __table_args__ = (
        # Prevent duplicate keys for a user/host pair.
        UniqueConstraint('owner_id', 'destination', name='_duplicate_keys_constraint'),
    )

    ## @var id
    #  Unique ID for this key.
    id = Column(Integer(), primary_key=True, nullable=False)

    ## @var owner_id
    #  The ID of the user who owns this key.
    owner_id = Column(Integer(), ForeignKey('users.id'), nullable=False)

    ## @var destination
    #  The data destination this key is for. This corresponds to a key
    #  in config/data_destinations.yml.
    destination = Column(String(100), nullable=False)

    ## @var username
    #  The user's username on the destination host.
    username = Column(String(50), nullable=False)

    ## @var public
    #  The public key.
    public = Column(Text(), nullable=False)

    ## @var private
    #  The private key.
    private = Column(Text(), nullable=False)
