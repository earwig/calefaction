class AdminSetting < ActiveRecord::Base

  def self.to_bool(value)
    value == 't'
  end

  def self.from_bool(value)
    value ? 't' : 'f'
  end

  def self.add(key, value)
    value = self.from_bool(value) if value == true || value == false
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

  def self.get_bool(key)
    self.to_bool(self.get(key))
  end

  def self.set(key, value)
    existing = self.get(key)
    return false if existing.nil? || existing == value
    self.find_by(key: key).update(value: value)
    Rails.cache.write("admin_setting/#{key}", value)
    true
  end

  def self.set_bool(key, value)
    self.set(key, self.from_bool(value))
  end
end
