try:
    import bpy
except ImportError:
    print("Warning: bpy module not found. This script must be run inside Blender.")
    
bl_info = {
    "name": "GothaLinker",
    "description": "Animar y mejorar animaciones desed shape keys",
    "author": "Gonzalo Castro (Gotharo)",
    "version": (2, 1),
    "blender": (4, 2, 7),
    "category": "Object",
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

# Libreria para BlendShapes

from .Phon_config import phoneme_configs

def apply_phoneme_config(phoneme_name):
    print(f"Aplicando configuración para el fonema: {phoneme_name}")
    if phoneme_name not in phoneme_configs:
        print(f"Error: El fonema '{phoneme_name}' no está definido en las configuraciones.")
        return

    config = phoneme_configs[phoneme_name]
    for controller_name, (value_x, value_y) in config.items():
        controller_obj = bpy.data.objects.get(controller_name)
        if controller_obj:
            # Aplicar los valores a las coordenadas del objeto
            controller_obj.location.x = value_x
            controller_obj.location.y = value_y
            print(f"Configuración aplicada a '{controller_name}': ({value_x}, {value_y})")
        else:
            print(f"Error: No se encontró el controlador '{controller_name}' en la escena.")

def Linker():
    print("Ejecutando Linker")
    selected_obj = bpy.context.object
    if not selected_obj or not selected_obj.data.shape_keys:
        print("Error: No hay un objeto seleccionado o no tiene Shape Keys.")
    else:
        shape_keys = selected_obj.data.shape_keys.key_blocks
        riggui_collection = bpy.data.collections.get("RIGGUI")
        if not riggui_collection:
            print("Error: La colección 'RIGGUI' no existe en la escena.")
        else:
            for shape_key_name, (controller_name, (axis, direction)) in control_pairs.items():
                shape_key = shape_keys.get(shape_key_name)
                controller_obj = riggui_collection.objects.get(controller_name)
                if shape_key and controller_obj:
                    axis_index = 0 if axis == "X" else 1
                    driver = shape_key.driver_add("value")
                    driver.driver.type = 'SCRIPTED'
                    var = driver.driver.variables.new()
                    var.name = "controller_pos"
                    var.type = 'TRANSFORMS'
                    target = var.targets[0]
                    target.id = controller_obj
                    target.transform_type = f"LOC_{axis}"
                    target.transform_space = 'LOCAL_SPACE'
                    if direction == -1:
                        driver.driver.expression = "max(0, min(1, -controller_pos))"
                    else:
                        driver.driver.expression = "max(0, min(1, controller_pos))"
                    print(f"Driver agregado: '{controller_name}' controla '{shape_key_name}' en eje {axis} ({'Negativo' if direction == -1 else 'Positivo'})")
                else:
                    print(f"Error: No se encontraron '{shape_key_name}' o '{controller_name}' en la colección 'RIGGUI'.")

def Unlink():
    print("Ejecutando Unlink")
    obj = bpy.context.active_object
    if obj and obj.data.shape_keys:
        shape_keys = obj.data.shape_keys.key_blocks
        anim_data = obj.data.shape_keys.animation_data
        if anim_data:
            for driver in anim_data.drivers:
                if driver.data_path.startswith("key_blocks["):
                    anim_data.drivers.remove(driver)
            print("Drivers eliminados de todos los shape keys.")
        else:
            print("No hay drivers asociados a los shape keys.")
    else:
        print("El objeto no tiene shape keys.")

def Clearshapes():
    print("Ejecutando Clearshapes")
    obj = bpy.context.active_object

    # Verificar si el objeto tiene shape keys
    if obj and obj.data.shape_keys:
        # Obtener los shape keys
        shape_keys = obj.data.shape_keys.key_blocks
        
        # Obtener la animación de datos (animation data) del objeto
        anim_data = obj.data.shape_keys.animation_data
        
        if anim_data:
            # Recorrer todos los shape keys
            for shape_key in shape_keys:
                # Establecer el valor del shape key a 0
                shape_key.value = 0
                
                # Obtener la ruta de datos (data path) del shape key
                data_path = f'key_blocks["{shape_key.name}"].value'
                
                # Buscar y eliminar los keyframes asociados al shape key
                if anim_data.action:
                    for fcurve in anim_data.action.fcurves:
                        if fcurve.data_path == data_path:
                            # Eliminar todos los keyframes del fcurve
                            anim_data.action.fcurves.remove(fcurve)
            
            print("Todos los valores de los shape keys han sido establecidos a 0 y los keyframes eliminados.")
        else:
            print("No hay animación asociada a los shape keys.")
    else:
        print("El objeto no tiene shape keys.")

def Bake_ctrlstoshapes():
    print("Ejecutando Bake_ctrlstoshapes")
    selected_obj = bpy.context.object
    if not selected_obj or not selected_obj.data.shape_keys:
        print("Error: No hay un objeto seleccionado o no tiene Shape Keys.")
    else:
        shape_keys = selected_obj.data.shape_keys
        riggui_collection = bpy.data.collections.get("RIGGUI")
        if not riggui_collection:
            print("Error: La colección 'RIGGUI' no existe en la escena.")
        else:
            shape_key_curves = {}
            for shape_key_name, (controller_name, (axis, direction)) in control_pairs.items():
                shape_key = shape_keys.key_blocks.get(shape_key_name)
                controller_obj = riggui_collection.objects.get(controller_name)
                if shape_key and controller_obj:
                    axis_index = 0 if axis == "X" else 1
                    if not controller_obj.animation_data or not controller_obj.animation_data.action:
                        print(f"Advertencia: El controlador '{controller_name}' no tiene datos de animación.")
                        continue
                    controller_action = controller_obj.animation_data.action
                    fcurve = next((fc for fc in controller_action.fcurves if fc.data_path == "location" and fc.array_index == axis_index), None)
                    if fcurve:
                        if not shape_keys.animation_data:
                            shape_keys.animation_data_create()
                        if not shape_keys.animation_data.action:
                            shape_keys.animation_data.action = bpy.data.actions.new(name=f"{selected_obj.name}_ShapeKey_Action")
                        shape_key_action = shape_keys.animation_data.action
                        shape_key_path = f'key_blocks["{shape_key.name}"].value'
                        if shape_key_name not in shape_key_curves:
                            shape_key_fcurve = shape_key_action.fcurves.find(shape_key_path)
                            if not shape_key_fcurve:
                                shape_key_fcurve = shape_key_action.fcurves.new(data_path=shape_key_path, index=0)
                            shape_key_fcurve.keyframe_points.clear()
                            shape_key_curves[shape_key_name] = shape_key_fcurve
                        else:
                            shape_key_fcurve = shape_key_curves[shape_key_name]
                        for kp in fcurve.keyframe_points:
                            frame, value = kp.co
                            new_value = value if direction > 0 else -value
                            existing_kp = next((p for p in shape_key_fcurve.keyframe_points if p.co.x == frame), None)
                            if existing_kp:
                                existing_kp.co.y += new_value
                            else:
                                shape_key_fcurve.keyframe_points.insert(frame, new_value)
                        print(f"Animación copiada de '{controller_name}' a Shape Key '{shape_key_name}' en el eje {axis} ({'Negativo' if direction == -1 else 'Positivo'})")
            print("Todas las animaciones han sido copiadas correctamente a los Shape Keys.")

def Bake_Shapestoctrls():
    print("Ejecutando Bake_Shapestoctrls")
    selected_obj = bpy.context.object
    if not selected_obj or not selected_obj.data.shape_keys:
        print("Error: No hay un objeto seleccionado o no tiene Shape Keys.")
    else:
        shape_keys = selected_obj.data.shape_keys
        if not shape_keys.animation_data or not shape_keys.animation_data.action:
            print("Error: No hay animaciones en los Shape Keys.")
        else:
            shape_key_action = shape_keys.animation_data.action
            riggui_collection = bpy.data.collections.get("RIGGUI")
            if not riggui_collection:
                print("Error: La colección 'RIGGUI' no existe en la escena.")
            else:
                controller_curves = {}
                for shape_key_name, (controller_name, (axis, direction)) in control_pairs.items():
                    shape_key = shape_keys.key_blocks.get(shape_key_name)
                    controller_obj = riggui_collection.objects.get(controller_name)
                    if shape_key and controller_obj:
                        fcurve = shape_key_action.fcurves.find(f'key_blocks["{shape_key.name}"].value')
                        if fcurve:
                            axis_index = 0 if axis == "X" else 1
                            if not controller_obj.animation_data:
                                controller_obj.animation_data_create()
                            if not controller_obj.animation_data.action:
                                controller_obj.animation_data.action = bpy.data.actions.new(name=f"{controller_name}_Action")
                            controller_action = controller_obj.animation_data.action
                            path = f'location[{axis_index}]'
                            if controller_name not in controller_curves:
                                controller_curves[controller_name] = {}
                            if path not in controller_curves[controller_name]:
                                ctrl_fcurve = controller_action.fcurves.find(path)
                                if not ctrl_fcurve:
                                    ctrl_fcurve = controller_action.fcurves.new(data_path="location", index=axis_index)
                                ctrl_fcurve.keyframe_points.clear()
                                controller_curves[controller_name][path] = ctrl_fcurve
                            else:
                                ctrl_fcurve = controller_curves[controller_name][path]
                            for kp in fcurve.keyframe_points:
                                frame, value = kp.co
                                new_value = max(-1, min(1, value if direction > 0 else -value))
                                existing_kp = next((p for p in ctrl_fcurve.keyframe_points if p.co.x == frame), None)
                                if existing_kp:
                                    # Se reemplaza el valor existente sin sumarlo
                                    existing_kp.co.y = new_value
                                else:
                                    ctrl_fcurve.keyframe_points.insert(frame, new_value)
                            print(f"Animación copiada de Shape Key '{shape_key_name}' a '{controller_name}' en el eje {axis} ({'Negativo' if direction == -1 else 'Positivo'})")
                print("Todas las animaciones han sido copiadas correctamente a los controladores.")
               
def Keyshapes():
    print("Ejecutando Keyshapes")
    selected_obj = bpy.context.object
    if selected_obj and selected_obj.type == 'MESH' and selected_obj.data.shape_keys:
        shape_keys = selected_obj.data.shape_keys.key_blocks
        current_frame = bpy.context.scene.frame_current
        for shape_key in shape_keys:
            shape_key.value = shape_key.value
            shape_key.keyframe_insert(data_path="value", frame=current_frame)
        print("Keyframed all shape keys.")
    else:
        print("No shape keys found on the active object.")

# Función para seleccionar objetos
def seleccionar_objetos(lista_objetos):
    bpy.ops.object.select_all(action='DESELECT')  # Deseleccionar todos los objetos
    for obj in bpy.data.objects:
        if obj.name in lista_objetos:
            obj.select_set(True)  # Seleccionar el objeto
            bpy.context.view_layer.objects.active = obj  # Asegurar que se mantenga activo

# operadores para cada fonema

class ApplyPhonemeFVOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_fv"
    bl_label = "Aplicar FV"
    bl_description = "Aplica la configuración del fonema FV"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("FV")
        return {'FINISHED'}


class ApplyPhonemeAEOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_ae"
    bl_label = "Aplicar AE"
    bl_description = "Aplica la configuración del fonema AE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("AE")
        return {'FINISHED'}

class ApplyPhonemeAHOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_ah"
    bl_label = "Aplicar AH"
    bl_description = "Aplica la configuración del fonema AH"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("AH")
        return {'FINISHED'}

class ApplyPhonemeBMPOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_bmp"
    bl_label = "Aplicar BMP"
    bl_description = "Aplica la configuración del fonema BMP"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("BMP")
        return {'FINISHED'}

class ApplyPhonemeChJOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_chj"
    bl_label = "Aplicar ChJ"
    bl_description = "Aplica la configuración del fonema ChJ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("ChJ")
        return {'FINISHED'}
    
class ApplyPhonemeEESZTLDNOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_eesztldn"
    bl_label = "Aplicar EESZTLDN"
    bl_description = "Aplica la configuración del fonema EESZTLDN"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("EESZTLDN")
        return {'FINISHED'}
    
class ApplyPhonemeErOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_er"
    bl_label = "Aplicar Er"
    bl_description = "Aplica la configuración del fonema Er"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("Er")
        return {'FINISHED'}

class ApplyPhonemeIhOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_ih"
    bl_label = "Aplicar Ih"
    bl_description = "Aplica la configuración del fonema Ih"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("Ih")
        return {'FINISHED'}

class ApplyPhonemeKGHNGOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_kghng"
    bl_label = "Aplicar KGHNG"
    bl_description = "Aplica la configuración del fonema KGHNG"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("KGHNG")
        return {'FINISHED'}

class ApplyPhonemeOhOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_oh"
    bl_label = "Aplicar Oh"
    bl_description = "Aplica la configuración del fonema Oh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("Oh")
        return {'FINISHED'}

class ApplyPhonemeROperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_r"
    bl_label = "Aplicar R"
    bl_description = "Aplica la configuración del fonema R"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("R")
        return {'FINISHED'}

class ApplyPhonemeThOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_th"
    bl_label = "Aplicar Th"
    bl_description = "Aplica la configuración del fonema Th"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("Th")
        return {'FINISHED'}
    
class ApplyPhonemeWOOOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_woo"
    bl_label = "Aplicar WOO"
    bl_description = "Aplica la configuración del fonema WOO"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("WOO")
        return {'FINISHED'}

class MIADDON_OT_Linker(bpy.types.Operator):
    bl_idname = "miaddon.linker"
    bl_label = "Ejecutar Linker"

    def execute(self, context):
        Linker()
        return {'FINISHED'}

class MIADDON_OT_Unlink(bpy.types.Operator):
    bl_idname = "miaddon.unlink"
    bl_label = "Ejecutar Unlink"

    def execute(self, context):
        Unlink()
        return {'FINISHED'}

class MIADDON_OT_Clearshapes(bpy.types.Operator):
    bl_idname = "miaddon.clearshapes"
    bl_label = "Ejecutar Clearshapes"

    def execute(self, context):
        Clearshapes()
        return {'FINISHED'}
    
class MIADDON_OT_Bake_ctrlstoshapes(bpy.types.Operator):
    bl_idname = "miaddon.bake_ctrlstoshapes"
    bl_label = "Ejecutar Bake_ctrlstoshapes"

    def execute(self, context):
        Bake_ctrlstoshapes()
        return {'FINISHED'}

class MIADDON_OT_Bake_Shapestoctrls(bpy.types.Operator):
    bl_idname = "miaddon.bake_shapestoctrls"
    bl_label = "Ejecutar Bake_Shapestoctrls"

    def execute(self, context):
        Bake_Shapestoctrls()
        return {'FINISHED'}
    
class MIADDON_OT_Keyshapes(bpy.types.Operator):
    bl_idname = "miaddon.keyshapes"
    bl_label = "Ejecutar Keyshapes"

    def execute(self, context):
        Keyshapes()
        return {'FINISHED'}

class OBJECT_OT_select_riggui(bpy.types.Operator):
    """Selecciona todos los objetos dentro de la colección 'RIGGUI', excluyendo 'CTRL_faceGUI'"""
    bl_idname = "object.select_riggui"
    bl_label = "Select RIGGUI"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Nombre de la colección a seleccionar
        collection_name = "RIGGUI"

        # Obtener la colección
        riggui_collection = bpy.data.collections.get(collection_name)

        if not riggui_collection:
            self.report({'ERROR'}, f"La colección '{collection_name}' no existe en la escena.")
            return {'CANCELLED'}

        # Deseleccionar todo antes de seleccionar los objetos en la colección
        bpy.ops.object.select_all(action='DESELECT')

        # Seleccionar todos los objetos dentro de la colección, excluyendo 'CTRL_faceGUI'
        for obj in riggui_collection.objects:
            if obj.name != "CTRL_faceGUI":  # Excluir este objeto específico
                obj.select_set(True)

        self.report({'INFO'}, f"Todos los objetos en la colección '{collection_name}', excepto 'CTRL_faceGUI', han sido seleccionados.")
        return {'FINISHED'}

class SeleccionarObjetosBrowsOperator(bpy.types.Operator):
    bl_idname = "object.seleccionar_objetos_brows"
    bl_label = "Sel Brows"
    bl_description = "Selecciona los objetos relacionados con las cejas en el viewport"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        seleccionar_objetos(objetos_brows)  # Pasar la lista correspondiente
        return {'FINISHED'}

class SeleccionarObjetosMidHeadOperator(bpy.types.Operator):
    bl_idname = "object.seleccionar_objetos_mid_head"
    bl_label = "Sel E-N-E"
    bl_description = "Selecciona los objetos relacionados con ojos, nariz y orejas"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        seleccionar_objetos(objetos_mid_Head)  # Pasar la lista correspondiente
        return {'FINISHED'}

class SeleccionarObjetosMouthJawOperator(bpy.types.Operator):
    bl_idname = "object.seleccionar_objetos_mouth_jaw"
    bl_label = "Sel Mouth-Jaw"
    bl_description = "Selecciona los objetos relacionados con la boca y la mandíbula"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        seleccionar_objetos(objetos_mouth_jaw)  # Pasar la lista correspondiente
        return {'FINISHED'}

# Class para Blenshapes



class MIADDON_PT_Panel(bpy.types.Panel):
    bl_label = "CTRLsAndShapes Panel"
    bl_idname = "MIADDON_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GothaLinkerV2'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text='Linking head and shapes', icon='OUTLINER')

        row = layout.row()
        row.operator("miaddon.linker", text="Linker", icon='LINKED')
        row.operator("miaddon.unlink", text="Unlink", icon='UNLINKED')

        row = layout.row()
        row.label(text='Key&Clear', icon='MONKEY')
        row = layout.row()        
        row.operator("miaddon.clearshapes", text="Clearshapes", icon='MATFLUID')
        row.operator("miaddon.keyshapes", text="Keyshapes", icon='KEYINGSET')

        row = layout.row()
        row.label(text='Bake Ctrls&Shapes', icon='RESTRICT_SELECT_OFF')

        row = layout.row()
        row.operator("miaddon.bake_ctrlstoshapes", text="Bake_ctrlstoshapes")

        row = layout.row()
        row.operator("miaddon.bake_shapestoctrls", text="Bake_Shapestoctrls")


        # Agregar el botón del nuevo operador
        row = layout.row()
        
        row.operator("object.select_riggui", text="Select RIGGUI")

        row = layout.row()
        row.label(text='SET SELECTORS', icon='RESTRICT_SELECT_OFF')
        row = layout.row()
        row.operator("object.seleccionar_objetos_brows", text="Sel Brows")
        row.operator("object.seleccionar_objetos_mid_head", text="Sel E-N-E")
        row.operator("object.seleccionar_objetos_mouth_jaw", text="Sel Mouth-Jaw")

        # Botones para los fonemas
        row = layout.row()
        row.label(text='SET PHONEMES', icon='STATUSBAR')
        row = layout.row()
        row.operator("object.apply_phoneme_fv", text="FV")
        row.operator("object.apply_phoneme_ae", text="AE")
        row.operator("object.apply_phoneme_ah", text="AH")
        row.operator("object.apply_phoneme_bmp", text="BMP")

        row = layout.row()
        row.operator("object.apply_phoneme_chj", text="ChJ")
        row.operator("object.apply_phoneme_eesztldn", text="EESZTLDN")
        row.operator("object.apply_phoneme_er", text="Er")
        row.operator("object.apply_phoneme_ih", text="Ih")
        
        row = layout.row()
        row.operator("object.apply_phoneme_kghng", text="KGHNG")
        row.operator("object.apply_phoneme_oh", text="Oh")
        row.operator("object.apply_phoneme_r", text="R")
        row.operator("object.apply_phoneme_th", text="Th")

        row = layout.row()
        row.operator("object.apply_phoneme_woo", text="WOO")
        


def register():
    bpy.utils.register_class(MIADDON_PT_Panel)
    bpy.utils.register_class(MIADDON_OT_Linker)
    bpy.utils.register_class(MIADDON_OT_Unlink)
    bpy.utils.register_class(MIADDON_OT_Clearshapes)
    bpy.utils.register_class(MIADDON_OT_Bake_ctrlstoshapes)
    bpy.utils.register_class(MIADDON_OT_Bake_Shapestoctrls)
    bpy.utils.register_class(MIADDON_OT_Keyshapes)
    bpy.utils.register_class(OBJECT_OT_select_riggui)  # Nueva clase
    bpy.utils.register_class(SeleccionarObjetosBrowsOperator)
    bpy.utils.register_class(SeleccionarObjetosMidHeadOperator)
    bpy.utils.register_class(SeleccionarObjetosMouthJawOperator)
    bpy.utils.register_class(ApplyPhonemeFVOperator)
    bpy.utils.register_class(ApplyPhonemeAEOperator)
    bpy.utils.register_class(ApplyPhonemeAHOperator)
    bpy.utils.register_class(ApplyPhonemeBMPOperator)
    bpy.utils.register_class(ApplyPhonemeChJOperator)
    bpy.utils.register_class(ApplyPhonemeEESZTLDNOperator)
    bpy.utils.register_class(ApplyPhonemeErOperator)
    bpy.utils.register_class(ApplyPhonemeIhOperator)
    bpy.utils.register_class(ApplyPhonemeKGHNGOperator)
    bpy.utils.register_class(ApplyPhonemeOhOperator)
    bpy.utils.register_class(ApplyPhonemeROperator)
    bpy.utils.register_class(ApplyPhonemeThOperator)
    bpy.utils.register_class(ApplyPhonemeWOOOperator)
    
    
def unregister():
    bpy.utils.unregister_class(MIADDON_OT_Linker)
    bpy.utils.unregister_class(MIADDON_OT_Unlink)
    bpy.utils.unregister_class(MIADDON_OT_Clearshapes)
    bpy.utils.unregister_class(MIADDON_OT_Bake_ctrlstoshapes)
    bpy.utils.unregister_class(MIADDON_OT_Bake_Shapestoctrls)
    bpy.utils.unregister_class(MIADDON_OT_Keyshapes)
    bpy.utils.unregister_class(OBJECT_OT_select_riggui)  # Nueva clase
    bpy.utils.unregister_class(SeleccionarObjetosBrowsOperator)
    bpy.utils.unregister_class(SeleccionarObjetosMidHeadOperator)
    bpy.utils.unregister_class(SeleccionarObjetosMouthJawOperator)
    bpy.utils.unregister_class(ApplyPhonemeFVOperator)
    bpy.utils.unregister_class(ApplyPhonemeAEOperator)
    bpy.utils.unregister_class(ApplyPhonemeAHOperator)
    bpy.utils.unregister_class(ApplyPhonemeBMPOperator)
    bpy.utils.unregister_class(ApplyPhonemeChJOperator)
    bpy.utils.unregister_class(ApplyPhonemeEESZTLDNOperator)
    bpy.utils.unregister_class(ApplyPhonemeErOperator)
    bpy.utils.unregister_class(ApplyPhonemeIhOperator)
    bpy.utils.unregister_class(ApplyPhonemeKGHNGOperator)
    bpy.utils.unregister_class(ApplyPhonemeOhOperator)
    bpy.utils.unregister_class(ApplyPhonemeROperator)
    bpy.utils.unregister_class(ApplyPhonemeThOperator)
    bpy.utils.unregister_class(ApplyPhonemeWOOOperator)
    
if __name__ == "__main__":
    register()