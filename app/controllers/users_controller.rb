class UsersController < ApplicationController

  def signup
    if request.post?
      # do user create logic
      redirect_to root_url
    end
  end

  def login
    if request.post?
      if params[:username].nil? || params[:username].empty? ||
         params[:password].nil? || params[:password].empty?
        flash.now[:alert] = 'Both a character name and password are required.'
        render 'login' and return
      end
      user = User.find_by(name: params[:username])
      if user.nil? || !user.authenticate(params[:password])
        flash.now[:alert] = 'Incorrect character name or password.'
        render 'login' and return
      end

      flash.now[:alert] = 'Login successful.'
      render 'login' and return
      # redirect_to root_url
    end
  end

  def logout
    if request.post?
      # do user logout logic
      redirect_to root_url
    end
  end

  def reset
    if request.post?
      # do user reset logic
    end
  end
end
