require 'eaal'

module Calefaction::EVE
  extend self

  class APIUser
    def initialize(key_id=nil, vcode=nil)
      @api = EAAL::API.new(key_id, vcode)
    end

    def characters
      query('account') { @api.Characters.characters }
    end

    def character_sheet(char_id)
      query('char') { @api.CharacterSheet(characterID: char_id) }
    end

    def corporation_sheet(corp_id)
      query('corp') { @api.CorporationSheet(corporationID: corp_id) }
    end

    private
    def query(scope)
      @api.scope = scope
      begin
        yield
      rescue EAAL::Exception::EAALError
        nil
      end
    end
  end

  def corp_ticker(corp_id)
    cache_key = "calefaction/eve/corp_ticker/#{corp_id}"
    existing = Rails.cache.read(cache_key)
    return existing unless existing.nil?
    sheet = basic_api.corporation_sheet(corp_id)
    return '?' if sheet.nil?
    Rails.cache.write(cache_key, sheet.ticker)
    sheet.ticker
  end

  private
  def basic_api
    @@api ||= APIUser.new
  end
end
