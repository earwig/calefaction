require 'eaal'

module Calefaction::EVE
  extend self

  class APIUser
    def initialize(key_id, vcode)
      @api = EAAL::API.new(key_id, vcode)
    end

    def character_sheet(char_id)
      @api.scope = 'char'
      begin
        @api.CharacterSheet(characterID: char_id)
      rescue EAAL::Exception::EAALError
        nil
      end
    end

    def characters
      @api.scope = 'account'
      begin
        @api.Characters.characters
      rescue EAAL::Exception::EAALError
        nil
      end
    end
  end

  def corp_ticker(corp_id)
    cache_key = "calefaction/eve/corp_ticker/#{corp_id}"
    existing = Rails.cache.read(cache_key)
    return existing unless existing.nil?
    sheet = corporation_sheet(corp_id)
    return '?' if sheet.nil?
    Rails.cache.write(cache_key, sheet.ticker)
    sheet.ticker
  end

  private
  def corporation_sheet(corp_id)
    ensure_basic_api
    @@api.scope = 'corp'
    begin
      @@api.CorporationSheet(corporationID: corp_id)
    rescue EAAL::Exception::EAALError
      nil
    end
  end

  def ensure_basic_api
    @@api ||= EAAL::API.new(nil, nil)
  end
end
