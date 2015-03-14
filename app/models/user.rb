# require 'calefaction/api/eveonline'

class User < ActiveRecord::Base
  include Encryptor
  has_secure_password

  def api_verify
    self.class.decrypt(super())
  end

  def api_verify=(value)
    super(self.class.encrypt(value))
  end

  def member_of?(corp_id)
    false
  end
end
