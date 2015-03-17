class RemoveIsCorpFromUser < ActiveRecord::Migration
  def change
    remove_column :users, :is_corp, :boolean
  end
end
