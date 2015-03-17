class ReplaceNameWithIdInUser < ActiveRecord::Migration
  def change
    remove_column :users, :name, :string
    add_column :users, :userid, :integer, first: true
  end
end
