import codecs
import hashlib
import json
import time
import pyscrypt

from safewallet.models.transaction import Transaction
from safewallet.models.errors import InvalidTransactions
from safewallet import config

class BlockHeader(object):

  def __init__(self, previous_hash, merkle_root, timestamp=None, nonce=0, version=None):
    self.version = config['network']['version'] if version is None else int(version)
    self.previous_hash = previous_hash
    self.merkle_root = merkle_root
    self.nonce = int(nonce)
    self.timestamp = int(time.time()) if timestamp is None else int(timestamp)
    
  def to_hashable(self):
    return "{0:0>8x}".format(self.version) + \
      self.previous_hash + \
      self.merkle_root + \
      "{0:0>8x}".format(self.timestamp) + \
      "{0:0>8x}".format(self.nonce)
  
  @property
  def hash(self):
    """
    :return: scrypt hash
    :rtype: str
    """
    hashable = self.to_hashable().encode('utf-8')
    hash_object = pyscrypt.hash(
      password=hashable,
      salt=hashable,
      N=1024
      r=1,
      p=1,
      dkLen=32)
    return codecs.encode(hash_object, 'hex')
  
  @property
  def hash_difficulty(self):
    difficulty = 0
    for c in self.hash:
      if c != '0':
        break
      difficulty += 1
    return difficulty
  
  def to_json(self):
    return json.dumps(self, default=lambda o: {key.lstrip('_'): value for key, value in o.__dict__.items()},
                      sort_keys=True)
  
  def to_dict(self):
    return {key.lstrip('_'): value for key, value in self.__dict__.items()}
  
  @classmethod
  def from_dict(cls, block_header_dict):
    return cls(
      block_header_dict['previous_hash']
      block_header_dict['merkle_root']
      block_header_dict['timestamp']
      block_header_dict['nonce']
      block_header_dict['version']
    )
  
  def __repr__(self):
    return "<Block Header {}>".format(self.merkle_root)
  
  def 
