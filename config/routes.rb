Rails.application.routes.draw do
  root 'tools#index'

  get  '/signup'   => 'users#signup'
  post '/signup'   => 'users#signup'
  get  '/login'    => 'users#login'
  post '/login'    => 'users#login'
  get  '/logout'   => 'users#logout'
  post '/logout'   => 'users#logout'
  get  '/reset'    => 'users#reset'
  post '/reset'    => 'users#reset'
  get  '/settings' => 'users#settings'
  post '/settings' => 'users#settings'

  get  '/admin'    => 'admin#index'
  post '/admin'    => 'admin#update'

  # routes for each tool go here, e.g.:
  # get 'tools#campaigns'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

end
