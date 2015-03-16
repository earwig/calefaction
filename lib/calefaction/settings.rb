module Calefaction::Settings
  extend self

  SETTINGS = [
    {key: :site_name,      type: :string,  label: 'Site name'},
    {key: :corp_name,      type: :string,  label: 'Corporation name'},
    {key: :corp_id,        type: :integer, label: 'Corporation ID'},
    {key: :description,    type: :markup,  label: 'Welcome message'},
    {key: :copyright,      type: :string,  label: 'Copyright'},
    {key: :allow_non_corp, type: :boolean, label: 'Allow non-corp members'}
  ]

  def update(params)
    SETTINGS.each do |setting|
      key = setting[:key]
      case setting[:type]
      when :string, :integer, :markup
        AdminSetting.set(key, params[key]) if params.has_key?(key)
      when :boolean
        AdminSetting.set_bool(key, params.has_key?(key))
      end
    end
  end
end
