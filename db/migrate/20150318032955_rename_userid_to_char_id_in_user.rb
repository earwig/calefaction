class RenameUseridToCharIdInUser < ActiveRecord::Migration
  def change
    rename_column :users, :userid, :char_id
  end
end
