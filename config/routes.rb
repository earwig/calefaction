Rails.application.routes.draw do
  root 'tools#index'

  get '/signup' => 'users#create'
  get '/login'  => 'users#login'

  get '/admin'  => 'admin#index'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

end
