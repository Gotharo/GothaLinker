phoneme_configs = {
    "FV": {
        "CTRL_L_mouth_towardsU": (0.0, 0.2333),
        "CTRL_R_mouth_towardsD": (0.0, 0.7939)
    },
    "AE": {
        "CTRL_L_mouth_suckBlow": (0.0000, 0.2026),
        "CTRL_R_mouth_suckBlow": (0.0000, 0.2026),
        "CTRL_L_mouth_towardsU": (0.0000, 0.1604),
        "CTRL_R_mouth_pressD": (0.0000, 0.0357),
        "CTRL_C_jaw": (0.0000, 0.3210)
    },
    "AH": {
        "CTRL_L_mouth_towardsU": (0.0, 0.2527),
        "CTRL_R_mouth_pressD": (0.0, 0.0865),
        "CTRL_C_jaw": (0.0, 0.5748)
    },
    "BMP": {
        "CTRL_L_mouth_towardsU": (0.0, 0.1181),
        "CTRL_L_mouth_towardsD": (0.0, 0.2686)
    },
    "ChJ": {
        "CTRL_R_mouth_funnelD": (0.0, 0.8126)
    },
    "EESZTLDN": {
        "CTRL_L_mouth_sharpCornerPull": (0.0, 0.3750),
        "CTRL_R_mouth_sharpCornerPull": (0.0, 0.3418),
        "CTRL_L_mouth_cornerPull": (0.0000, 0.3284),
        "CTRL_R_mouth_cornerPull": (0.0000, 0.3284),
        "CTRL_L_mouth_dimple": (0.0000, 0.3164),
        "CTRL_R_mouth_dimple": (0.0000, 0.3164),
        "CTRL_L_mouth_suckBlow": (0.0000, -0.2026),
        "CTRL_R_mouth_suckBlow": (0.0000, -0.2026),
        "CTRL_C_jaw": (0.0000, 0.1299)
    },
    "Er": {
        "CTRL_L_mouth_sharpCornerPull": (0.0000, 0.3247),
        "CTRL_R_mouth_sharpCornerPull": (0.0000, 0.3247),
        "CTRL_C_jaw": (0.0000, 0.1898)
    },
    "Ih": {
        "CTRL_L_mouth_sharpCornerPull": (0.0000, 0.3247),
        "CTRL_R_mouth_sharpCornerPull": (0.0000, 0.3247),
        "CTRL_C_jaw": (0.0000, 0.1225)
    },
    "KGHNG": {
        "CTRL_L_mouth_sharpCornerPull": (0.0000, 0.3247),
        "CTRL_R_mouth_sharpCornerPull": (0.0000, 0.3247),
        "CTRL_L_mouth_cornerDepress": (0.0000, 0.0488),
        "CTRL_R_mouth_cornerDepress": (0.0000, 0.0488),
        "CTRL_R_mouth_funnelD": (0.0000, 0.2229),
        "CTRL_R_mouth_pressD": (0.0000, 0.1487),
        "CTRL_C_jaw": (0.0000, 0.1052)
    },
    "Oh": {
        "CTRL_L_mouth_sharpCornerPull": (0.0000, 0.0773),
        "CTRL_R_mouth_sharpCornerPull": (0.0000, 0.0773),
        "CTRL_L_mouth_cornerPull": (0.0000, 0.3752),
        "CTRL_R_mouth_cornerPull": (0.0000, 0.3752),
        "CTRL_L_mouth_cornerDepress": (0.0000, 0.3684),
        "CTRL_R_mouth_cornerDepress": (0.0000, 0.3684),
        "CTRL_R_mouth_purseD": (0.0000, 0.6445),
        "CTRL_L_mouth_towardsD": (0.0000, 0.3996),
        "CTRL_R_mouth_pressD": (0.0000, 0.1428),
        "CTRL_C_jaw": (0.0000, 0.5399)
    },
    "R": {
        "CTRL_R_mouth_purseD": (0.0000, 0.6460),
        "CTRL_R_mouth_pressD": (0.0000, 0.0785),
        "CTRL_C_jaw": (0.0000, 0.1212)
    },
    "Th": {
        "CTRL_L_mouth_sharpCornerPull": (0.0000, 0.3247),
        "CTRL_R_mouth_sharpCornerPull": (0.0000, 0.3247),
        "CTRL_R_mouth_purseD": (0.0000, 0.6460),
        "CTRL_R_mouth_pressD": (0.0000, 0.1260),
        "CTRL_C_jaw": (0.0000, 0.1831)
    },
    "WOO": {
        "CTRL_L_mouth_sharpCornerPull": (0.0000, 0.1548),
        "CTRL_R_mouth_sharpCornerPull": (0.0000, 0.1548),
        "CTRL_L_mouth_cornerPull": (0.0000, 0.1594),
        "CTRL_R_mouth_cornerPull": (0.0000, 0.1594),
        "CTRL_L_mouth_cornerDepress": (0.0000, 0.0668),
        "CTRL_R_mouth_cornerDepress": (0.0000, 0.0668),
        "CTRL_L_mouth_stretch": (0.0000, 0.0651),
        "CTRL_R_mouth_stretch": (0.0000, 0.0651),
        "CTRL_L_mouth_suckBlow": (0.0000, -0.1407),
        "CTRL_R_mouth_suckBlow": (0.0000, -0.1407),
        "CTRL_R_mouth_purseD": (0.0000, 0.9529),
        "CTRL_L_mouth_towardsD": (0.0000, 0.1238),
        "CTRL_R_mouth_funnelD": (0.0000, 0.2012),
        "CTRL_R_mouth_pressD": (0.0000, 0.1159)
    }
}

# Lista de shape keys, controladores y direcciones
control_pairs = {

    "eyeWideRight": ("CTRL_R_eye_blink", ("Y", -1)),   # Y Negativo
    "eyeWideLeft": ("CTRL_L_eye_blink", ("Y", -1)),    # Y Negativo
    "eyeBlinkLeft": ("CTRL_L_eye_blink", ("Y", 1)),    # Y Positivo
    "eyeBlinkRight": ("CTRL_R_eye_blink", ("Y", 1)),   # Y Positivo
    "mouthRight": ("CTRL_C_mouth", ("X", -1)),         # X Positivo
    "mouthLeft": ("CTRL_C_mouth", ("X", 1)),         # X Negativo
    "jawRight": ("CTRL_C_jaw", ("X", 1)),             # X Positivo
    "jawLeft": ("CTRL_C_jaw", ("X", -1)),             # X Negativo
    "eyeLookDownLeft": ("CTRL_C_eye", ("Y", -1)),     # Y Negativo
    "eyeLookDownRight": ("CTRL_C_eye", ("Y", -1)),    # Y Negativo
    "eyeLookUpRight": ("CTRL_C_eye", ("Y", 1)),       # Y Positivo
    "eyeLookUpLeft": ("CTRL_C_eye", ("Y", 1)),        # Y Positivo
    "eyeLookInLeft": ("CTRL_C_eye", ("X", -1)),       # X Negativo
    "eyeLookOutLeft": ("CTRL_C_eye", ("X", 1)),       # X Positivo
    "eyeLookInRight": ("CTRL_C_eye", ("X", 1)),       # X Positivo
    "eyeLookOutRight": ("CTRL_C_eye", ("X", -1)),     # X Negativo
    "mouthSmileRight": ("CTRL_R_mouth_suckBlow", ("Y", 1)),  # Y Positivo
    "mouthSmileLeft": ("CTRL_L_mouth_suckBlow", ("Y", 1)),   # Y Positivo
    "mouthFrownRight": ("CTRL_R_mouth_suckBlow", ("Y", -1)), # Y Negativo
    "mouthFrownLeft": ("CTRL_L_mouth_suckBlow", ("Y", -1)),  # Y Negativo
    "eyeLookUpRight": ("CTRL_C_eye", ("Y", 1)),      # Y Positivo
    "mouthSmileRight": ("CTRL_R_mouth_suckBlow", ("Y", 1)),   # Y Positivo
    "mouthSmileLeft": ("CTRL_L_mouth_suckBlow", ("Y", 1)),    # Y Positivo
    "eyeLookUpLeft": ("CTRL_C_eye", ("Y", 1)),       # Y Positivo
    "eyeSquintRight": ("CTRL_R_eye_squintInner", ("Y", 1)),  # Y Positivo
    "eyeSquintLeft": ("CTRL_L_eye_squintInner", ("Y", 1)),   # Y Positivo
    "MouthClose": ("CTRL_R_mouth_pressD", ("Y", 1)),  # Y Positivo
    "mouthClose": ("CTRL_R_mouth_pressD", ("Y", 1)),  # Y Positivo
    "mouthFunnel": ("CTRL_R_mouth_funnelD", ("Y", 1)),  # Y Positivo
    "mouthPucker": ("CTRL_R_mouth_purseD", ("Y", 1)),  # Y Positivo
    "mouthDimpleLeft": ("CTRL_L_mouth_dimple", ("Y", 1)),  # Y Positivo
    "mouthDimpleRight": ("CTRL_R_mouth_dimple", ("Y", 1)),  # Y Positivo
    "mouthStretchLeft": ("CTRL_L_mouth_stretch", ("Y", 1)),  # Y Positivo
    "mouthStretchRight": ("CTRL_R_mouth_stretch", ("Y", 1)),  # Y Positivo
    "mouthRollLower": ("CTRL_R_mouth_towardsD", ("Y", 1)),  # Y Positivo
    "mouthRollUpper": ("CTRL_R_mouth_towardsU", ("Y", 1)),  # Y Positivo
    "mouthShrugLower": ("CTRL_L_mouth_towardsD", ("Y", 1)),  # Y Positivo
    "mouthShrugUpper": ("CTRL_L_mouth_towardsU", ("Y", 1)),  # Y Positivo
    "mouthPressLeft": ("CTRL_L_mouth_cornerPull", ("Y", 1)),  # Y Positivo
    "mouthPressRight": ("CTRL_R_mouth_cornerPull", ("Y", 1)),  # Y Positivo
    "mouthLowerDownLeft": ("CTRL_L_mouth_cornerDepress", ("Y", 1)),  # Y Positivo
    "mouthLowerDownRight": ("CTRL_R_mouth_cornerDepress", ("Y", 1)),  # Y Positivo
    "mouthUpperUpLeft": ("CTRL_L_mouth_sharpCornerPull", ("Y", 1)),  # Y Positivo
    "mouthUpperUpRight": ("CTRL_R_mouth_sharpCornerPull", ("Y", 1)),  # Y Positivo
    "jawOpen": ("CTRL_C_jaw", ("Y", 1)),  # Y Positivo
    "jawForward": ("CTRL_C_jaw_fwdBack", ("Y", 1)),  # Y Positivo
    "browInnerUp": ("CTRL_L_brow_raiseIn", ("Y", 1)),  # Y Positivo
    "browDownLeft": ("CTRL_L_brow_down", ("Y", 1)),  # Y Positivo
    "browDownRight": ("CTRL_R_brow_down", ("Y", 1)),  # Y Positivo
    "browOuterUpLeft": ("CTRL_L_brow_raiseOut", ("Y", 1)),  # Y Positivo
    "browOuterUpRight": ("CTRL_R_brow_raiseOut", ("Y", 1)),  # Y Positivo
    "cheekPuff": ("CTRL_L_ear_up", ("Y", 1)),  # Y Positivo
    "cheekSquintLeft": ("CTRL_L_eye_cheekRaise", ("Y", 1)),  # Y Positivo
    "cheekSquintRight": ("CTRL_R_eye_cheekRaise", ("Y", 1)),  # Y Positivo
    "noseSneerLeft": ("CTRL_L_nose_wrinkleUpper", ("Y", 1)),  # Y Positivo
    "noseSneerRight": ("CTRL_R_nose_wrinkleUpper", ("Y", 1)),  # Y Positivo
    "tongueOut": ("CTRL_C_tongue_inOut", ("Y", 1)),  # Y Positivo

}

# Listas de objetos
objetos_brows = [
    "CTRL_L_brow_raiseIn",
    "CTRL_L_brow_raiseOut",
    "CTRL_R_brow_raiseOut",
    "CTRL_L_brow_down",
    "CTRL_R_brow_down",
    "CTRL_L_brow_lateral",
    "CTRL_R_brow_lateral"
]

objetos_mid_Head = [
    "CTRL_C_eye",
    "CTRL_L_eye",
    "CTRL_R_eye",
    "CTRL_L_eye_squintInner",
    "CTRL_R_eye_squintInner",
    "CTRL_L_eye_cheekRaise",
    "CTRL_R_eye_cheekRaise",
    "CTRL_L_eye_blink",
    "CTRL_R_eye_blink",
    "CTRL_C_eye_parallelLook",
    "CTRL_L_ear_up",
    "CTRL_L_nose",
    "CTRL_R_nose",
    "CTRL_L_nose_wrinkleUpper",
    "CTRL_R_nose_wrinkleUpper"
]

objetos_mouth_jaw = [
    
    "CTRL_C_mouth",
    "CTRL_L_mouth_sharpCornerPull",
    "CTRL_R_mouth_sharpCornerPull",
    "CTRL_L_mouth_cornerPull",
    "CTRL_R_mouth_cornerPull",
    "CTRL_L_mouth_dimple",
    "CTRL_R_mouth_dimple",
    "CTRL_L_mouth_cornerDepress",
    "CTRL_R_mouth_cornerDepress",
    "CTRL_L_mouth_stretch",
    "CTRL_R_mouth_stretch",
    "CTRL_L_mouth_suckBlow",
    "CTRL_R_mouth_suckBlow",
    "CTRL_R_mouth_purseD",
    "CTRL_L_mouth_towardsU",
    "CTRL_R_mouth_towardsU",
    "CTRL_L_mouth_towardsD",
    "CTRL_R_mouth_towardsD",
    "CTRL_R_mouth_funnelD",
    "CTRL_R_mouth_pressD",
    "CTRL_C_tongue_inOut",
    "CTRL_C_jaw",
    "CTRL_C_jaw_fwdBack"
]