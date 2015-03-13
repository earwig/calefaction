class AdminSetting < ActiveRecord::Base

  def self.get(key)
    self.find_by(key: key).value
  end
end
