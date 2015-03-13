# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

AdminSetting.add('site_name',   'Your Corporation\'s Site')
AdminSetting.add('corp_name',   'Your Corporation')
AdminSetting.add('corp_id',     '1')
AdminSetting.add('copyright',   'Your Corporation/Your Name')
AdminSetting.add('description',
  'Welcome to your corporation\'s website! This message can be changed in the admin settings panel.')
