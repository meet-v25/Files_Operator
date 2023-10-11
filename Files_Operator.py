import os, cv2, numpy as np, numpy.linalg as npLA
from shutil import rmtree

########################################################################################################################
################################################### HELPER FUNCTIONS ###################################################
########################################################################################################################
def imshow(img,*args): # -> null
    if(len(args)==0): title="image"; 
    else: title=args[0]; 
    if(type(img)==list): 
        for i in img: cv2.imshow(title,i); cv2.waitKey(0); cv2.destroyAllWindows(); 
    else: cv2.imshow(title,img); cv2.waitKey(0); cv2.destroyAllWindows(); 

def show_Channels(i1): # -> (R,G,B)
        i2 = i1.copy(); i2[:,:,0]=0; i2[:,:,1]=0; # Show R 
        i3 = i1.copy(); i3[:,:,0]=0; i3[:,:,2]=0; # Show G 
        i4 = i1.copy(); i4[:,:,1]=0; i4[:,:,2]=0; # Show B 
        imshow([i2,i3,i4]); 
        return i2,i3,i4; 

def shp(img): # -> (h,w,c)
    s=img.shape; print(s); return s; 

def helper_new(): pass


########################################################################################################################
############################################### NEW OPERATOR FUNCTIONS #################################################
########################################################################################################################

def Crop_Img(pathh,coords):
    new_folder = 'Croped_Imgs_000'; new_dir = os.path.join(pathh,new_folder); 
    while(os.path.isdir(new_dir)): 
        num = str(1+int(new_folder[12:])); num = '0'*(3-len(num)) + num ; 
        new_folder = new_folder[:12] + num; new_dir = os.path.join(pathh,new_folder); 
    os.mkdir(new_dir); 
    
    x,w,y,h = coords; x1=x; x2=x1+w; y1=y; y2=y+h; nfile = 0; 
    
    for filename in os.listdir(pathh):
        if(os.path.isfile(os.path.join(pathh,filename))):

                old_path = os.path.join(pathh, str(filename)); 
                new_path = os.path.join(new_dir, str(filename)); 

                old_img = cv2.imread(old_path); 
                new_img = old_img[ y1:y2+1 , x1:x2+1 ]; 

                cv2.imwrite(new_path, new_img); 
                nfile += 1; 
    
    print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
    print(f"{nfile} number of files have been cropped and store in a new folder there."); 
    print(f"________________________________________________________________________________________"); 

########################################################################################################################

def Compress_Single_Img(folder_pathh,img_namme,confirm_text_flag):
    
    pathh = os.path.join(folder_pathh,img_namme); ext = pathh[pathh.index("."):]; 
    img_name_wo_ext = img_namme[:img_namme.index(".")]; new_dir = os.path.join(folder_pathh, img_name_wo_ext); 
    if(os.path.isdir(new_dir)): rmtree(new_dir); 
    os.mkdir(new_dir); 

    old_img = cv2.imread(pathh); shp = old_img.shape; Us=[None,None,None]; Ss=[None,None,None]; Vs=[None,None,None]; 
    for i in range(3): U,S,V = npLA.svd(old_img[:,:,i], full_matrices=False); Us[i]=U; Ss[i]=S; Vs[i]=V; 
    
    for k in range(1, min(shp[0],shp[1])):

        new_img = np.zeros(shape=shp); 
        for i in range(3): new_img[:,:,i] = Us[i][:,:k] @ (np.diag(Ss[i][:k]) @ (Vs[i][:k,:])); 
        
        new_img = new_img.astype('uint8'); 
        new_path = os.path.join(new_dir, img_name_wo_ext + ('_'+('0'*(5-len(str(k))))+str(k)) + ext ); 
        cv2.imwrite(new_path,new_img); 

    if(confirm_text_flag):
        print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
        print(f"Multiple compressed images are saved there, in a folder with the image's name."); 
        print(f"________________________________________________________________________________________"); 

def Compress_Imgs_in_Folder(pathh):
    for filename in os.listdir(pathh):
        if(os.path.isfile(os.path.join(pathh,filename))):
            if (1-( filename.endswith("jfif") or filename.endswith("jfif") )):
                Compress_Single_Img(folder_pathh=pathh, img_namme=filename, confirm_text_flag=0); 
    
    print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
    print(f"Folders with multiple compressed images are saved there."); 
    print(f"________________________________________________________________________________________"); 

########################################################################################################################

def new_fn():pass


########################################################################################################################






########################################################################################################################
################################################## MAIN LOOPING CODE ###################################################
########################################################################################################################

while(1):
    
    if(1):
        print("\n"*2); 
        print("0. Exit"); 
        print("1. Images Crop (Path,P1,P2)"); 
        print("2. Files Rename (Path,Choose)"); 
        print("3. Compress a single image (Path)"); 
        print("4. Compress multiple images (Path)"); 
    choice = int(input(f"\nEnter Your Choice Index Here : ")); print(); 
    match choice:

        case 1:
            pathh = input(f"Copy-paste path of the folder here : ").strip(); 
            x1 = int('0'+input(f"Enter x1, must enter (i.e. starting horizontal pixel) ..... : ")); 
            x2 = int('0'+input(f"Enter x2, if you have it (i.e. ending horizontal pixel) ... : ")); 
            w  = int('0'+input(f"Enter w, if you have it (i.e. width=w=x2-x1) .............. : ")); 
            y1 = int('0'+input(f"Enter y1, must enter (i.e. starting verticle pixel) ....... : ")); 
            y2 = int('0'+input(f"Enter y2, if you have it (i.e. starting verticle pixel) ... : ")); 
            h  = int('0'+input(f"Enter h, if you have it (i.e. height=h=y2-y1) ............. : ")); 
            w += (w==0)*(x2-x1); h += (h==0)*(y2-y1); 
            Crop_Img(pathh=pathh, coords=(x1,w,y1,h)); 
        
        case 2:
            input("This operation is yet to be implemented. Please try any other option(s). Press Enter to continue."); 
        
        case 3:
            folder_pathh = input(f"Copy paste path of the folder in which image is here : ").strip(); 
            img_namme = input(f"Copy paste name image here along with extension : ").strip(); 
            Compress_Single_Img(folder_pathh=folder_pathh, img_namme=img_namme, confirm_text_flag=1); 
        
        case 4:
            pathh = input(f"Copy paste path of the folder here : ").strip(); 
            Compress_Imgs_in_Folder(pathh=pathh); 
        
        case 0: break; 
        case _: input("Invalid choice. Press Enter and try again."); 
