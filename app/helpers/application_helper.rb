require 'calefaction/version'

module ApplicationHelper

  def get_title(title = '')
    base = AdminSetting.get('site_name')
    title.empty? ? base : "#{title} : #{base}"
  end

  def get_copyright_year
    start = 2015
    year = Time.now.year
    year > start ? "#{start}–#{year}" : start
  end

  def get_copyright_holders
    AdminSetting.get('copyright')
  end
end
