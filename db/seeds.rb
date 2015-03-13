# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

AdminSetting.create(key: 'site_name',   value: 'Your Corporation Site')
AdminSetting.create(key: 'corporation', value: 'Your Corporation')
AdminSetting.create(key: 'description', value: 'Your corporation\'s description goes here!')
AdminSetting.create(key: 'copyright',   value: 'Your Corporation/Your Name')
