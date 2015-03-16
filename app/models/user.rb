require 'eaal'

class User < ActiveRecord::Base
  has_secure_password
  alias_attribute :admin?, :is_admin
  alias_attribute :corp?, :is_corp

  def char_names
    ensure_api_user
    begin
      @api.Characters.characters.map { |char| char.name }
    rescue EAAL::EAALError
      []
    end
  end

  def member_of?(corp_id)
    ensure_api_user
    @api.scope = 'char'
    begin
      @api.CharacterSheet(names: name).corporationID.to_i == corp_id
    rescue EAAL::EAALError
      false
    end
  end

  private
  def ensure_api_user
    @api ||= EAAL::API.new(api_key, api_verify)
  end
end
