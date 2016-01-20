# encoding: utf-8
# filename: common/spec_helper.rb

require 'rspec'
require 'appium_lib'
require 'sauce_whisk'

def using_sauce
	user = ENV['SAUCE_USERNAME']
	key  = ENV['SAUCE_ACCESS_KEY']
	user && !user.empty? && key && !key.empty?
end

def upload_app
	storage = SauceWhisk::Storage.new
	app = @caps[:caps][:app]
	storage.upload app

	@caps[:caps][:app] = "sauce-storage:#{File.basename(app)}"
end

def setup_driver
	return if $driver
	@caps = Appium.load_appium_txt file: File.join(Dir.pwd, './common/appium.txt')
	# if using_sauce
	# 	upload_app
	# 	@caps[:caps].delete :avd # re: https://github.com/appium/ruby_lib/issues/241
	# end
	Appium::Driver.new @caps
end

def promote_methods
	Appium.promote_singleton_appium_methods Pages
	Appium.promote_appium_methods RSpec::Core::ExampleGroup
end

setup_driver
promote_methods

RSpec.configure do |config|

	config.before(:each) do
		$driver.start_driver
	end

	config.after(:each) do
		driver_quit
	end
end
