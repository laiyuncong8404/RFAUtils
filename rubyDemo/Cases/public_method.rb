# encoding: utf-8

#手机back键
def back_click()
   press_keycode(4)
end

#login_AP
def set_AP_mode_before_login()
   if @mode_textview.text == '远程模式'
      @mode_textview.click
      modes = find_elements(:class_name, 'android.widget.CheckedTextView')
      modes[0].click #点击‘本地模式’
   elsif @mode_textview.text == '本地模式'
   end
end

#login_STA
def set_STA_mode_before_login()
   if @mode_textview.text == '本地模式'
      @mode_textview.click
      modes = find_elements(:class_name, 'android.widget.CheckedTextView')
      modes[1].click #点击‘远程模式’
   elsif @mode_textview.text == '远程模式'
   end
end

#login_page
def login(username = nil,password = nil)
   @username_textfiled.clear
   @username_textfiled.type username
   @password_textfiled.clear
   @password_textfiled.type password
   # @autoLogin_button.click
   # @rememberPassword_button.click
   @login_button.click
   sleep 2
end

def login_with_password_remember(username = nil,password = nil)
   @username_textfiled.clear
   @username_textfiled.type username
   @password_textfiled.clear
   @password_textfiled.type password
   # @autoLogin_button.click
   @rememberPassword_button.click
   # @login_button.click
   sleep 2
end

#温控中心_page
def enter_wkzx_page()
   if exists{button('确定')}==true #绑定了设备，但没有连接
      # swipe(start_x: 550, start_y: 1120, end_x: 550, end_y: 800, duration: 1000)
      # touch_action = Appium::TouchAction.new
      # element = text('成都21')
      # touch_action.press(element: element, x: 230, y: 1115).perform
      # touch_action.release().perform
      ele_index('android.widget.TextView', 2).click #第一个设备名称
      button('确定').click
      sleep 3
      @handle = find_element(:id, 'com.iceboxcontrol:id/handle')
      expect(@handle.displayed?).to be true
      sleep 3
   elsif exists{button('否')}==true #提示没有绑定设备
      button('否').click
      sleep 3
      @handle = find_element(:id, 'com.iceboxcontrol:id/handle')
      expect(@handle.displayed?).to be true
      sleep 3
   else #绑定了设备且已连接
      @handle = find_element(:id, 'com.iceboxcontrol:id/handle')
      expect(@handle.displayed?).to be true
      sleep 3
   end
end

def wkzx_uncheck_all_mode()
   # checkboxes = [@wkzx_lcs_switch, @wkzx_bws_switch, @wkzx_smart_switch, @wkzx_holiday_switch, @wkzx_leco_switch, @wkzx_foodfirst_switch, @wkzx_quickcool_switch, @wkzx_quickcold_switch]
   checkboxes = tags('android.widget.CheckBox')
   for checkbox in checkboxes[0..1]
      checkbox.click if checkbox.attribute('checked') == 'true'
         exists{button('确定')}? button('确定').click : nil
      sleep 3
   end
   for checkbox in checkboxes[2..-1]
      checkbox.click if checkbox.attribute('checked') == 'true'
      sleep 3
   end
end

def wkzx_OnProgress?()
   sleep 5
   exists{tag('android.widget.ProgressBar')}? wkzx_OnProgress?() : (sleep 5)
end


#食谱大全_page
def enter_cookbook_page()
   id('com.iceboxcontrol:id/handle').click
   text('食谱大全').click
   sleep 3
end


#食品管理_page
def enter_foodmanage_page()
   id('com.iceboxcontrol:id/handle').click
   text('食品管理').click
   sleep 2
end

def enter_foodadd_page()
   id('com.iceboxcontrol:id/foodmanage_foodadd').click
   sleep 2
end

def enter_foodadd_detail_page()
   enter_foodadd_page()
   text('蔬菜').click
   id('com.iceboxcontrol:id/foodadd_item_img').click
   sleep 1
end

def enter_foodadd_voiceinput_page()
   enter_foodadd_page()
   id('com.iceboxcontrol:id/foodadd_voiceinput').click
   sleep 1
end

def foodadd_search(foodname=nil)
   id('com.iceboxcontrol:id/foodadd_searchfood').clear
   id('com.iceboxcontrol:id/foodadd_searchfood').type foodname
   sleep 3
   id('com.iceboxcontrol:id/foodadd_search_icon').click
   sleep 2
end

def swipe_food_to_visibel()
   swipe(start_x:284,start_y:1725,end_x:284,end_y:547,duration:2000)
end

def swipe_food_categary_to_visible()
   swipe(start_x: 900, start_y: 300, end_x: 50, end_y: 300, duration: 4000)
end

def add_food()
   id('com.iceboxcontrol:id/foodadd_detail_foodnum').clear
   id('com.iceboxcontrol:id/foodadd_detail_foodnum').type rand(1..9999)
   sleep 1
   id('com.iceboxcontrol:id/foodadd_confirm').click
   sleep 1
   button('确定').click
end

def back_from_foodadd_page_to_foodmanage_page()
   if exists{text('食品添加')} == true and text('食品添加').displayed? == true
      id('com.iceboxcontrol:id/foodadd_back').click
      sleep 1
   else exists{button('确定')} == true and button('确定').displayed? == true
      button('取消').click
      id('com.iceboxcontrol:id/foodadd_back').click
      sleep 2
   end
end

def back_from_foodadd_detail_page_to_foodmanage_page()
   id('com.iceboxcontrol:id/foodadd_detail_back').click; sleep 1
   back_from_foodadd_page_to_foodmanage_page()
end

def back_from_foodedit_detail_page_to_foodmanage_page()
   if exists{text('食品管理')} == true and text('食品管理').displayed? == true
   elsif exists{text('食品详情')} == true and text('食品详情').displayed? == true
      id('com.iceboxcontrol:id/foodmanage_back').click
   else exists{button('确定')} == true and button('确定').displayed? == true
      button('取消').click
      id('com.iceboxcontrol:id/foodmanage_back').click
   end
end


#提醒_page
def enter_reminder_page()
   id('com.iceboxcontrol:id/handle').click
   text('提醒').click
   sleep 3
end


#设置_page
def enter_setting_page()
   id('com.iceboxcontrol:id/handle').click
   text('设置').click
   sleep 3
end

#userinfo_page
def enter_userinfo_page()
   @userinfo_textview_text.click #进入个人信息页面
   sleep 3
end

def clear_nickname()
   @userinfo_nickname_textfiled.click
   length = (@userinfo_nickname_textfiled.text).length
   length.times do
      press_keycode(22) #Directional Pad Right key. May also be synthesized from trackball motions
   end
   length.times do
      press_keycode(67)#Backspace key. Deletes characters before the insertion point
   end
end

def set_nickname(nickname = nil)
   @userinfo_nickname_textfiled.type nickname
   hide_keyboard
end

#userinfo_password page
def change_user_password(oldpwd=nil,newpwd=nil,newpwdRepeat=nil)
   @userinfo_oldpwd_textfiled.type oldpwd
   @userinfo_newpwd_textfiled.type newpwd
   @userinfo_newpwdRepeat_textfiled.type newpwdRepeat
   hide_keyboard #隐藏键盘
end

#fridgePwd page
def enter_fridgePwd_page()
   @identify_textview.click
   sleep 3
end

def change_fridgePwd(fridgePwd=nil,fridgeNewPwdRepeat=nil)
   @fridgeNewPwd.clear
   @fridgeNewPwd.type fridgePwd
   @fridgeNewPwdRepeat.clear
   @fridgeNewPwdRepeat.type fridgeNewPwdRepeat
   hide_keyboard #隐藏键盘
end

#net_setting page
def enter_net_setting_page()
   @net_setting_textview.click
   sleep 3
end

# def set_wifi_connect(wifi_name=nil,wifi_pwd=nil)
#    @wifi_setting_button.click
#    text(wifi_name).click
#    @wifi_pwd_input.clear
#    @wifi_pwd_input.type wifi_pwd
# end

#device_connect page
def enter_device_connect_page()
   @dev_connect_textview.click
   sleep 3
end

#device_connect_add page
def enter_device_connect_add_page()
   @device_connect_add_button.click
end
def device_connect_add(device_name=nil,device_sn=nil,fridgeNewPwd=nil)
   @device_connect_add_name.type device_name
   @device_connect_add_sn.type device_sn
   @device_connect_add_fridgePwd.type fridgeNewPwd
end
def clear_device_connect_add_info()
   @device_connect_add_name.click
   length = (@device_connect_add_name.text).length
   length.times do
      press_keycode(22) #Directional Pad Right key. May also be synthesized from trackball motions
   end
   length.times do
      press_keycode(67)#Backspace key. Deletes characters before the insertion point
   end
   @device_connect_add_sn.click
   length = (@device_connect_add_sn.text).length
   length.times do
      press_keycode(22) #Directional Pad Right key. May also be synthesized from trackball motions
   end
   length.times do
      press_keycode(67)#Backspace key. Deletes characters before the insertion point
   end
   @device_connect_add_fridgePwd.click
   length = (@device_connect_add_fridgePwd.text).length
   length.times do
      press_keycode(22) #Directional Pad Right key. May also be synthesized from trackball motions
   end
   length.times do
      press_keycode(67)#Backspace key. Deletes characters before the insertion point
   end
end

#enter_device_connect_select_page
def enter_device_connect_select_page()
   @device_connect_connect_button.click
end

#enter_jd_dev_connect_page
def enter_jd_dev_connect_page()
   @jd_dev_connect.click
   button('确定').click
end