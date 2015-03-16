module AdminHelper

  def setting_tag(setting)
    key = "settings[#{setting[:key]}]"
    value = AdminSetting.get(setting[:key])

    case setting[:type]
    when :string
      text_field_tag(key, value, size: '40')
    when :integer
      text_field_tag(key, value, size: '10')
    when :markup
      text_area_tag(key, value, size: '60x5')
    when :boolean
      check_box_tag(key, '1', value == 't')
    end
  end
end
