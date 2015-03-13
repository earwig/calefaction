class AdminSetting < ActiveRecord::Base

  def self.get(key)
    Rails.cache.fetch("admin_setting/#{key}") do
      self.find_by(key: key).value
    end
  end

  def self.set(key, value)
    self.find_by(key: key).update(value: value)
    Rails.cache.write("admin_setting/#{key}", value)
  end
end
