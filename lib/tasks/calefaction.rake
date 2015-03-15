require 'io/console'

namespace :calefaction do
  desc "Sets some initial database values and creates an admin user"
  task setup: :environment do
    print "Enter your corporation's name: "
    corp_name = STDIN.gets.chomp

    print "\nEnter your corporation's ID (this is visible in the URL for "\
          "your corp's page on \nzKillboard, among other places): "
    corp_id = STDIN.gets.to_i
    if corp_id <= 0
      puts 'Corporation ID must be a positive integer. Stopping.'
      next
    end

    print "\nEnter your character's API key ID (create one at\n"\
          "https://community.eveonline.com/support/api-key/createpredefined?accessMask=8): "
    user_api_key = STDIN.gets.chomp

    print "\nEnter the verification code for the key you just entered: "
    user_api_verify = STDIN.gets.chomp

    user = User.new(api_key: user_api_key, api_verify: user_api_verify,
                    is_admin: true, is_corp: true)
    chars = user.char_names
    if chars.empty?
      puts "The given API key is invalid, has no characters, or something "\
           "else is wrong\nwith the EVE API right now..."
      next
    end

    if chars.length == 1
      user.name = chars.first
    else
      puts "\nChoose a character:"
      chars.each_with_index do |name, i|
        puts "  [#{i}]: #{name}"
      end
      puts "Enter the number next to your chosen character: "
      loop do
        index = STDIN.gets.to_i
        break unless index >= chars.length || index < 0
        puts "Bad input; try again: "
      end
      user.name = chars[index]
    end

    unless user.member_of? corp_id
      puts 'You are not a member of the given corporation. Stopping.'
      next
    end

    print "\nEnter your email address (used for password resets; may be blank): "
    user.email = STDIN.gets.chomp
    user.email = nil if user.email.empty?

    print "\nEnter your new password (to log in to the website, **NOT** for EVE!): "
    user.password = STDIN.noecho(&:gets).chomp
    puts

    print "\nConfirm the password: "
    if user.password != STDIN.noecho(&:gets).chomp
      puts "\nPasswords do not match. Stopping."
      next
    end
    puts

    AdminSetting.where(key: %w(corp_name site_name)).update_all(value: corp_name)
    AdminSetting.find_by(key: 'corp_id').update(value: corp_id)
    user.save

    puts "\nDone!"
  end
end
