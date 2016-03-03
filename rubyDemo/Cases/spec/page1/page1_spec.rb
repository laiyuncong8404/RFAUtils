# encoding: utf-8
=begin
#运行本脚本前，请开启appium_server；
#手机API18(4.3)及以上，手机连接AP；#手机连接电脑; 
#WiFi模块工作在AP模式
#脚本中未做异常网络处理，因此网络需要稳定，平台连接稳定
=end

require 'rubygems'
require 'rspec'
require 'appium_lib'
require 'net/http'
require File.join(File.dirname(__FILE__),'..', '..','public_method')

APP_PATH = 'C:\\RFAUtils\\rubyDemo\\IceBoxControl_Marvell-MW300_20150921.apk'

def desired_caps
	{
		caps: {
			app:               APP_PATH,
			appActivity:      'com.iceboxcontrol.activitys.LoginActivity',
			appPackage:       'com.iceboxcontrol',
			platformName:     'android',
			platformVersion:  '4.4.4',#API:19
			deviceName:       '274b3f06',#MI 3真机
			# deviceName:       'emulator-5554',
			# platformVersion:  '5.1',#API:22
			# deviceName:       '15584d42', #MI 4真机
			unicodeKeyboard:  'true',
			resetKeyboard:    'true',
			noReset:       'false'
			# newCommandTimeout:'60'
		},
		appium_lib: {
			sauce_username: nil, # don't run on sauce
			sauce_access_key: nil,
			wait: 10,
		}
	}
end

describe 'iceboxcontrol_CHiQ1U_BM09_AP_mode' do
	before(:all) do
		@driver = Appium::Driver.new(desired_caps).start_driver
		Appium.promote_appium_methods RSpec::Core::ExampleGroup
		@username = "13540774227"
		@old_password = @new_password = "123456"
		@wrong_username = "13340774227"
		@wrong_password = @short_password = "12345"
		@new_nickname = "Lucy"
		@wrong_fridgePwd = @short_fridgeNewPwd = "12345"
		@new_fridgeNewPwd = "4008111666"
		@device_name = '成都CHiQ_1U_BM09'
		# @device_sn = "FRTEST400911700407014921" #QCA4004_WiFI
		# @device_sn = "FRTEST400911700407014000" #CHiQ_1U_BM30
		@device_sn = "CDTEST400911700407014001" #CHiQ_1U_BM09		
	end
	after(:all) do
		# @driver_quit
	end

	context 'after user login as AP mode' do
		before :all do
			@username_textfiled = find_element(:id, 'com.iceboxcontrol:id/login_username')
			@password_textfiled = find_element(:id, 'com.iceboxcontrol:id/login_password')
			@login_button = find_element(:id, 'com.iceboxcontrol:id/login_btn')
			@autoLogin_button = find_element(:id, 'com.iceboxcontrol:id/auto_login')
			@rememberPassword_button = find_element(:id, 'com.iceboxcontrol:id/remember_psw')
			@forgotPassword_textview = find_element(:id, 'com.iceboxcontrol:id/forgot_psw')
			@registerId_textview = find_element(:id, 'com.iceboxcontrol:id/register_id')
			@mode_textview = find_element(:id, 'android:id/text1')
		end

		context 'login_page' do
			after :each do
				sleep 3
			end

			it 'AP_mode can login with empty username and empty password' do
				begin
					login()
					sleep 5
					expect(@login_button.displayed?).to be true
					enter_wkzx_page()
					sleep 3
					back_click
					expect(button('确定').displayed?).to be true
					alert_click('确定')
				ensure
					start_activity app_package: 'com.iceboxcontrol', app_activity: 'com.iceboxcontrol.activitys.LoginActivity'
				end
			end
			it 'AP_mode can login with empty username and no-empty password' do
				begin
					login(nil,@old_password)
					sleep 5
					expect(@login_button.displayed?).to be true
					enter_wkzx_page()
					sleep 3
					back_click
					expect(button('确定').displayed?).to be true
					alert_click('确定')
				ensure
					start_activity app_package: 'com.iceboxcontrol', app_activity: 'com.iceboxcontrol.activitys.LoginActivity'
				end
			end
			it 'AP_mode can login with no-empty username and empty password' do
				begin
					login(@username,nil)
					sleep 5
					expect(@login_button.displayed?).to be true
					enter_wkzx_page()
					sleep 3
					back_click
					expect(button('确定').displayed?).to be true
					alert_click('确定')
				ensure
					start_activity app_package: 'com.iceboxcontrol', app_activity: 'com.iceboxcontrol.activitys.LoginActivity'
				end
			end
		end #login_page
	end #after user login as AP mode
end #iceboxcontrol_AP_mode
