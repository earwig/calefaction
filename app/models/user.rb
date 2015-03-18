require 'calefaction/eve'

class User < ActiveRecord::Base
  has_secure_password
  alias_attribute :admin?, :is_admin

  def characters
    chars = api.characters
    chars.nil? ? [] : chars
  end

  def name
    sheet = api.character_sheet(char_id)
    sheet.nil? ? '?' : sheet.name
  end

  def corp_id
    sheet = api.character_sheet(char_id)
    sheet.nil? ? 0 : sheet.corporationID.to_i
  end

  def member_of?(corp)
    corp_id == corp
  end

  def in_corp?
    member_of? AdminSetting.get(:corp_id).to_i
  end

  private
  def api
    @api ||= Calefaction::EVE::APIUser.new(api_key, api_verify)
  end
end
