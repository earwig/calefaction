class CreateUsers < ActiveRecord::Migration
  def change
    create_table :users do |t|
      t.string :name
      t.string :email
      t.string :password_digest
      t.string :api_key
      t.string :api_verify
      t.boolean :is_admin
      t.boolean :is_corp

      t.timestamps null: false
    end
  end
end
