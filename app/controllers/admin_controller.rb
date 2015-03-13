class AdminController < ApplicationController
  def index
  end

  def update
    if !params[:settings].nil?
      params[:settings].each do |key, value|
        ## assert in list of valid settings...
        ## only if changed (i.e. not equal to get)
        AdminSetting.set(key, value)
      end
    end
    render 'index'
  end
end
