require 'eaal'

class User < ActiveRecord::Base
  has_secure_password
  alias_attribute :admin?, :is_admin

  def char_names
    ensure_api_user
    begin
      @api.Characters.characters.map { |char| char.name }
    rescue EAAL::EAALError
      []
    end
  end

  def in_corp?
    member_of? AdminSetting.get(:corp_id).to_i
  end

  def member_of?(corp)
    corp_id == corp
  end

  def corp_id
    ensure_api_user
    @api.scope = 'char'
    begin
      @api.CharacterSheet(names: name).corporationID.to_i
    rescue EAAL::EAALError
      0
    end
  end

  private
  def ensure_api_user
    @api ||= EAAL::API.new(api_key, api_verify)
  end
end
