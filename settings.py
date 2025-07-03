
## IMPORTING LIBRARIES REQUIRED 
import os
from dotenv import load_dotenv
import numpy as np
import platform
import requests


## LOADING ENVIRONMENT VARIABLES
load_dotenv()


## download the models -- 
## vegetation , furniture , pavement 
# def download_models():
    



## COMMON FOLDER AND VARIABLES 
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
API_BASE_URL = "https://ndd.roadathena.com"



####ANCHOR -  PVEMENT SETTINGS 

###!SECTION PAVEMENT VARIABLES 
PAVEMENT_BASE = "pavement"   
# -------------------------------------------------------------------GPX settings
GPX_FORMAT =  os.path.join(BASE_DIR,'gpxSettings/gpx.fmt')
GPX_DIR =  os.path.join(BASE_DIR, PAVEMENT_BASE , 'gpx')
GPX_FORMAT = os.path.join(BASE_DIR, PAVEMENT_BASE , 'gpxSettings/gpx.fmt')
# ------------------------------------------------------------------ Input videos folder
VIDEO_DIR = os.path.join(BASE_DIR, PAVEMENT_BASE , 'videos')
# ------------------------------------------------------------------ Utils
EXIFTOOL_PATH = "D:\pothole_n_hero\PotholeDetection\pothole_image_data\\video-meta\exiftool.exe"
# ------------------------------------------------------------------ Model related settings 
CONFIDENCE_THRESHOLD = 0.2 
NMS_THRESHOLD = 0.4

# CLASSES_FILE = os.path.join(BASE_DIR,PAVEMENT_BASE , 'modelData','best_pavement_v2_seg_FR_classes.txt').replace('\\','/')
CLASSES_FILE = os.path.join(BASE_DIR,PAVEMENT_BASE , 'modelClasses', 'best_pavement_v2_seg_FR_classes.txt').replace('\\','/')
# MODEL_NAME = 'best_pavement_v2_seg_FR.pt'
MODEL_NAME = 'best_pavement_v2_seg_FR.pt'
# CLASSES_FILE = os.path.join(BASE_DIR,'modelData','classes_DelhiAirforce.txt')
# MODEL_NAME = 'bestseg_delhiAirforce_small2segments.pt'

os.makedirs(os.path.join(BASE_DIR , "bin") , exist_ok= True  )
MODEL_WEIGHTS = os.path.join(BASE_DIR,  PAVEMENT_BASE , 'modelData',MODEL_NAME).replace('\\','/')
MODEL_CFG = os.path.join(BASE_DIR, PAVEMENT_BASE , 'modelData','yolov4-custom-LK.cfg')
POTHOLEID = 3
CRACKSIDS = [1, 5]
WEBCRACKID=1


# CLASSES_TO_DETECT = [1,2,3,4,5]


CLASSES_TO_DETECT = [1,2,3,5]
# {0: 'Road', 1: 'Pothole', 2: 'Raveling', 3: 'Paverblock', 4: 'Mud', 5: 'Crack/L-H', 6: 'Garbage', 7: 'Manhole', 8: 'Patch'}
## DELHI AIRFORCE COLORS NEW 
COLORS = [ (0 , 0 , 0 ) ,   (0, 0, 255) , (73,50,188) , (255 , 0 , 0 ), (0 , 255, 0 ),  (255, 255, 0)  , (0 , 255, 0 ), (0 , 255, 0 ),  (0, 255,255)]

"""
# CLASSES_TO_DETECT = [1,2,3,4,5]
CLASSES_TO_DETECT = [1,2,3,5,8]

# ----------------------------------------------------------------- Anomalies settings
COLORS = [(0, 0, 0), (160, 160, 0), (0, 255,255),(0, 0, 255),(73,50,188),(255, 255, 0), (100, 100, 0) ] # colours chandigarh model


## DELHI AIRFORCE COLORS NEW 
COLORS = [ (0, 0, 255) , (73,50,188) , (255 , 0 , 0 ),  (255, 255, 0)  , (0, 255,255)]
"""



class_names=[]
# with open(CLASSES_FILE, "r") as f:
#     class_names = [cname.strip() for cname in f.readlines()]
for (i,cls) in enumerate(class_names):
    if cls.lower() == 'pothole':
        POTHOLEID=i
# ----------------------------------------------------------------- Anomalies settings
# COLORS = [(0, 0, 0), (160, 160, 0), (0, 255,255),(0, 0, 255),(73,50,188),(255, 255, 0), (100, 100, 0) ] # colours chandigarh model
# COLORS = [(0, 0, 255), (0, 255,255),(255, 255, 0), (100, 100, 0), (73,50,188)] # colours chandigarh model
ROI= np.array([[0, 315],
            [0, 1080], [1920, 1080], [1800, 315]],
    np.int32)

USE_ROI=False
SHOW_ROI=False
SHARPEN_IMAGE=False
BRIGHTEN_IMAGE=False
DISPLAY_VIDEO = True
DRAW_EXTRACTED_ROAD=False
USE_EXTRACTED_ROAD =False

###!SECTION MODEL-UTILS
# ----------------------------------------------------------------- Excel report settings
ROADATHENA_LOGO_PATH = f'{BASE_DIR}/{PAVEMENT_BASE}/utilMedia/RA-logo-1.png'
HANUAI_LOGO_PATH = f'{BASE_DIR}/{PAVEMENT_BASE}/utilMedia/HanuAI.png'
DEFAULT_DATA_ROW_HEIGHT = 30



###!SECTION --------------- AWS CODE SETTINGS 
# --------------------------------------------------------------- AWS S3 settings.
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = os.environ.get('AWS_DEFAULT_ACL')
AWS_S3_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
S3_VIDEOS_DOWNLOAD_PATH = f"{BASE_DIR}/{PAVEMENT_BASE}/videos"



###!SECTION FFMPEG SETTINGS 
# ----------------------------------------------------------------- FFMPEG settings
FFMPEG_DOWNLOAD_URL_LINUX = "https://radashboard.s3.ap-south-1.amazonaws.com/ModelsNBinFiles/ffmpeg/ffmpeg"
FFMPEG_DOWNLOAD_URL_WINDOWS = "https://radashboard.s3.ap-south-1.amazonaws.com/ModelsNBinFiles/ffmpeg/ffmpeg.exe"


EXIFTOOL_DOWNLOAD_URL_LINUX = "https://raiotransection.s3.ap-south-1.amazonaws.com/ModelsNBinFiles/exiftool/exiftool"
EXIFTOOL_DOWNLOAD_URL_WINDOWS = "https://raiotransection.s3.ap-south-1.amazonaws.com/ModelsNBinFiles/exiftool/exiftool.exe"



def downloadFFMPEG(url):
    resp = requests.get(url)
    if not os.path.exists(os.path.join(BASE_DIR, 'bin')):
        os.mkdir(os.path.join(BASE_DIR, 'bin'))
    fileName = url.split("/")[-1]
    with open(os.path.join(BASE_DIR, "bin",fileName).replace("\\", "/"), 'wb') as myfile:
        myfile.write(resp.content)
        
def downloadEXIFTOOL(url):
    resp = requests.get(url)
    if not os.path.exists(os.path.join(BASE_DIR, 'bin')):
        os.mkdir(os.path.join(BASE_DIR, 'bin'))
    fileName = url.split("/")[-1]
    with open(os.path.join(BASE_DIR, "bin",fileName).replace("\\", "/"), 'wb') as myfile:
        myfile.write(resp.content)


##!SECTION SYSTEM SPECIFIC SETTINGS 
systemName = platform.system()
systemName = systemName.lower()

if systemName=='linux':
    
    ## DOWNLOAD THE FFMPED AND EXIFTOOL IF NOT PRESENT IN THE SYSTEM 
    FFMPEG_PATH = os.path.join(BASE_DIR,  'bin','ffmpeg')
    if not os.path.exists(FFMPEG_PATH):
        downloadFFMPEG(FFMPEG_DOWNLOAD_URL_LINUX)
        os.chmod(FFMPEG_PATH, 0o755)
        
    EXIFTOOL_PATH = os.path.join(BASE_DIR,  'bin','exiftool')
    if not os.path.exists(EXIFTOOL_PATH):
        downloadFFMPEG(EXIFTOOL_DOWNLOAD_URL_LINUX)
        os.chmod(EXIFTOOL_PATH, 0o755)
    
        
    ## EXIFTOOL INSTALL 
    
elif systemName=='windows':
    FFMPEG_PATH = os.path.join(BASE_DIR,'bin','ffmpeg.exe')
    if not os.path.exists(FFMPEG_PATH):
        downloadFFMPEG(FFMPEG_DOWNLOAD_URL_WINDOWS)
        
    EXIFTOOL_PATH = os.path.join(BASE_DIR,  'bin','exiftool.exe')
    if not os.path.exists(EXIFTOOL_PATH):
        downloadFFMPEG(EXIFTOOL_DOWNLOAD_URL_WINDOWS)
        # os.chmod(EXIFTOOL_PATH, 0o755)
        
else:
    
    FFMPEG_PATH = None
    EXIFTOOL_PATH = None 

# --------------------------------------------------------------------------------



###!SECTION FURNITURE AND VEGETATION MODELS SETTINGS 

## Important variables 
VEGETATION_BASE = "vegetation"
FURNITURE_BASE = "furniture"

## Model selection 
VEGE_MODEL = "v-8.6.pt"
FUR_MODEL = "best_26.pt"

## Model paths
VEGETATION_MODEL_NAME = f"{BASE_DIR}/{VEGETATION_BASE}/model/{VEGE_MODEL}" 
FURNITURE_MODEL_NAME = f"{BASE_DIR}/{FURNITURE_BASE}/model/{FUR_MODEL}"
AWS_BUCKET_PATH = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"


FURNITURE_CLASSES = ["CHEVRON","PROHIBITORY_MANDATORY_SIGNS,CAUTIONARY_WARNING_SIGNS","HAZARD","INFORMATORY_SIGNS"]
VEGETATION_CLASSES = ["Vegetation" , "Pole" , "Tree" , "gap in vegetation" ]


##!SECTION NAV BAR ASSETS 
## set the screen display of processing on or off 
SHOW_SCREEN = False
left_image_path, right_image_path, title_text = "images/HanuAI.png", "images/RA-logo-1.png", "Process Road Models "




###!SECTION VEGETATION EXTRAS SETTINGS -- HANDLE MODEL FROM HERE 
CHAINAGE_WISE_REPORT = True  # default true 
CREATE_NEW_JSONS = True  # default true 
PROCESS_VIDEOS = True    # default true 
UPLOAD_TO_S3 = True    # default true 

## COLORS FILE OF VEGETATION 
VEGETATION_CLASSES_COLORS = class_colors = {
        "Encroachment": (0, 165, 255),  # light blue
        "Vegetation": (255, 0, 255),  # yellow
        "Tree": (128, 0, 128),  # light blue
        "gap in vegetation": (0, 255, 255),  # dark blue
        "Pole": (80, 127, 255),
        "Bus Stop": (224 , 190 , 21) # light blue ,
    }


## SPACE INFO 
SPACE_INFO = True