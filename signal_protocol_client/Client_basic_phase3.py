from math import ceil, log2
import time
import random
import sympy
import warnings
from random import randint, seed
import sys
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256, HMAC, SHA256
import requests
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import random
import re
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass

#+-----+++++-------++++++++-------+++++-----+#
#|  CS 411 Term Project Fall 23-24 Phase 3  |#
#|    Ahmet Emre Eser & Batuhan Soydeger    |#
#+-----+++++-------++++++++-------+++++-----+#

API_URL = 'http://harpoon1.sabanciuniv.edu:9999/'

stuID  = 31273 # Enter your student ID
stuIDB = 18007

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

def Setup():
    E = Curve.get_curve('secp256k1')
    return E

def KeyGen(E):
    n = E.order
    P = E.generator
    sA = randint(1,n-1)
    QA = sA*P
    return sA, QA

def SignGen(message, E, sA):
    n = E.order
    P = E.generator
    k = randint(1, n-2)
    R = k*P
    r = R.x % n
    h = int.from_bytes(SHA3_256.new(r.to_bytes((r.bit_length()+7)//8, byteorder='big')+message).digest(), byteorder='big')%n
    s = (k - sA*h) % n
    return h, s

def SignVer(message, h, s, E, QA):
    n = E.order
    P = E.generator
    V = s*P + h*QA
    v = V.x % n
    h_ = int.from_bytes(SHA3_256.new(v.to_bytes((v.bit_length()+7)//8, byteorder='big')+message).digest(), byteorder='big')%n
    if h_ == h:
        return True
    else:
        return False

curve : Curve = Setup()

#server's Identitiy public key
IKey_Ser = Point(13235124847535533099468356850397783155412919701096209585248805345836420638441, 93192522080143207888898588123297137412359674872998361245305696362578896786687, curve)


def IKRegReq(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'IKPUB.X': x, 'IKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegReq"), json = mes)		
    print(response.json())

def IKRegVerify(code):
    mes = {'ID':stuID, 'CODE': code}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegVerif"), json = mes)
    if((response.ok) == False): raise Exception(response.json())
    print(response.json())

def SPKReg(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'SPKPUB.X': x, 'SPKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SPKReg"), json = mes)		
    print(response.json())

def OTKReg(keyID,x,y,hmac):
    mes = {'ID':stuID, 'KEYID': keyID, 'OTKI.X': x, 'OTKI.Y': y, 'HMACI': hmac}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "OTKReg"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetIK(rcode):
    mes = {'ID':stuID, 'RCODE': rcode}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetIK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetSPK(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetSPK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetOTK(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetOTK"), json = mes)		
    print(response.json())

############## The new functions of phase 2 ###############

#Pseudo-client will send you 5 messages to your inbox via server when you call this function
def PseudoSendMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "PseudoSendMsg"), json = mes)		
    print(response.json())
    return response

#Get your messages. server will send 1 message from your inbox
def ReqMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "ReqMsg"), json = mes)	
    print(response.json())	
    if((response.ok) == True): 
        res = response.json()
        return res["IDB"], res["OTKID"], res["MSGID"], res["MSG"], res["IK.X"], res["IK.Y"], res["EK.X"], res["EK.Y"]
    else:
        return (-1,0,0,0,0,0,0,0)

#Get the list of the deleted messages' ids.
def ReqDelMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "ReqDelMsgs"), json = mes)      
    print(response.json())      
    if((response.ok) == True): 
        res = response.json()
        return res["MSGID"]

#If you decrypted the message, send back the plaintext for checking
def Checker(stuID, stuIDB, msgID, decmsg):
    mes = {'IDA':stuID, 'IDB':stuIDB, 'MSGID': msgID, 'DECMSG': decmsg}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "Checker"), json = mes)		
    print(response.json())


############## The new functions of phase 3 ###############

#Pseudo-client will send you 5 messages to your inbox via server when you call this function
def PseudoSendMsgPH3(h,s):
    mes = {'ID': stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "PseudoSendMsgPH3"), json=mes)
    print(response.json())

# Send a message to client idB
def SendMsg(idA, idB, otkID, msgid, msg, ikx, iky, ekx, eky):
    mes = {"IDA": idA, "IDB": idB, "OTKID": int(otkID), "MSGID": msgid, "MSG": msg, "IK.X": ikx, "IK.Y": iky, "EK.X": ekx, "EK.Y": eky}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SendMSG"), json=mes)
    print(response.json())    


# Receive KeyBundle of the client stuIDB
def reqKeyBundle(stuID, stuIDB, h, s):
    key_bundle_msg = {'IDA': stuID, 'IDB':stuIDB, 'S': s, 'H': h}
    print("Requesting party B's Key Bundle ...")
    response = requests.get('{}/{}'.format(API_URL, "ReqKeyBundle"), json=key_bundle_msg)
    print(response.json()) 
    if((response.ok) == True):
        print(response.json()) 
        res = response.json()
        return res['KEYID'], res['IK.X'], res['IK.Y'], res['SPK.X'], res['SPK.Y'], res['SPK.H'], res['SPK.s'], res['OTK.X'], res['OTK.Y']
        
    else:
        return -1, 0, 0, 0, 0, 0, 0, 0, 0


#Status control. Returns #of messages and remained OTKs
def Status(stuID: int, h: int, s: int) -> Tuple[int, int, int]:
    mes = {'ID': stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "Status"), json=mes)
    print(response.json())
    if (response.ok == True):
        res = response.json()
        return res['numMSG'], res['numOTK'], res['StatusMSG']

############## The new functions of BONUS ###############

# Exchange partial keys with users 2 and 4
def ExchangePartialKeys(stuID, z1x, z1y, h, s):
    request_msg = {'ID': stuID, 'z1.x': z1x, 'z1.y': z1y, 'H': h, 'S': s}
    print("Sending your PK (z) and receiving others ...")
    response = requests.get('{}/{}'.format(API_URL, "ExchangePartialKeys"), json=request_msg)
    if ((response.ok) == True):
        print(response.json())
        res = response.json()
        return res['z2.x'], res['z2.y'], res['z4.x'], res['z4.y']
    else:
        print(response.json())
        return 0, 0, 0, 0


# Exchange partial keys with user 3
def ExchangeXs(stuID, x1x, x1y, h, s):
    request_msg = {'ID': stuID, 'x1.x': x1x, 'x1.y': x1y, 'H': h, 'S': s}
    print("Sending your x and receiving others ...")
    response = requests.get('{}/{}'.format(API_URL, "ExchangeXs"), json=request_msg)
    if ((response.ok) == True):
        print(response.json())
        res = response.json()
        return res['x2.x'], res['x2.y'], res['x3.x'], res['x3.y'], res['x4.x'], res['x4.y']
    else:
        print(response.json())
        return 0, 0, 0, 0, 0, 0

# Check if your conference key is correct
def BonusChecker(stuID, Kx, Ky):
    mes = {'ID': stuID, 'K.x': Kx, 'K.y': Ky}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "BonusChecker"), json=mes)
    print(response.json())



#### UTILITY FUNCTIONS #### - from phase 1 
def int_to_bytearray(a : int) -> bytearray:
    from math import ceil
    return bytearray(a.to_bytes(length = ceil(a.bit_length()/8), byteorder='big'))

def bytearray_to_int(a: bytearray) -> int:
    int.from_bytes(a, byteorder='big')

def announce(num : int, title : str) -> None:
    print(title+":", end=' ')
    print(num)

@dataclass
class Curve_Params:
    E = Curve.get_curve('secp256k1')
    n = E.order
    p = E.field
    P = E.generator
    a = E.a
    b = E.b
    # aliases so that we don't forget what these letters mean : )
    G = P
    generator = P
    prime = P
    order = n
    curve = E

#### UTILITY FUNCTIONS #### - from phase 2
def pt_to_int_tuple(a : Point) -> Tuple[int, int]:
    return (a.x, a.y)
def decompose_pt_bytes(a : Point) -> Tuple[bytearray, bytearray]:
    byte_tuple =  int_to_bytearray(a.x),  int_to_bytearray(a.y)
    return byte_tuple
def concat_x_y_tuple(a : Tuple[bytearray, bytearray]) -> bytearray:
    return a[0] + a[1]
def concat_x_y_pt(a : Point) -> bytearray:
    return (decompose_pt_bytes(a))[0] + (decompose_pt_bytes(a))[1]


#### SIGNATURE GENERATION - VERIFICATION FUNCTIONS #### - from phase 1
# @return (h, s) where h is the hash value of msg and s is the signature
# @param sa : priv/secret key of the signer
def gen_sig(msg: str | int | bytes | bytearray, sa: int) -> Tuple[int, int]:
    if (isinstance(msg, str)):
        m_bytes = bytearray(msg, encoding="utf-8")
    elif (isinstance(msg, int)):
        m_bytes = bytearray(msg.to_bytes(length=ceil((msg.bit_length())/8), byteorder='big'))# bytearray(hex(msg), encoding='utf-8')
    elif (isinstance(msg, bytes) or isinstance(msg, bytearray)):
        m_bytes = msg

    k = randint(1, Curve_Params.order)
    R : Point = Curve_Params.curve.mul_point(k, Curve_Params.generator)
    Rx = R.x % Curve_Params.order
    r_bytes = bytearray(Rx.to_bytes(length = ceil(Rx.bit_length() / 8),byteorder = 'big'))

    H = SHA3_256.new(r_bytes + m_bytes)
    h : int = int.from_bytes(H.digest(), byteorder='big') % Curve_Params.order

    s : int = (k - (sa * h)) % Curve_Params.order
    return (h, s)

# @param sig = (h, s) where h is the hash value of msg and s is the signature
# @param Qa : public key of the signer
def verif_sig(msg: str | int | bytes | bytearray, sig: Tuple[int, int], Qa : Point) -> bool:
    s        : int = sig[1]
    h_actual : int = sig[0] # h received in signature

    sG  : Point = Curve_Params.curve.mul_point(s, Curve_Params.generator)
    hQa : Point = Curve_Params.curve.mul_point(h_actual, Qa)
    V   : Point = Curve_Params.curve.add_point(sG, hQa)
    Vx  : int = V.x

    v_bytes = bytearray(Vx.to_bytes(length=ceil(Vx.bit_length() / 8), byteorder = 'big'))
    
    if (isinstance(msg, str)):
        m_bytes = bytearray(msg, encoding="utf-8")
    elif (isinstance(msg, int)):
        m_bytes = bytearray(msg.to_bytes(length=ceil((msg.bit_length())/8), byteorder='big'))
    elif (isinstance(msg, bytes) or isinstance(msg, bytearray)):
        m_bytes = msg

    Hash_func = (SHA3_256.new(v_bytes + m_bytes))
    h_computed  : int = int.from_bytes(Hash_func.digest(), byteorder='big') % Curve_Params.order
    return (h_computed == h_actual)

#### REGISTRATION FUNCTIONS #### -- from phase 1
def genIK(seed_arg : int | None) -> Tuple[int, Point] | Tuple[None, None]:
    if (seed_arg is not None):
        random.seed(seed_arg)

    IKey_Pr  : int = random.randint(1, Curve_Params.n - 2) # randint includes both endpoints
    IKey_Pub : Point = Curve_Params.curve.mul_point(IKey_Pr, Curve_Params.P)       # overloaded multiplication operator
    pub_key_on_curve: bool = Curve_Params.curve.is_on_curve(IKey_Pub)
    
    try:
        assert(pub_key_on_curve)
    except:
        print("publik key is not on curve, returning None tuple")
        return (None, None)
    
    return (IKey_Pr, IKey_Pub)

# returns (H, S) of signature of stuID
def register_ik(stuID : int, ik_priv : int, ik_pub : Point ) -> Tuple[int, int] | None:
    reg_id_signature : Tuple[int, int] = gen_sig(stuID, ik_priv)
    verif_result : bool = verif_sig(stuID, reg_id_signature, ik_pub)
    try:
        assert(verif_result)
    except:
        print("signature of student id not valid, returning None")
        return None

    H : int = reg_id_signature[0]
    S : int = reg_id_signature[1]

    IKPUBX : int = ik_pub.x
    IKPUBY : int = ik_pub.y

    print("Sending signature and my IKEY to server via IKRegReq() function in json format")
    IKRegReq(H, S, IKPUBX, IKPUBY)
    print("Received the verification code through email")
    return (H, S)

def registration_verif(reg_req_code_arg : int) -> None:
    reg_req_code = reg_req_code_arg
    print("Sending the verification code to server via IKRegVerify() function in json format")
    IKRegVerify(reg_req_code)

def gen_SPK(seed_arg : int) -> Tuple[int, Point]:
    global register_user
    random.seed(seed_arg)
    SPKey_Pr  : int   = random.randint(1, Curve_Params.order - 2)
    SPKey_Pub : Point = Curve_Params.curve.mul_point(SPKey_Pr, Curve_Params.generator)
    if register_user:
        print("Generating SPK...")
        print(f"Private SPK:")
        print(SPKey_Pr)
        print("Public SPK.x:")
        print(SPKey_Pub.x)
        print("Public SPK.y:")
        print(SPKey_Pub.y)
    return SPKey_Pr, SPKey_Pub

def register_SPK(SPKey_Pr : int, SPKey_Pub : Point, ik_priv : int) -> Tuple[int, int]:
    SPKey_Pub_Bytes : bytearray = bytearray(SPKey_Pub.x.to_bytes(length = ceil(SPKey_Pub.x.bit_length() / 8), byteorder = 'big' )) + bytearray(SPKey_Pub.y.to_bytes(length = ceil(SPKey_Pub.y.bit_length() / 8), byteorder = 'big' ))

    SPKey_signature : Tuple[int, int] = gen_sig( SPKey_Pub_Bytes, ik_priv ) # IMPORTANT: MUST SIGN WITH THE IDENTITY KEY (IK)
    SPKey_sig_H = SPKey_signature[0]
    SPKey_sig_S = SPKey_signature[1]

    print("Signature of my SPK is:")
    print(f"h= {SPKey_sig_H}")
    print(f"s= {SPKey_sig_S}")
    print("Sending SPK and the signatures to the server via SPKReg() function in json format...")
    SPKReg(h=SPKey_sig_H, s=SPKey_sig_S, x=SPKey_Pub.x, y=SPKey_Pub.y) 
    return (SPKey_sig_H, SPKey_sig_S)

def gen_hmac_key(SPKey_Pr: int, server_ik : Point) -> bytearray:
    # print("Creating HMAC key (Diffie Hellman)")
    IKS = Point(server_ik.x, server_ik.y, Curve_Params.curve)
    T  = Curve_Params.curve.mul_point(SPKey_Pr, IKS)
    # print(f"T is  ({T.x} , {T.y})")
    U : bytearray = bytearray(b'TheHMACKeyToSuccess') + int_to_bytearray(T.y) + int_to_bytearray(T.x)
    # print(f"U is {bytes(U)}")
    hash_func = SHA3_256.new(U)
    K_HMAC : bytearray = bytearray(hash_func.digest())
    # print(f"HMAC Key is created {bytes(K_HMAC)}")
    return K_HMAC

def reg_otk(K_HMAC : bytearray, seed_arg : int,  register_otk = True) -> Tuple[List[Tuple[int, Point]], List[str]]:
    
    OTK_LIST : List[Tuple[int, Point]] = []
    OTK_HMACS : List[str] = []
    if (register_otk):
        print("Creating OTKs starting from index 0...")
    random.seed(13)
    for i in range(10):
        k = random.randint(1, Curve_Params.curve.order - 2)
        otk_pub_part = Curve_Params.curve.mul_point(k, Curve_Params.generator)
        OTK_LIST.append((k, otk_pub_part))
        otk_concat = int_to_bytearray(OTK_LIST[i][1].x) + int_to_bytearray(OTK_LIST[i][1].y)
        hmac = HMAC.new(K_HMAC, otk_concat, SHA256)
        hmac_otk = (hmac.hexdigest())
        if (register_otk):
            print(hmac_otk)
        OTK_HMACS.append(hmac_otk)
        if (register_otk):
            OTKReg(i, OTK_LIST[i][1].x, OTK_LIST[i][1].y, OTK_HMACS[i])
    # if otk generation is not successful an error will terminate the loop
    if (register_otk):
        print("OTK keys were generated successfully!")
    return (OTK_LIST, OTK_HMACS)


# generates ks from pre key bundle
def generate_Ks(EKX, EKY, IKX, IKY, SPK_pr, ik_priv, OTK) -> bytearray:
    ek_pub_partner : Point = Point(EKX, EKY, Curve_Params.curve)
    ik_pub_partner : Point = Point(IKX, IKY, Curve_Params.curve)

    T1 : Point = Curve_Params.curve.mul_point(SPK_pr, ik_pub_partner)
    T2 : Point = Curve_Params.curve.mul_point(ik_priv, ek_pub_partner)
    T3 : Point = Curve_Params.curve.mul_point(SPK_pr, ek_pub_partner)
    T4 : Point = Curve_Params.curve.mul_point(OTK, ek_pub_partner)

    U = concat_x_y_pt(T1) + concat_x_y_pt(T2) +  concat_x_y_pt(T3) +  concat_x_y_pt(T4) + bytearray(b'WhatsUpDoc')

    print("\nGenerating the key Ks, Kenc, & Khmac and theen the HMAC value...", end='\n\n')

    hasher = SHA3_256.new(U)
    Ks = bytearray(hasher.digest())
    return Ks

##################################################
# DO NOT TOUCH THE CONTROL VARIABLES BELOW UNLESS:
#   1) RE-REGISTERING THE USER
#       - register_user = True
#       - register_otk  = True
#       - all others    = False
#   2) PHASE 2 CHECK
#       - check_for_messages = True
#       - req_deleted_msgs   = True
#       - all others         = False
#   3) RESETTING KEYS
#       - reset_keys = True
#       - all others = False
##################################################

register_user      : bool = False
register_otk       : bool = False
reset_keys         : bool = False
req_deleted_msgs   : bool = True


if __name__ == "__main__":
    # REGISTRATION - FROM PHASE 1
    seed = 13
    IK : Tuple[int | None, Point | None] = genIK(13)
    ik_priv: int = IK[0]
    ik_pub: Point = IK[1]
    assert(ik_priv is not None)


    if (register_user):
        registration_HS : Tuple[int, int] | None = register_ik(stuID, ik_priv, ik_pub)
        assert(registration_HS is not None)
        stu_id_h, stu_id_s = registration_HS
    else:
        reg_id_signature : Tuple[int, int] = gen_sig(stuID, ik_priv)
        stu_id_h, stu_id_s = reg_id_signature[0], reg_id_signature[1]


    if (register_user):
        reg_req_code = int(input("Enter registration code you recevied via email: "))
    else:
        reg_req_code = 238155 # registration code from last register_user run goes here

    if (register_user):
        registration_verif(reg_req_code)
    
    if reset_keys:
        reset_code = int(input("Enter the reset code you received via email: "))
        ResetIK(reset_code)
        ResetSPK(stu_id_h, stu_id_s)
        ResetOTK(stu_id_h, stu_id_s)
    else:
        reset_code : int = 567537 # reset code from last reset_keys run goes here

    SPK : Tuple[int, Point] = gen_SPK(seed)
    (SPK_pr, SPK_pub) = SPK

    if (register_user):
        SPKey_sig_H, SPKey_sig_S = register_SPK(SPK_pr, SPK_pub, ik_priv)
    
    k_hmac : bytearray = gen_hmac_key(SPK_pr, IKey_Ser)

    # same seed generates the same otks -- so that we have a copy of the otks on the client:
    reg_otk_return_val = reg_otk(k_hmac, seed, register_otk)
    otk_list, otk_hmac_list = reg_otk_return_val

    # message and otk check
    (numMSG, numOTK, StatusMsg) = Status(stuID, stu_id_h, stu_id_s)
    print(StatusMsg)

    if (numOTK <= 1): # keep getting internal server error when 1 or less otks remain on the server ... weird! 
        reg_otk_return_val = reg_otk(k_hmac, seed, True)
        otk_list, otk_hmac_list = reg_otk_return_val
        response = PseudoSendMsg(stu_id_h, stu_id_s)
        if (response.ok is True):
            numOTK = 10

    if (numMSG <= 0):
        print("Checking the inbox for incoming messages")
        print("+++++++++++++++++++++++++++++++++++++++++++++\n")
        print("Signing my stuID with my private IK", end='\n\n')
        response = PseudoSendMsg(stu_id_h, stu_id_s)
        if (response.ok is True):
            numMSG = 5


    PreKeyBundle = []        
    kdf_key = bytearray(b'')
    next_kdf_key = bytearray(b'')

    enc_key_list  : List[bytearray] = []
    hmac_key_list : List[bytearray] = []
    decr_msg_list : List[str] = []

    sendPreKeyBundle = []
    KDF_send = bytearray(b'')
    next_KDF_send = bytearray(b'')

    send_enc_key_list : List[bytearray] = []
    send_hmac_key_list: List[bytearray] = []
    send_decr_msg_list: List[bytearray] = []

    faulty_msg_id = -1 

    # msg decryption
    for i in range(numMSG):
        print("\n+++++++++++++++++++++++++++++++++++++++++++++\n")
        PreKeyBundle.append( ReqMsg(stu_id_h, stu_id_s) )
        IDB, OTKID, MSGID, MSG, IKX, IKY, EKX, EKY = PreKeyBundle[i]
        
        # renaming to prevent confusion
        partner_stu_id     : int = IDB 
        one_time_prekey_id : int = OTKID
        order_msg          : int = MSGID

        print(f"\nI got this from client {stuIDB}:")
        print(MSG, end='\n\n')

        msg_bytes     : bytearray = int_to_bytearray(MSG)
        nonce_bytes   : bytearray = msg_bytes[:8]
        msg_mac_bytes : bytearray = msg_bytes[-32:]
        ctext_bytes   : bytearray = msg_bytes[8:-32]

        print("Converting the message to bytes to decrypt it...", end='\n\n')
        print("Converted message is:")
        print(msg_bytes)

        Ks = generate_Ks(EKX, EKY, IKX, IKY, SPK_pr, ik_priv, otk_list[one_time_prekey_id][0])
        init_kdf_key = Ks # the first ever kdf key

        # kdf part 
        if (i == 0):
            kdf_key = init_kdf_key
        else: 
            kdf_key = next_kdf_key

        hasher = SHA3_256.new( kdf_key + bytearray(b'JustKeepSwimming') )
        enc_key = bytearray(hasher.digest())
        
        enc_key_list.append(enc_key)

        hasher = SHA3_256.new( kdf_key + enc_key + bytearray(b'HakunaMatata') )
        hmac_key = bytearray(hasher.digest())

        hmac_key_list.append(hmac_key)

        hasher = SHA3_256.new( enc_key + hmac_key + bytearray(b'OhanaMeansFamily') )
        next_kdf_key = bytearray(hasher.digest())

        # msg decryption 
        aes_inst = AES.new(enc_key, AES.MODE_CTR, nonce=nonce_bytes)
        ptext_bytes : bytearray  = bytearray(aes_inst.decrypt(ctext_bytes))

        # hmac check
        hmac_inst = HMAC.new(hmac_key, digestmod=SHA256)
        hmac_inst.update(ctext_bytes)

        print(f"hmac is: {bytes(msg_mac_bytes)}", end='\n\n')

        try:
            hmac_inst.verify(msg_mac_bytes)
            print("Hmac value is verified")
            # print(f"MAC of message {i} is correct")
            ptext_str : str = ptext_bytes.decode('ascii')
            print(f"The collected plaintext: {ptext_str}")
            decr_msg_list.append(ptext_str)
        except ValueError:
            faulty_msg_id = i
            print("Hmac value couldn't be verified")
            # print(f"MAC of message {i} is WRONG, sending INVALIDHMAC instead")
            decr_msg_list.append("INVALIDHMAC")
            ptext_str = "INVALIDHMAC"
        
        # send decrypted message for checking
        Checker(stuID, stuIDB, MSGID, ptext_str)
    
        #### encrypting the same message and sending it back part -- phase 3 ####
        if (decr_msg_list[i] != "INVALIDHMAC"):
            print("Requesting pre key bundle")
            (stuidb_h, stuidb_s) = gen_sig(stuIDB, ik_priv)
            key_bundle_send = reqKeyBundle(stuID, stuIDB, stuidb_h, stuidb_s)
            sendPreKeyBundle.append(key_bundle_send)

            receiver_keyid, receiver_ikx, receiver_iky, receiver_spkx, reveiver_spky, receiver_spkh, receiver_spks, receiver_otkx, receiver_otky = key_bundle_send

            receiver_IK:  Point = Point(receiver_ikx, receiver_iky, Curve_Params.curve)
            receiver_SPK: Point = Point(receiver_spkx, reveiver_spky, Curve_Params.curve)
            receiver_OTK: Point = Point(receiver_otkx, receiver_otky, Curve_Params.curve)
            receiver_OTKID: int = receiver_keyid

            # Verify received pre-key signature 
            sig_prekey_msg: bytearray = int_to_bytearray(receiver_spkx) + int_to_bytearray(reveiver_spky)
            verif_res: bool = verif_sig(sig_prekey_msg, (receiver_spkh, receiver_spks), receiver_IK) # not sure of send_IK

            try:
                assert(verif_res)
                print("Pre-key signature verif successful")
            except: 
                print("Cannot verify pre-key signature, terminating program...")
                exit(1)


            ##### EK AND KS GENERATION -- phase 3 ####
                
            #### genIK generates a scalar, point pair (as good as any) hence we can reuse it here:
            sender_EK_priv, sender_EK_pub = genIK(seed + 1)
            mulpt = Curve_Params.curve.mul_point
            T1 = mulpt(ik_priv, receiver_SPK)
            T2 = mulpt(sender_EK_priv, receiver_IK)
            T3 = mulpt(sender_EK_priv, receiver_SPK)
            T4 = mulpt(sender_EK_priv, receiver_OTK)
            U = concat_x_y_pt(T1) + concat_x_y_pt(T2) +  concat_x_y_pt(T3) +  concat_x_y_pt(T4) + bytearray(b'WhatsUpDoc')

            print("Generating the KDF chain for the encryption and the MAC value generation", end='\n')

            print("Generating session key / Phase 3...")

            print("U is:")
            print(bytes(U))

            hasher = SHA3_256.new(U)
            KS_sending_msg = bytearray(hasher.digest())

            KDF_sending_init = KS_sending_msg

            # KDF chain for sending
            if (i == 0):
                KDF_send = KDF_sending_init
            else:
                KDF_send = next_KDF_send

            hasher = SHA3_256.new(KDF_send + bytearray(b'JustKeepSwimming') )
            send_enc_key = bytearray(hasher.digest())

            send_enc_key_list.append(send_enc_key)

            hasher = SHA3_256.new(KDF_send + send_enc_key + bytearray(b'HakunaMatata'))
            send_hmac_key = bytearray(hasher.digest())

            send_hmac_key_list.append(send_hmac_key)

            hasher = SHA3_256.new(send_enc_key + send_hmac_key + bytearray(b'OhanaMeansFamily') )
            next_KDF_send = bytearray(hasher.digest())

            # aes encryption
            aes_inst_send = AES.new(send_enc_key, AES.MODE_CTR, nonce=nonce_bytes)
            send_ctext_bytes: bytearray = (aes_inst_send.encrypt(ptext_bytes))

            # hmac generation
            send_hmac_inst = HMAC.new(send_hmac_key, digestmod=SHA256)
            send_hmac_inst.update(send_ctext_bytes)
            send_hmac_bytes = bytearray(send_hmac_inst.digest())

            send_MSG: bytearray = nonce_bytes + send_ctext_bytes + send_hmac_bytes

            # sending message to psudo-client
            print("Sending the message to the server, so it would deliver it to pseudo-client/user whenever it is active ...")
            SendMsg(stuID, stuIDB, receiver_OTKID, MSGID, bytearray_to_int(send_MSG), ik_pub.x, ik_pub.y, sender_EK_pub.x, sender_EK_pub.y)


    ##### end of for loop #####

    # DELETED messages part
    if (req_deleted_msgs):
        print("\n+++++++++++++++++++++++++++++++++++++++++++++\n")
        list_del_msgs = ReqDelMsg(stu_id_h, stu_id_s)

        print("\nChecking whether there were some deleted messages!!")
        print("==========================================")

        for i in range(numMSG):
            if i != faulty_msg_id:
                print(f"Message {i+1}", end=' - ')
                if ( list_del_msgs != None and i + 1 in list_del_msgs ):
                    print("Was deleted by sender - X")
                else:
                    print(f"{decr_msg_list[i]} - Read")

