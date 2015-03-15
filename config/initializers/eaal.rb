require 'eaal'

EAAL.cache = EAAL::Cache::FileCache.new("#{Rails.root}/tmp/eaal")
