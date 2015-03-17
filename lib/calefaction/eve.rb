module Calefaction::EVE
  extend self

  def corp_ticker(corp_id)
    cache_key = "calefaction/eve/corp_ticker/#{corp_id}"
    existing = Rails.cache.read(cache_key)
    return existing unless existing.nil?
    ticker = get_corp_ticker_from_api(corp_id)
    return '?' if ticker.nil?
    Rails.cache.write(cache_key, ticker)
    ticker
  end

  private
  def get_corp_ticker_from_api(corp_id)
    ensure_api
    @@api.scope = 'corp'
    begin
      @@api.CorporationSheet(corporationID: corp_id).ticker
    rescue EAAL::EAALError
      nil
    end
  end

  def ensure_api
    @@api ||= EAAL::API.new(nil, nil)
  end
end
