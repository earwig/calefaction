require 'io/console'

namespace :calefaction do
  desc "Sets some initial database values and creates an admin user"
  task setup: :environment do
    print "Enter your corporation's name: "
    corp_name = STDIN.gets.chomp

    print "\nEnter your corporation's ID (this is visible in the URL for "\
          "your corp's page on \nzKillboard, among other places): "
    corp_id = STDIN.gets.chomp.to_i
    if corp_id <= 0
      puts 'Corporation ID must be a positive integer. Stopping.'
      next
    end

    print "\nEnter your character's name: "
    user_name = STDIN.gets.chomp

    print "\nEnter your email address (used for password resets; may be blank): "
    user_email = STDIN.gets.chomp
    user_email = nil if user_email.empty?

    print "\nEnter your new password (to log in to the website, **NOT** for EVE!): "
    user_pass = STDIN.noecho(&:gets).chomp
    puts

    print "\nConfirm the password: "
    if user_pass != STDIN.noecho(&:gets).chomp
      puts "\nPasswords do not match. Stopping."
      next
    end
    puts

    print "\nEnter your character's API key ID (create one at\n"\
          "https://community.eveonline.com/support/api-key/createpredefined?accessMask=8): "
    user_api_key = STDIN.gets.chomp

    print "\nEnter the verification code for the key you just entered: "
    user_api_verify = STDIN.gets.chomp

    User.transaction do
      AdminSetting.where(key: %w(corp_name site_name)).update_all(value: corp_name)
      AdminSetting.find_by(key: 'corp_id').update(value: corp_id)
      user = User.new(name: user_name, email: user_email, password: user_pass,
                      api_key: user_api_key, api_verify: user_api_verify,
                      is_admin: true, is_corp: true)
      unless user.member_of? corp_id
        puts 'You are not a member of the given corporation. Stopping.'
        raise ActiveRecord::Rollback
      end
      user.save
    end
  end
end
