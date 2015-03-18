require 'io/console'

namespace :calefaction do
  desc "Set some initial database values and creates an admin user"
  task setup: :environment do
    begin
      AdminSetting.get(:test)
    rescue ActiveRecord::StatementInvalid
      puts "The database has not been set up properly. You need to run\n"\
           "`rake db:setup` first."
      next
    end

    if AdminSetting.get(:corp_id).nil?
      puts "The database does not contain the correct seed values. You need "\
           "to run\n`rake db:reset tmp:cache:clear` first."
      next
    end

    if AdminSetting.get(:corp_id).to_i > 0
      puts "The database is not empty; you should change settings from "\
           "within the\napplication. Alternatively, you can start over with\n"\
           "`rake db:reset tmp:cache:clear calefaction:setup`."
      next
    end

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
    api_key = STDIN.gets.chomp

    print "\nEnter the verification code for the key you just entered: "
    api_verify = STDIN.gets.chomp

    user = User.new(api_key: api_key, api_verify: api_verify, admin?: true)
    chars = user.characters
    if chars.empty?
      puts "The given API key is invalid, has no characters, or something "\
           "else is wrong\nwith the EVE API right now..."
      next
    end

    if chars.length == 1
      puts "\nUsing character: #{chars.first.name}"
      user.char_id = chars.first.characterID
    else
      puts "\nChoose a character:"
      chars.each_with_index do |char, i|
        puts "  [#{i}]: #{char.name}"
      end
      print "Enter the number next to your chosen character: "
      loop do
        index = STDIN.gets.to_i
        if index >= 0 && index < chars.length
          user.char_id = chars[index].characterID and break
        end
        print "Bad input; try again: "
      end
    end

    unless user.member_of? corp_id
      puts 'You are not a member of the given corporation. Stopping.'
      next
    end

    print "\nEnter your email address (required; used to log in): "
    user.email = STDIN.gets.chomp
    if user.email.blank?
      puts "\nInvalid email address. Stopping."
      next
    end

    print "\nEnter your new password (to log in to the website, **NOT** for EVE!): "
    user.password = STDIN.noecho(&:gets).chomp
    puts

    print "\nConfirm the password: "
    if user.password != STDIN.noecho(&:gets).chomp
      puts "\nPasswords do not match. Stopping."
      next
    end
    puts

    AdminSetting.set(:corp_name, corp_name)
    AdminSetting.set(:site_name, corp_name)
    AdminSetting.set(:corp_id, corp_id)
    user.save
    puts "\nDone!"
  end
end
