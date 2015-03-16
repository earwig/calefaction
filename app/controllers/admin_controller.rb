class AdminController < ApplicationController
  def index
  end

  def update
    if params[:settings].is_a? Hash
      params[:settings].each do |key, value|
        AdminSetting.set(key, value)
      end
    end
    flash.now[:notice] = 'Admin settings updated.'
    render 'index'
  end
end
