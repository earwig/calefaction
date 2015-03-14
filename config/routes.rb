Rails.application.routes.draw do
  root 'tools#index'

  get  '/login'  => 'users#login'
  get  '/signup' => 'users#signup'
  post '/signup' => 'users#create'

  get  '/admin'  => 'admin#index'
  post '/admin'  => 'admin#update'

  # routes for each tool go here, e.g.:
  # get 'tools#campaigns'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

end
