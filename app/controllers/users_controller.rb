class UsersController < ApplicationController

  def signup
    if request.post?
      # do user create logic
      redirect_to root_url
    end
  end

  def login
    if request.post?
      # do user login logic
      redirect_to root_url
    end
  end

  def logout
    if request.post?
      # do user logout logic
      redirect_to root_url
    end
  end
end
