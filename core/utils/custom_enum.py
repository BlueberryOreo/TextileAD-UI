from enum import Enum

class ModelName(Enum):
    """
    Enum for different models.
    """
    AI_VAD = "ai_vad"
    CFA = "cfa"
    CFLOW = "cflow"
    CSFLOW = "csflow"
    DFKDE = "dfkde"
    DFM = "dfm"
    DRAEM = "draem"
    DSR = "dsr"
    EFFICIENT_AD = "efficient_ad"
    FASTFLOW = "fastflow"
    FRE = "fre"
    GANOMALY = "ganomaly"
    PADIM = "padim"
    PATCHCORE = "patchcore"
    REVERSE_DISTILLATION = "reverse_distillation"
    STFPM = "stfpm"
    UFLOW = "uflow"


class DatasetName(Enum):
    """
    Enum for different datasets.
    """
    AVENUE = "avenue"
    BTECH = "btech"
    DATUMARO = "datumaro"
    FOLDER = "folder" # custom folder dataset
    KOLEKTOR = "kolektor"
    MVTEC_3D = "mvtec_3d"
    MVTECAD2 = "mvtecad2"
    MVTEC_LOCO = "mvtec_loco"
    MVTEC = "mvtec"
    REALIAD = "realiad"
    SHANGHAITECH = "shanghaitech"
    UCSD_PED = "ucsd_ped"
    VAD = "vad"
    VISA = "visa"
