########################################################################################################################
import os, cv2, numpy as np, numpy.linalg as npLA, pandas as pd
from shutil import rmtree
########################################################################################################################
################################################### HELPER FUNCTIONS ###################################################
########################################################################################################################
def partite_pixels(img,limit): 
    i2=img.copy(); i2=i2*((i2-(i2%limit))//limit); i1=img.copy()-i2; imshow([i1,i2]); return i1,i2; # i1=PixelValuesLessThanLimit
def shift_by_delta(img,delta): 
    i1,i2=(img.copy()+delta),(img.copy()-delta); imshow([i1,i2]); return i1,i2; # (i1+delta),(i1-delta)
def shift_channels(img): 
    i1=img.copy(); i1[:,:,0],i1[:,:,1],i1[:,:,2] = img[:,:,1],img[:,:,2],img[:,:,0]; 
    i2=img.copy(); i2[:,:,0],i2[:,:,1],i2[:,:,2] = img[:,:,2],img[:,:,0],img[:,:,1]; imshow([i1,i2]); return i1,i2; 
########################################################################################################################
def get_extension(s): # -> dot_ext
    flag=0; l=len(s); dot_ext=None; 
    for i in range(l-1,-1,-1):
        if(s[i]=="."): dot_ext = s[i:]; flag=1; break; 
    if(flag==0): print(f"Extension not found for : -->> {s} <<-- ."); raise; 
    else: return dot_ext; 
def get_path_parts(s): # -> (folder_path, img_name, dot_ext)
    end = len(s); i = end-1; 
    while(i>0 and s[i]!="."): i-=1; 
    dot_ext = s[i:end]; end=i; 
    while(i>0 and s[i]!="\\"): i-=1; 
    img_name = s[i+1:end]; folder_path = s[:i]; 
    return folder_path, img_name, dot_ext; 
def shp(img): # -> (img.shape)
    print(img.shape); return (img.shape); 
def imshow(img,*args):
    if(len(args)==0): title="image"; 
    else: title=args[0]; 
    if(type(img)==list): 
        for i in img: cv2.imshow(title,i); cv2.waitKey(0); cv2.destroyAllWindows(); 
    else: cv2.imshow(title,img); cv2.waitKey(0); cv2.destroyAllWindows(); 
def show_Channels(img):
        i1 = img.copy(); i1[:,:,0]=i1[:,:,2]; i1[:,:,1]=i1[:,:,2]; imshow(i1,"Channel R"); 
        i1 = img.copy(); i1[:,:,0]=i1[:,:,1]; i1[:,:,2]=i1[:,:,1]; imshow(i1,"Channel G"); 
        i1 = img.copy(); i1[:,:,1]=i1[:,:,0]; i1[:,:,2]=i1[:,:,0]; imshow(i1,"Channel B"); 
def printim(img):
    if(img[0].flatten()==img[1].flatten() and img[0].flatten()==img[2].flatten() ):
        print(f"{np.transpose(img.copy(),(2,0,1))[0]}  Identicle ."); 
        # print(f"{np.transpose(img.copy(),(2,0,1))[0].flatten()}  Identicle ."); 
    else:
        for i in range(3): print(np.transpose(img.copy(),(2,0,1))[i].flatten()); print(); 

########################################################################################################################
############################################### NEW OPERATOR FUNCTIONS #################################################
########################################################################################################################

def Crop_Img(pathh,coords):
    new_folder = 'Croped_Imgs_000'; new_dir = os.path.join(pathh,new_folder); 
    while(os.path.isdir(new_dir)): 
        num = str(1+int(new_folder[12:])); num = '0'*(3-len(num)) + num ; 
        new_folder = new_folder[:12] + num; new_dir = os.path.join(pathh,new_folder); 
    os.mkdir(new_dir); 
    
    x1,x2,w,y1,y2,h = coords; x2+=(x2==0)*(x1+w); y2+=(y2==0)*(y1+h); nfile = 0; 
    
    for filename in os.listdir(pathh):
        if(os.path.isfile(os.path.join(pathh,filename))):

                old_path = os.path.join(pathh, str(filename)); 
                new_path = os.path.join(new_dir, str(filename)); 

                old_img = cv2.imread(old_path); H,W,Channels = old_img.shape; 
                new_img = old_img[ max(0,y1):min(H-1,y2+1) , max(0,x1):min(W-1,x2+1) ]; 

                cv2.imwrite(new_path, new_img); 
                nfile += 1; 
    
    print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
    print(f"{nfile} number of files have been cropped and store in a new folder there."); 
    print(f"________________________________________________________________________________________"); 

########################################################################################################################

def File_Rename_1(pathh): # Format : Str1{n}Str2 
    s1 = input("Enter Str1 : "); 
    s2 = input("Enter Str2 : "); 
    st = int('0'+input("Enter starting index for 1st file : ")); 
    D = int('0'+input("How many total digits should there be in {n} ? : ")); 
    p0 = input("Should we remove preceding zeros? eg. 07 -> 7 (y/0/1/.) : "); 
    cnt=0; n=(st==0)+st; D+=(D==0)*4; print(); 

    if(p0 in ["y","Y","0","1","."]):
        for filename in os.listdir(pathh):
            if(os.path.isfile(os.path.join(pathh,filename))):
                old_name=filename; new_name = s1 + str(n) + s2; n+=1; 
                os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); cnt+=1; 
    else:
        for filename in os.listdir(pathh):
            if(os.path.isfile(os.path.join(pathh,filename))):
                old_name = filename; old_path = os.path.join(pathh,old_name); dot_ext = get_extension(filename); 
                new_name = s1 + ("0")*(D-len(str(n))) + str(n) + s2 + dot_ext; n+=1; 
                os.rename(old_path,os.path.join(pathh,new_name)); cnt+=1; 
                print(f"Renamed  >> {old_name} <<  to  >> {new_name} << ."); 
    
    print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
    print(f" {cnt} files have been formatted. "); 
    print(f"________________________________________________________________________________________"); 

def File_Rename_2(pathh): # Change N_th SubStr1 to SubStr2 
    renamed = unrenamed = 0 ; 
    last = input("Do you want to change it from the last? 0/1/y/. : "); 
    s1 = input("Enter sub-string_1 : "); l1=len(s1); 
    s2 = input("Enter sub-string_2 : "); l2=len(s2); 
    n = input("Enter N(N_th occurece)/'all' : "); print(); 

    if(n.lower()!="all"):
        if(n in ["","0"]): n=1; nn=n; 
        else: n=int(n); nn=n; 

        if(last in ["y","0","1","."]):
            for filename in os.listdir(pathh):
                if(os.path.isfile(os.path.join(pathh,filename))):
                    old_name=filename; s=old_name; l=len(filename); i=(l-l1); n=nn; 
                    while(i>=0):
                        f=0; 
                        for j in range(l1):
                            if(s[i+j]!=s1[j]): f=1; break; 
                        if(f==0): n-=1;     # f=Flag=0 means the substring matches, and hence n of Nth is reduced by 1
                        if(n==0): break; 
                        i-=1; 
                    if(n>0): print(f"No modifications done for the file : -->> {filename} <<-- , as {nn}_th is larger to have a substring :  -> {s1} <-  from last."); unrenamed+=1; 
                    else:
                        new_name = old_name[:i] + s2 + old_name[i+l1:] ; 
                        os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); renamed+=1; 
        else:
            for filename in os.listdir(pathh):
                if(os.path.isfile(os.path.join(pathh,filename))):
                    old_name=filename; s=old_name; l=len(filename); i=0; n=nn; 
                    while(i<(l-l1)):
                        f=0; 
                        for j in range(l1):
                            if(s[i+j]!=s1[j]): f=1; break; 
                        if(f==0): n-=1;     # f=Flag=0 means the substring matches, and hence n of Nth is reduced by 1
                        if(n==0): break; 
                        i+=1; 
                    if(n>0): print(f"No modifications done for the file : -->> {filename} <<-- , as {nn}_th is larger to have a substring : -> {s1} <- . "); unrenamed+=1; 
                    else:
                        new_name = old_name[:i] + s2 + old_name[i+l1:] ; 
                        os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); renamed+=1; 
        
        print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
        print(f" {renamed} files have been renamed, while {unrenamed} files are as it is, not renamed.  "); 
        print(f"________________________________________________________________________________________"); 

    else:   # Replace all substrings, excepting the extension
        delta_l = (l2-l1); 
        for filename in os.listdir(pathh):
            if(os.path.isfile(os.path.join(pathh,filename))):

                dot_ext=get_extension(filename); old_name=filename; s=old_name; 
                ext_len=len(dot_ext); l=len(filename); cur_loop_lim=(l-l1-ext_len)+1; file_rename_flag=0; i=0; 
                while(i<cur_loop_lim):
                    f=0; 
                    for j in range(l1):
                        if(s[i+j]!=s1[j]): f=1; break; 
                    if(f==0): s = s[:i] + s2 + s[i+l1:]; cur_loop_lim+=delta_l; i+=delta_l; file_rename_flag=1; 
                    i+=1; 
                new_name = s; 
                
                if(file_rename_flag==0): print(f"No modifications done for the file : -->> {filename} <<-- , as it does not have a substring : -> {s1} <- . "); unrenamed+=1; 
                else: os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); renamed+=1; 
        
        print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
        print(f" {renamed} files have been renamed, while {unrenamed} files are as it is, not renamed.  "); 
        print(f"________________________________________________________________________________________"); 

def File_Rename_3(pathh): # Insert SubStr at x_th position (from front or last)
    last = input("Do you want to insert it from the last? 0/1/y/. : "); 
    sstr = input("Enter SubStr to be inserted : "); 
    x_i = int(input("Enter position (1 based indexing) at which to be inserted" + " (1=>After Extension, 5,6=>Before Extension)"*(last in ["y","0","1"]) + " : "))-1; 
    cnt = 0; 

    if(last in ["y","0","1","."]):
        for filename in os.listdir(pathh):
            if(os.path.isfile(os.path.join(pathh,filename))):
                if(x_i==0): old_name=filename; new_name=old_name+sstr; 
                else: old_name=filename; l=len(old_name); new_name=old_name[:l-x_i] + sstr + old_name[l-x_i:]; 
                os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); cnt+=1; 
    else:
        for filename in os.listdir(pathh):
            if(os.path.isfile(os.path.join(pathh,filename))):
                old_name=filename; new_name=old_name[:x_i] + sstr + old_name[x_i:]; 
                os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); cnt+=1; 
    
    print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
    print(f" {cnt} files have been renamed."); 
    print(f"________________________________________________________________________________________"); 

def File_Rename_4(pathh): # Remove SubStr from x_th position (from front or last)
    last = input("Do you want to remove it from the last? 0/1/y/. : "); 
    sstr = input("Enter SubStr to be removed : "); m=len(sstr); 
    x_i = ((last not in ["0","1","y","."])*(int(input("Enter position from which to be removed : "))))-1; 
    renamed = unrenamed = 0; print(""); 

    if(last in ["y","0","1","."]):
        for filename in os.listdir(pathh):
            if(os.path.isfile(os.path.join(pathh,filename))):
                old_name=filename; n=len(old_name); endi=n-x_i; stri=old_name[endi-m-1:endi]; 
                if(stri==sstr): 
                    new_name=old_name[:endi-m-1]+old_name[endi:]; 
                    os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); renamed+=1; 
                else: print(f"No modifications done for the file : -->> {filename} <<-- , as -> {sstr} <- not found at {x_i} index {'from the last'*(last in ['0','1','y'])} . "); unrenamed+=1; 
    else:
        for filename in os.listdir(pathh):
            if(os.path.isfile(os.path.join(pathh,filename))):
                old_name=filename; n=len(old_name); stri=old_name[x_i:x_i+m]; 
                if(stri==sstr): 
                    new_name=old_name[:x_i]+old_name[x_i+m:]; 
                    os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); renamed+=1; 
                else: print(f"No modifications done for the file : -->> {filename} <<-- , as -> {sstr} <- not found at {x_i} index {'from the last'*(last in ['0','1','y'])} . "); unrenamed+=1; 
    
    print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
    print(f" {renamed} files have been renamed, while {unrenamed} files are as it is, not renamed.  "); 
    print(f"________________________________________________________________________________________"); 

def File_Rename_5(pathh): # Change Char at position X_th to Char_dash
    x_i = int(input("Enter position index X_th (eg. Any char at 25th pos...) : "))-1; 
    chr = input("Enter Char_dash (eg. ...should be changed to # char) : "); 
    renamed = unrenamed = 0; print(); 
    
    for filename in os.listdir(pathh):
        if(os.path.isfile(os.path.join(pathh,filename))):
            old_name=filename; new_name=old_name[:x_i] + chr + old_name[x_i+1:]; 
            if(old_name[x_i]==chr): unrenamed+=1; print(f"-->> {filename} already has {chr} at {x_i} position. "); 
            else: os.rename(os.path.join(pathh,old_name),os.path.join(pathh,new_name)); renamed+=1; 
    
    print(f"\n'''''''''''''''''''''''''''''''''''''''''Done'''''''''''''''''''''''''''''''''''''''''"); 
    print(f" {renamed} files have been renamed, while {unrenamed} files already had {chr} at {x_i}th position. "); 
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

if(__name__=="__main__"):
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
            pathh = input(f"Copy-paste path of the folder here : ").strip(); print(); 
            if(1-os.path.isdir(pathh)): input("\nFolder does not exist or the path is not of a folder. Press Enter and try again. "); print(); 
            x1 = int('0'+input(f"Enter x1, must enter (i.e. starting horizontal pixel) ..... : ")); x1 = (x1-1)+(x1==0); 
            y1 = int('0'+input(f"Enter y1, must enter (i.e. starting verticle pixel) ....... : ")); y1 = (y1-1)+(y1==0); 
            w  = int('0'+input(f"Enter w, if you have it (i.e. width=w=x2-x1) .............. : ")); 
            h  = int('0'+input(f"Enter h, if you have it (i.e. height=h=y2-y1) ............. : ")); 
            x2 = int('0'+input(f"Enter x2, if you have it (i.e. ending horizontal pixel) ... : ")); x2 = (x2-1)+(x2==0); 
            y2 = int('0'+input(f"Enter y2, if you have it (i.e. ending verticle pixel) ..... : ")); y2 = (y2-1)+(y2==0); 
            Crop_Img(pathh=pathh, coords=(x1,x2,w,y1,y2,h)); 
        
        case 2:
            print(); 
            print("1. Format : Str1{n}Str2 "); 
            print("2. Change Nth/All occurence of SubStr1 to SubStr2 "); 
            print("3. Insert SubStr at X_th position "); 
            print("4. Remove SubStr at X_th position "); 
            print("5. Change Char at position X_th to Char_dash "); 
            
            choiice = int(input(f"\nEnter Your Choice Index Here : ")); 
            if(not(1<=choiice<=5)): input("Invalid choice. Press Enter and try again. "); continue; 
            pathh = input(f"Copy-paste path of the folder here : ").strip(); print(""); 
            if(1-os.path.isdir(pathh)): input("\nFolder does not exist or the path is not of a folder. Press Enter and try again. "); continue; 
            [File_Rename_1,File_Rename_2,File_Rename_3,File_Rename_4,File_Rename_5][choiice-1](pathh=pathh); 
        
        case 3:
            pathh = input(f"Copy paste path of the folder in which image is here : ").strip(); 
            if(1-os.path.isdir(pathh)): input("\nFolder does not exist or the path is not of a folder. Press Enter and try again. "); print(); 
            img_namme = input(f"Copy paste name image here along with extension : ").strip(); 
            Compress_Single_Img(folder_pathh=pathh, img_namme=img_namme, confirm_text_flag=1); 
        
        case 4:
            pathh = input(f"Copy paste path of the folder here : ").strip(); 
            if(1-os.path.isdir(pathh)): input("\nFolder does not exist or the path is not of a folder. Press Enter and try again. "); print(); 
            Compress_Imgs_in_Folder(pathh=pathh); 
        
        case 0: break; 
        case _: input("Invalid choice. Press Enter and try again. "); 

