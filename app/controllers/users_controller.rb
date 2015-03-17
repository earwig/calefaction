class UsersController < ApplicationController

  def signup
    if request.post?
      # do user create logic
      redirect_to root_url
    end
  end

  def login
    if request.post?
      if params[:username].blank? || params[:password].blank?
        flash.now[:alert] = 'Both a character name and password are required.'
        render 'login' and return
      end

      user = User.find_by(name: params[:username])
      if user.nil? || !user.authenticate(params[:password])
        flash.now[:alert] = 'Incorrect character name or password.'
        render 'login' and return
      end

      allow_non_corp = AdminSettings.get_bool(:allow_non_corp)
      if !allow_non_corp && !user.in_corp? && !user.admin?
        corp_name = AdminSettings.get_bool(:corp_name)
        flash[:alert] = "You are not a member of #{corp_name}, and access to "\
                        "this site is disallowed for non-corp members."
        redirect_to root_url and return
      end

      session[:user_id] = user.id
      flash[:notice] = 'Login successful!'
      redirect_to root_url
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
