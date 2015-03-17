require 'eaal'

class User < ActiveRecord::Base
  has_secure_password
  alias_attribute :admin?, :is_admin

  def name
    ensure_api_user
    @api.scope = 'char'
    begin
      @api.CharacterSheet(characterID: userid).name
    rescue EAAL::Exception::EAALError
      '?'
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
      @api.CharacterSheet(characterID: userid).corporationID.to_i
    rescue EAAL::Exception::EAALError
      0
    end
  end

  def characters
    ensure_api_user
    begin
      @api.Characters.characters
    rescue EAAL::Exception::EAALError
      []
    end
  end

  private
  def ensure_api_user
    @api ||= EAAL::API.new(api_key, api_verify)
  end
end
