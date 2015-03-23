require 'calefaction/eve'
require 'calefaction/version'

module ApplicationHelper

  def get_title(title = '')
    base = AdminSetting.get(:site_name)
    title.empty? ? base : "#{title} : #{base}"
  end

  def corp_logo_url(size = 256)
    corp_id = AdminSetting.get(:corp_id)
    "https://image.eveonline.com/Corporation/#{corp_id}_#{size}.png"
  end

  def corp_logo_tag
    corp_name = AdminSetting.get(:corp_name)
    image_tag(corp_logo_url, title: corp_name, alt: "#{corp_name} Logo")
  end

  def copyright_year
    start = 2015
    year = Time.now.year
    year > start ? "#{start}–#{year}" : start
  end
end
