class AdminSetting < ActiveRecord::Base

  def self.add(key, value)
    self.create(key: key, value: value)
  end

  def self.get(key)
    existing = Rails.cache.read("admin_setting/#{key}")
    return existing unless existing.nil?
    setting = self.find_by(key: key)
    return nil if setting.nil?
    Rails.cache.write("admin_setting/#{key}", setting.value)
    setting.value
  end

  def self.set(key, value)
    existing = self.get(key)
    return if existing.nil? || existing == value
    self.find_by(key: key).update(value: value)
    Rails.cache.write("admin_setting/#{key}", value)
  end
end
