module ToolsHelper

  def get_description
    AdminSetting.get('description')
  end
end
