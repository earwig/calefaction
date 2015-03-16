require 'calefaction/settings'

class AdminController < ApplicationController

  def index
  end

  def update
    if params[:settings].is_a? Hash
      Calefaction::Settings.update(params[:settings])
      flash.now[:notice] = 'Admin settings updated.'
    else
      # TODO: can we make a better error message for this?
      flash.now[:alert] = 'Something is wrong with the settings you submitted.'
    end
    render 'index'
  end
end
