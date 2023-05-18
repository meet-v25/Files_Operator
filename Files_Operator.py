import os, cv2 as cv, numpy as np
from shutil import rmtree




##################################### IN-BUILT FUNCTIONS TO HELP #####################################
def Img_show(img):
    cv.imshow('image', img); cv.waitKey(0); cv.destroyAllWindows(); 




###################################### NEW OPERATOR FUNCTIONS ########################################


def Crop_Img(pathh,coords,ext):
    new_folder = 'Croped_Imgs'; 
    x,w,y,h = coords; x1=x; x2=x1+w; y1=y; y2=y+h; 
    nfile = 0; 
    
    for filename in os.listdir(pathh):
        if(os.path.isfile(os.path.join(pathh,filename))):
            if(filename.endswith(ext)):

                old_path = os.path.join(pathh, str(filename)); 
                new_dir = os.path.join(pathh, new_folder); 
                new_path = os.path.join(new_dir, str(filename)); 
                
                if(os.path.isdir(new_dir)): rmtree(new_dir); 
                os.mkdir(new_dir); 

                old_img = cv.imread(old_path); 
                new_img = old_img[ y1:y2+1 , x1:x2+1 ]; 

                cv.imwrite(new_path, new_img); 
                nfile += 1; 
    
    print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''")
    print(f"{nfile} number of files have been cropped and store in a new folder there.")
    print(f"_______________________________________________________________________________________")






######################################## MAIN LOOPING CODE ########################################

while(1):
  try:
    print("\n"*2); 
    print("0. Exit")
    print("1. Images Crop (Path,P1,P2)"); 
    print("2. Files Rename ()"); 
    print("3. Image Copression (Path)")
    choice = int(input(f"\nEnter Your Choice Index Here : ")); print(); 
    match choice:

        case 1:
            pathh = input(f"Copy-paste path of the folder here : "); 
            ext = input(f"Enter an extension of files on which you want to operate (in small-case) : "); 
            x = int(input(f"Enter x (i.e. starting horizontal pixel) ... : ")); 
            w = int(input(f"Enter w (i.e. width=w=x2-x1) ............... : ")); 
            y = int(input(f"Enter y (i.e. starting verticle pixel) ..... : ")); 
            h = int(input(f"Enter h (i.e. height=h=y2-y1) .............. : ")); 
            Crop_Img(pathh=pathh, coords=(x,w,y,h), ext=ext); 
        
        case 2:
            input("This operation is yet to be implemented. Please try any other option(s). Press Enter to continue."); 
        
        case 3:
            input("This operation is yet to be implemented. Please try any other option(s). Press Enter to continue."); 
        
        case 0:
            break; 
        
        case _:
            input("Invalid choice. Press Enter and try again."); 

  except:
    input("\nBad Input. Some input(s) you provided are causing error. Please verify them and make sure they are processable. Press Enter to continue."); 

