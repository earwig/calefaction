# require 'calefaction/api/eveonline'

class User < ActiveRecord::Base
  has_secure_password

  def member_of?(corp_id)
    false
  end
end
