require 'calefaction/eve'

class User < ActiveRecord::Base
  has_secure_password
  alias_attribute :admin?, :is_admin

  def characters
    ensure_api_user
    chars = @api.characters
    chars.nil? ? [] : chars
  end

  def name
    ensure_api_user
    sheet = @api.character_sheet(userid)
    sheet.nil? ? '?' : sheet.name
  end

  def corp_id
    ensure_api_user
    sheet = @api.character_sheet(userid)
    sheet.nil? ? 0 : sheet.corporationID.to_i
  end

  def member_of?(corp)
    corp_id == corp
  end

  def in_corp?
    member_of? AdminSetting.get(:corp_id).to_i
  end

  private
  def ensure_api_user
    @api ||= Calefaction::EVE::APIUser.new(api_key, api_verify)
  end
end
